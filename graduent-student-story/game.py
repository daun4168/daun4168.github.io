import asyncio
import importlib
from pyscript import document
from ui import UIManager, get_josa
from entity import Entity, Item, Inventory
from test import TestRunner

# --- 상수 정의 ---
CMD_INVENTORY = ["주머니"]
CMD_START = "일어나기"
CMD_LOOK_AROUND = "둘러보기"

# --- 게임 데이터 ---
INTRO_TEXT = [
    "당신은 10년차 대학원생입니다.\n...아니, 사실 '학생'이라 불리기엔 너무 늙었고, '연구원'이라 불리기엔 통장에 찍히는 돈이 너무 적습니다.",
    "동기들은 5년 전에 모두 탈출했습니다. 대기업 과장, 스타트업 대표...\n하지만 당신은 아직 이곳에 남아있습니다.",
    "왜냐고요?\n\"자네, 이번 데이터만 잘 나오면 졸업 시켜주겠네.\"\n매 학기 반복되는 그 달콤한 거짓말. 희망 고문.",
    "당신의 몸은 커피와 핫식스로 이루어져 있고,\n당신의 영혼은 이미 연구실 서버실 어딘가에 저당 잡혔습니다.",
    "그리고 오늘...\n드디어 운명의 날이 밝았습니다.",
]

class SceneLoader:
    def __init__(self):
        self.scenes = {}

    def load_scene_data(self, scene_id: str):
        if scene_id not in self.scenes:
            try:
                module_name = f"story.chapter0.{scene_id}"
                scene_module = importlib.import_module(module_name)
                # 복사해서 저장하여 원본 데이터가 수정되지 않도록 함
                self.scenes[scene_id] = scene_module.SCENE.copy()
                self.scenes[scene_id]["keywords"] = scene_module.SCENE["keywords"].copy()
            except ImportError as e:
                print(f"Error loading scene {scene_id}: {e}")
                return None
        return self.scenes[scene_id]

class Game:
    def __init__(self, ui_manager: UIManager, scene_loader: SceneLoader, inventory: Inventory, test_runner: TestRunner):
        self.ui = ui_manager
        Entity.set_ui_manager(self.ui)
        self.scene_loader = scene_loader
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.user_input.onkeypress = self._handle_enter
        self.submit_button.onclick = self._handle_click
        self.inventory = inventory
        self.health = 100.0
        self.max_health = 100.0
        self.current_scene_id = None
        self.game_started = False
        self.scene_states = {}
        self.test_runner = test_runner
        self.test_runner.set_game(self)
        self._initialize_game()

    def _initialize_game(self):
        self.user_input.disabled = True
        self.submit_button.disabled = True
        self.ui.set_location_name("어둠 속")
        self.ui.update_sight_status({})
        self.ui.update_inventory_status(self.inventory.items)
        asyncio.ensure_future(self.run_intro())

    async def run_intro(self):
        for paragraph in INTRO_TEXT:
            self.ui.print_narrative(paragraph, is_markdown=True)
            await asyncio.sleep(0.5)
        self.ui.print_system_message(f"`{CMD_START}`를 입력하면 눈을 뜹니다...")
        self.user_input.disabled = False
        self.submit_button.disabled = False
        self.user_input.focus()

    def _start_game(self):
        self.game_started = True
        self.health = 15.0
        self._load_scene("scene0")

    def _load_scene(self, scene_id: str):
        self.current_scene_id = scene_id
        scene_data = self.scene_loader.load_scene_data(scene_id)
        if not scene_data:
            self.ui.print_system_message(f"오류: 장면({scene_id})을 불러올 수 없습니다.")
            return

        self.ui.set_location_name(scene_data["name"])
        self.ui.update_health_status(self.health, self.max_health)
        self.ui.print_narrative(scene_data["initial_text"], is_markdown=True)
        self.ui.update_sight_status(scene_data["keywords"])

        if scene_id == "scene0":
            self.scene_states["scene0"] = {"look_around_tutorial_shown": False}
            self.ui.print_system_message("이제부터 상호작용 방식이 바뀝니다. 본문에 등장하는 특정 단어, 즉 **[키워드]**를 직접 입력하여 주변을 탐색할 수 있습니다.\n\n본문을 자세히 읽고 상호작용할 단어를 찾아 입력해 보세요. 발견한 **[키워드]**는 상단의 **시야**에 표시됩니다.\n\n예를 들어, `교수님`을 입력해볼까요?", is_markdown=True)
        elif scene_id == "scene1":
            self.scene_states["scene1"] = {
                "is_liquid_cleaned": False, 
                "trash_can_state": "initial",
                "wall_state": "initial",
                "combination_tutorial_shown": False
            }
        elif scene_id == "scene2":
            self.scene_states["scene2"] = {
                "professor_called_out": False,
                "card_returned": False
            }

    async def redisplay_scene(self):
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        scene_data = self.scene_loader.load_scene_data(self.current_scene_id)
        self.ui.print_narrative(scene_data["initial_text"], is_markdown=True)

    def _handle_click(self, event):
        content = self.user_input.value.strip()
        if not content: return
        asyncio.ensure_future(self.process_command(content))
        self.user_input.value = ""
        self.user_input.focus()

    def _handle_enter(self, event):
        if event.key == "Enter": self._handle_click(event)

    async def process_command(self, command: str):
        self.ui.print_user_log(command)
        if await self.test_runner.run_test_command(command): return

        if not self.game_started:
            if command.lower() == CMD_START.lower(): self._start_game()
            else: self.ui.print_system_message(f"`{CMD_START}`를 입력해야 합니다.")
            return

        if command.lower() in CMD_INVENTORY:
            self.inventory.show()
            return
        
        if command.lower() == CMD_LOOK_AROUND.lower():
            await self.redisplay_scene()
            return

        if self.inventory.has(command):
            self.inventory.get(command).show_description()
            return

        if '+' in command:
            parts = [p.strip().lower() for p in command.split('+')]
            if len(parts) == 2: await self.process_combination(parts[0], parts[1])
            else: self.ui.print_system_message("잘못된 조합 형식입니다. `아이템 + 대상` 형식으로 입력해주세요.")
            return

        await self.process_keyword(command)

    async def process_combination(self, part1: str, part2: str):
        scene_data = self.scene_loader.load_scene_data(self.current_scene_id)
        if not scene_data: return

        # Scene 1 조합 로직
        if self.current_scene_id == "scene1":
            # 성공 조합
            if ("컴퓨터" in part1 and part2 == "12345678") or ("컴퓨터" in part2 and part1 == "12345678"):
                self.ui.print_narrative("암호가 맞았다! 컴퓨터 화면에 메모장 파일 하나가 띄워져 있다.\n\n`시약장 비밀번호: 내 생일 (0815)`", is_markdown=True)
                scene_data["keywords"]["오래된 컴퓨터"]["state"] = "solved"
                return
            elif ("시약장" in part1 and part2 == "0815") or ("시약장" in part2 and part1 == "0815"):
                self.ui.print_narrative("철컥, 소리와 함께 **[시약장]** 문이 열렸다. 안에서 **[에탄올]** 병을 발견했다.", is_markdown=True)
                if not self.inventory.has("에탄올"): self.inventory.add(Item("에탄올", "소독 및 청소용. 마시지 마시오."))
                if "시약장" in scene_data["keywords"]: del scene_data["keywords"]["시약장"]
                self.ui.update_sight_status(scene_data["keywords"])
                return
            elif ("박스" in part1 and "법인카드" in part2) or ("박스" in part2 and "법인카드" in part1):
                if self.inventory.has("법인카드"):
                    self.ui.print_narrative("**[법인카드]** 모서리로 테이프를 잘라냅니다. 안에서 새하얀 **[실험용 랩 가운]**을 발견했습니다!", is_markdown=True)
                    scene_data["keywords"]["박스"]["state"] = "opened"
                    scene_data["keywords"]["실험용 랩 가운"] = {"type": "Object", "state": "discovered"}
                    self.ui.update_sight_status(scene_data["keywords"])
                else: self.ui.print_system_message("**주머니**에 **[법인카드]**가 없습니다.")
                return
            elif ("에탄올" in part1 and "의문의 액체" in part2) or ("에탄올" in part2 and part1 == "의문의 액체"):
                if self.inventory.has("에탄올"):
                    self.ui.print_narrative("**[에탄올]**을 붓자, 끈적한 **[의문의 액체]**가 녹아내리며 바닥이 깨끗해졌다!", is_markdown=True)
                    self.scene_states["scene1"]["is_liquid_cleaned"] = True
                    self.inventory.remove("에탄올")
                    if "의문의 액체" in scene_data["keywords"]: del scene_data["keywords"]["의문의 액체"]
                    self.ui.update_sight_status(scene_data["keywords"])
                    self.ui.print_system_message("이제 **[빗자루]**로 **[바닥]**을 청소할 수 있을 것 같다.", is_markdown=True)
                else: self.ui.print_system_message("**주머니**에 **[에탄올]**이 없습니다.")
                return
            elif ("빗자루" in part1 and "바닥" in part2) or ("빗자루" in part2 and "바닥" in part1):
                if self.scene_states["scene1"]["is_liquid_cleaned"] and self.scene_states["scene1"]["trash_can_state"] == "empty":
                    self.ui.print_narrative("깨끗해진 바닥을 **[빗자루]**로 쓸어 마무리 청소를 합니다...", is_markdown=True)
                    self._load_scene("scene2")
                elif not self.scene_states["scene1"]["is_liquid_cleaned"]:
                    self.ui.print_narrative("바닥의 끈적한 **[의문의 액체]** 때문에 **[빗자루]**질을 할 수가 없다. 저걸 먼저 어떻게든 해야 한다.", is_markdown=True)
                else:
                    self.ui.print_system_message("아직 **[쓰레기통]**이 정리되지 않은 것 같다. 마저 치우자.", is_markdown=True)
                return
            # 실패 조합 피드백
            elif "컴퓨터" in part1 or "컴퓨터" in part2: self.ui.print_system_message("잘못된 암호입니다.")
            elif "시약장" in part1 or "시약장" in part2: self.ui.print_system_message("자물쇠가 열리지 않습니다.")
            elif "바닥" in part1 or "바닥" in part2: self.ui.print_system_message("**[의문의 액체]**에 직접 사용해야 할 것 같다.", is_markdown=True)
            return
        
        # Scene 2 조합 로직
        elif self.current_scene_id == "scene2":
            if ("탑승구" in part1 and "스패너" in part2) or ("탑승구" in part2 and "스패너" in part1):
                if self.inventory.has("스패너"):
                    if not self.scene_states["scene2"]["professor_called_out"]:
                        self.ui.print_narrative("**[스패너]**로 **[탑승구]**의 뻑뻑한 부분을 조이려 하자, 갑자기 교수님이 나를 부른다.", is_markdown=True)
                        self.ui.print_system_message("교수님: \"자네, **[법인카드]**는 놓고 가게!\"")
                        self.scene_states["scene2"]["professor_called_out"] = True
                    elif self.scene_states["scene2"]["card_returned"]:
                        self.ui.print_narrative("**[스패너]**로 **[탑승구]**를 단단히 조였다. 이제 정말 출발할 시간이다!", is_markdown=True)
                        self.ui.print_system_message("프롤로그가 성공적으로 마무리되었습니다. 이 게임은 여기까지 완성되었습니다. 플레이해주셔서 감사합니다!", is_markdown=True)
                        self.user_input.disabled = True
                        self.submit_button.disabled = True
                    else:
                        self.ui.print_system_message("교수님이 **[법인카드]**를 놓고 가라고 한다. **[교수님]**에게 **[법인카드]**를 전달해야 할 것 같다.", is_markdown=True)
                else: self.ui.print_system_message("**주머니**에 **[스패너]**가 없습니다. **[탑승구]**를 조일 수 없습니다.", is_markdown=True)
                return
            elif ("교수님" in part1 and "법인카드" in part2) or ("교수님" in part2 and "법인카드" in part1):
                if self.scene_states["scene2"]["professor_called_out"] and not self.scene_states["scene2"]["card_returned"]:
                    if self.inventory.has("법인카드"):
                        self.ui.print_narrative("교수님께 **[법인카드]**를 건네자, 교수님은 만족스러운 표정으로 고개를 끄덕인다.", is_markdown=True)
                        self.inventory.remove("법인카드")
                        self.scene_states["scene2"]["card_returned"] = True
                        self.ui.print_system_message("이제 **[탑승구]**를 마저 조여야 할 것 같다.", is_markdown=True)
                    else: self.ui.print_system_message("**주머니**에 **[법인카드]**가 없습니다.", is_markdown=True)
                else: self.ui.print_system_message("지금은 **[교수님]**에게 **[법인카드]**를 전달할 필요가 없습니다.", is_markdown=True)
                return

        self.ui.print_system_message("아무 일도 일어나지 않았습니다.")

    async def process_keyword(self, command: str):
        cmd_lower = command.lower()
        scene_data = self.scene_loader.load_scene_data(self.current_scene_id)
        if not scene_data: return

        if cmd_lower == "법인카드":
            if self.inventory.has("법인카드"): self.inventory.get("법인카드").show_description()
            elif self.current_scene_id == "scene0":
                self.ui.print_system_message("**[법인카드]**를 발견하여 **주머니**에 추가합니다.", is_markdown=True)
                self.ui.print_system_message("어떤 아이템은 이렇게 **주머니**에 보관할 수 있습니다.", is_markdown=True)
                item = Item("법인카드", "긁히지는 않지만 날카로워서 무기나 도구로 쓸 수 있습니다.")
                self.inventory.add(item, silent=True)
                item.show_description()
                if "법인카드" in scene_data["keywords"]: del scene_data["keywords"]["법인카드"]
                self.ui.update_inventory_status(self.inventory.items)
                self.ui.update_sight_status(scene_data["keywords"])
            return

        scene_keywords = scene_data["keywords"]
        for keyword_name, keyword_data in scene_keywords.items():
            is_alias = keyword_data.get("type") == "Alias"
            target_name = keyword_data.get("target", "").lower()
            
            if cmd_lower == keyword_name.lower() or (is_alias and cmd_lower == target_name):
                original_keyword_name = target_name if is_alias else keyword_name
                original_keyword_data = scene_keywords[original_keyword_name] if is_alias else keyword_data

                if original_keyword_data["state"] == "hidden":
                    original_keyword_data["state"] = "discovered"
                    self.ui.update_sight_status(scene_keywords)
                    self.ui.print_system_message(f"**[{original_keyword_name}]**{get_josa(original_keyword_name, '을/를')} 발견하여 **시야**에 추가합니다.", is_markdown=True)

                if self.current_scene_id == "scene0":
                    if original_keyword_name == "교수님":
                        self.health -= 1
                        self.ui.update_health_status(self.health, self.max_health)
                        self.ui.print_narrative("뭘 꾸물거려? 빨리 가서 청소 안 하고! 이번 학기 졸업하기 싫나?", is_markdown=True)
                        if not self.scene_states['scene0']['look_around_tutorial_shown']:
                            self.ui.print_system_message("막혔을 때는 `둘러보기`를 입력하여 주변을 다시 살필 수 있습니다.", is_markdown=True)
                            self.scene_states['scene0']['look_around_tutorial_shown'] = True
                    elif original_keyword_name == "문":
                        if self.inventory.has("법인카드"):
                            self.ui.print_system_message("문을 나섭니다. 새로운 장소에서는 **시야**가 초기화되지만, **주머니** 속의 물건은 그대로 유지됩니다.", is_markdown=True)
                            self._load_scene("scene1")
                        else: self.ui.print_system_message("이 문으로 나갈 수 있을 것 같다. 하지만 아직 무언가 잊은 기분이 든다.")
                    elif original_keyword_name == "논문":
                        self.health -= 0.5
                        self.ui.update_health_status(self.health, self.max_health)
                        self.ui.print_narrative("읽어야 할 논문이 산더미처럼 쌓여있다. 보기만 해도 숨이 막힌다.", is_markdown=True)
                    elif original_keyword_name == "책상": self.ui.print_narrative("교수님의 책상이다. 각종 서류와 논문이 어지럽게 널려있다.", is_markdown=True)
                    elif original_keyword_name == "안경알": self.ui.print_narrative("교수님의 안경알이 빛을 번뜩인다. 저 너머의 눈은 웃고 있는지, 화를 내고 있는지 알 수 없다.", is_markdown=True)

                elif self.current_scene_id == "scene1":
                    if original_keyword_name == "쓰레기통":
                        state = self.scene_states["scene1"]["trash_can_state"]
                        if state == "initial":
                            self.ui.print_narrative("쓰레기통을 뒤적거리자, 먹다 남은 **[에너지바 껍질]**을 찾았다. 쓰레기 더미 아래에 무언가 더 있는 것 같다.", is_markdown=True)
                            if not self.inventory.has("에너지바 껍질"): self.inventory.add(Item("에너지바 껍질", "눅눅하고 비어있다."))
                            self.ui.print_system_message("`쓰레기통`을 다시 한번 입력해 보세요.", is_markdown=True)
                            self.scene_states["scene1"]["trash_can_state"] = "searched_once"
                        elif state == "searched_once":
                            self.ui.print_narrative("다시 한번 쓰레기통을 뒤지자, 깊숙한 곳에서 녹슨 **[스패너]**를 발견했다. 이제 쓰레기통은 완전히 비었다.", is_markdown=True)
                            if not self.inventory.has("스패너"): self.inventory.add(Item("스패너", "녹슬었지만 쓸만해 보인다."))
                            self.scene_states["scene1"]["trash_can_state"] = "empty"
                        elif state == "empty": self.ui.print_narrative("텅 빈 쓰레기통이다. 더는 아무것도 나오지 않는다.", is_markdown=True)
                    elif original_keyword_name == "박스":
                        if original_keyword_data.get("state") == "opened": self.ui.print_narrative("안에는 아무것도 없는 빈 박스다.", is_markdown=True)
                        else:
                            self.ui.print_narrative("테이프로 칭칭 감겨 있다. 손톱으로는 뜯을 수 없을 것 같다. 날카로운 게 필요하다.", is_markdown=True)
                            if not self.scene_states["scene1"]["combination_tutorial_shown"]:
                                self.ui.print_system_message("새로운 상호작용을 위해 `+` 기호를 사용할 수 있습니다. **주머니**의 아이템과 **시야**의 **[키워드]**를 조합해 보세요. 아이템끼리, 혹은 키워드끼리 조합하는 것도 가능합니다.\n예시: `법인카드 + 박스`", is_markdown=True)
                                self.scene_states["scene1"]["combination_tutorial_shown"] = True
                    elif original_keyword_name == "실험용 랩 가운": self.ui.print_narrative("새하얀 랩 가운이다. 입으면 왠지 졸업에 한 발짝 다가간 기분이 든다.", is_markdown=True)
                    elif original_keyword_name == "빗자루": self.ui.print_narrative("평범한 빗자루다. 바닥을 청소할 수 있을 것 같다.", is_markdown=True)
                    elif original_keyword_name == "오래된 컴퓨터":
                        if original_keyword_data.get("state") != "solved":
                            self.ui.print_narrative("전원 버튼을 누르자, 잠시 팬이 돌다가 암호 입력창이 뜬다.", is_markdown=True)
                            self.ui.print_system_message("암호를 알아내어 `컴퓨터 + [비밀번호]` 형식으로 입력해야 할 것 같다.", is_markdown=True)
                        else: self.ui.print_system_message("컴퓨터 화면에는 `시약장 비밀번호: 0815` 라는 메모만 띄워져 있다.")
                    elif original_keyword_name == "시약장": self.ui.print_narrative("자물쇠가 걸려있다. 알아낸 비밀번호를 `시약장 + [비밀번호]` 형식으로 입력해보자.", is_markdown=True)
                    elif original_keyword_name == "의문의 액체": self.ui.print_narrative("바닥에 끈적하게 눌어붙은 액체다. 무슨 성분인지 알 수 없지만, 달콤한 향이 나는 것 같다. 핥아볼까?", is_markdown=True)
                    elif original_keyword_name == "바닥": self.ui.print_narrative("바닥 한쪽에 **[의문의 액체]**가 흥건하다. 끈적해서 밟고 싶지 않다.", is_markdown=True)
                    elif original_keyword_name == "벽":
                        state = self.scene_states["scene1"]["wall_state"]
                        if state == "initial":
                            self.ui.print_narrative("벽지를 자세히 보니, 구석에 작은 메모가 붙어있다.", is_markdown=True)
                            self.scene_states["scene1"]["wall_state"] = "memo_discovered"
                            scene_data["keywords"]["메모"] = {"type": "Object", "state": "hidden"}
                            self.ui.update_sight_status(scene_data["keywords"])
                            self.ui.print_system_message("시야가 넓어진 것 같다. 어떤 **[키워드]**는 또 다른 **[키워드]**로 이어지기도 합니다. `메모`를 입력해서 내용을 확인해 보세요.", is_markdown=True)
                        else: self.ui.print_narrative("구석에 작은 메모가 붙어있다.", is_markdown=True)
                    elif original_keyword_name == "메모": self.ui.print_narrative("벽에 붙어있는 메모에는 '컴퓨터 비밀번호: 1에서 시작하고 8로 끝나는 여덟자리 숫자' 라고 적혀있다.", is_markdown=True)
                    elif original_keyword_name == "문": self.ui.print_narrative("이미 끔찍한 곳에 와있는데, 굳이 돌아갈 필요는 없어 보인다.", is_markdown=True)

                elif self.current_scene_id == "scene2":
                    if original_keyword_name == "교수님":
                        if self.scene_states["scene2"]["professor_called_out"] and not self.scene_states["scene2"]["card_returned"]:
                            self.ui.print_narrative("교수님: \"**[법인카드]**는 놓고 가게!\" 교수님이 나를 빤히 쳐다본다.", is_markdown=True)
                        elif self.scene_states["scene2"]["card_returned"]:
                            self.ui.print_narrative("교수님은 이미 **[법인카드]**를 받아갔다. 이제 **[탑승구]**를 조이는 일만 남았다.", is_markdown=True)
                        else:
                            self.ui.print_narrative("교수님: \"뭘 꾸물거려? 어서 **[탑승구]**로 들어가! 아, 그리고 그거 좀 뻑뻑하던데, 알아서 잘 조이고. 공대생이 그정돈 하겠지?\"", is_markdown=True)
                    elif original_keyword_name == "MK-II":
                        self.ui.print_narrative("교수님의 역작 **[MK-II]**다. 초공간 양자 전송 장치라는데, 전선 마감이 청테이프인 것이 불안하다. **[탑승구]** 쪽 경첩이 덜 조여진 것처럼 보인다.", is_markdown=True)
                        if self.inventory.has("스패너"): self.ui.print_system_message("**[스패너]**로 대충 고쳐볼까 했지만, 더 망가뜨릴 것 같다.", is_markdown=True)
                    elif original_keyword_name == "탑승구": self.ui.print_narrative("육중한 해치다. 경첩이 헐거워 제대로 닫히지 않을 것 같다. **주머니**에 있는 **[스패너]**로 조이면 될 것 같다.", is_markdown=True)
                    elif original_keyword_name == "콘센트": self.ui.print_narrative("벽에 꽂힌 **[MK-II]**의 **[콘센트]**다. 헐거워 보이지만, 건드리면 큰일 날 것 같다.", is_markdown=True)
                    elif original_keyword_name == "전선": self.ui.print_narrative("청테이프로 대충 감아놓은 **[전선]**이다. 교수님의 공학적 감각은 일반인의 상식을 뛰어넘는다.", is_markdown=True)

                return
        
        josa = get_josa(command, "으로는/로는")
        self.ui.print_system_message(f"'{command}'{josa} 아무것도 할 수 없습니다.")
