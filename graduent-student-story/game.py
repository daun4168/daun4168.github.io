import asyncio
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

SCENES = {
    "scene0": {
        "name": "교수님 오피스",
        "initial_text": "눈을 뜨자 익숙한 풍경이 보인다. 책상 위에 쌓인 논문 탑, 그리고 그 뒤에서 번뜩이는 안경알.\n\n\"자네, 정신이 드나? 서서 조는 기술이 아주 일취월장했어.\"\n\n교수님이 혀를 차며 나를 바라본다. 10년째 듣는 잔소리다. 타격감도 없다.\n\n\"연구실 제2섹터 청소나 하게. 외부 손님이 온다니까. 필요한 물건 있으면 저기 법인카드 가져가서 사고. 한도는 초과됐지만 포인트는 남았을 거야.\"\n\n교수는 턱짓으로 책상을 가리켰다.\n\n\"다 챙겼으면 뒤에 있는 문으로 나가. 난 사우나... 아니, 미팅 준비해야 하니까.\"",
        "keywords": {
            "교수님": {"type": "NPC", "state": "hidden"}, "법인카드": {"type": "Item", "state": "hidden"},
            "문": {"type": "Portal", "state": "hidden", "target": "scene1"}, "논문": {"type": "Object", "state": "hidden"},
            "책상": {"type": "Object", "state": "hidden"}, "안경알": {"type": "Object", "state": "hidden"}
        }
    },
    "scene1": {
        "name": "제 2 연구실",
        "initial_text": "문을 열자 퀴퀴한 곰팡이 냄새와 먼지가 뒤섞여 코를 찌른다. 이곳은 신성한 연구실인가, 고고학 발굴 현장인가.\n\n구석에는 정체를 알 수 없는 쓰레기통이 넘칠 듯이 차 있고, 벽 한쪽에는 굳게 닫힌 시약장과 낡은 박스들이 산더미처럼 쌓여 있다.\n먼지 쌓인 오래된 컴퓨터는 켜지기는 할지 의문이며, 바닥에는 정체불명의 의문의 액체가 흥건하다. 그 옆에 빗자루가 굴러다닌다.",
        "keywords": {
            "쓰레기통": {"type": "Object", "state": "hidden"}, "박스": {"type": "Object", "state": "hidden"},
            "빗자루": {"type": "Object", "state": "hidden"}, "오래된 컴퓨터": {"type": "Object", "state": "hidden"},
            "의문의 액체": {"type": "Object", "state": "hidden"}, "시약장": {"type": "Object", "state": "hidden"},
            "바닥": {"type": "Object", "state": "hidden"}, "벽": {"type": "Object", "state": "hidden"},
            "벽면": {"type": "Alias", "target": "벽"}, "문": {"type": "Object", "state": "hidden"},
            "컴퓨터": {"type": "Alias", "target": "오래된 컴퓨터"}
        }
    },
    "scene2": {
        "name": "제 2 연구실 (청소 완료)",
        "initial_text": "청소를 마치자마자 교수님이 땀을 뻘뻘 흘리며 거대한 기계를 들고 들어왔습니다.\n\n\"자, 이게 내 역작 MK-II야. 배송비를 아껴줄 초공간 양자 전송 장치지. 해외 직구 배송비가 너무 비싸서 직접 만들었어.\"\n\n교수는 전선을 대충 콘센트에 꽂더니 나를 쳐다봅니다. 기계에서 불안한 웅웅 소리가 납니다.\n\n\"테스트하게 저기 탑승구로 들어가. 자네 몸무게가 쌀 한 가마니랑 비슷하니까 딱이야.\"",
        "keywords": {
            "교수님": {"type": "NPC", "state": "hidden"}, "MK-II": {"type": "Object", "state": "hidden"},
            "탑승구": {"type": "End", "state": "hidden"}
        }
    }
}

class Game:
    def __init__(self):
        self.ui = UIManager()
        Entity.set_ui_manager(self.ui)
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.user_input.onkeypress = self._handle_enter
        self.submit_button.onclick = self._handle_click
        self.inventory = Inventory()
        self.health = 100.0
        self.max_health = 100.0
        self.current_scene_id = None
        self.game_started = False
        self.scene_states = {}
        self.test_runner = TestRunner(self)
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
        scene_data = SCENES[scene_id]
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

    async def redisplay_scene(self):
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        scene_data = SCENES[self.current_scene_id]
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
        # Scene 1 조합 로직
        if self.current_scene_id == "scene1":
            # 성공 조합
            if ("컴퓨터" in part1 and part2 == "12345678") or ("컴퓨터" in part2 and part1 == "12345678"):
                self.ui.print_narrative("암호가 맞았다! 컴퓨터 화면에 메모장 파일 하나가 띄워져 있다.\n\n`시약장 비밀번호: 내 생일 (0815)`", is_markdown=True)
                SCENES["scene1"]["keywords"]["오래된 컴퓨터"]["state"] = "solved"
                return
            elif ("시약장" in part1 and part2 == "0815") or ("시약장" in part2 and part1 == "0815"):
                self.ui.print_narrative("철컥, 소리와 함께 **[시약장]** 문이 열렸다. 안에서 **[에탄올]** 병을 발견했다.", is_markdown=True)
                if not self.inventory.has("에탄올"): self.inventory.add(Item("에탄올", "소독 및 청소용. 마시지 마시오."))
                if "시약장" in SCENES["scene1"]["keywords"]: del SCENES["scene1"]["keywords"]["시약장"]
                self.ui.update_sight_status(SCENES["scene1"]["keywords"])
                return
            elif ("박스" in part1 and "법인카드" in part2) or ("박스" in part2 and "법인카드" in part1):
                if self.inventory.has("법인카드"):
                    self.ui.print_narrative("**[법인카드]** 모서리로 테이프를 잘라냅니다. 안에서 새하얀 **[실험용 랩 가운]**을 발견했습니다!", is_markdown=True)
                    SCENES["scene1"]["keywords"]["박스"]["state"] = "opened"
                    SCENES["scene1"]["keywords"]["실험용 랩 가운"] = {"type": "Object", "state": "discovered"}
                    self.ui.update_sight_status(SCENES["scene1"]["keywords"])
                else: self.ui.print_system_message("**주머니**에 **[법인카드]**가 없습니다.")
                return
            elif ("에탄올" in part1 and "의문의 액체" in part2) or ("에탄올" in part2 and part1 == "의문의 액체"):
                if self.inventory.has("에탄올"):
                    self.ui.print_narrative("**[에탄올]**을 붓자, 끈적한 **[의문의 액체]**가 녹아내리며 바닥이 깨끗해졌다!", is_markdown=True)
                    self.scene_states["scene1"]["is_liquid_cleaned"] = True
                    self.inventory.remove("에탄올")
                    if "의문의 액체" in SCENES["scene1"]["keywords"]: del SCENES["scene1"]["keywords"]["의문의 액체"]
                    self.ui.update_sight_status(SCENES["scene1"]["keywords"])
                    self.ui.print_system_message("이제 **[빗자루]**로 **[바닥]**을 청소할 수 있을 것 같다.", is_markdown=True)
                else: self.ui.print_system_message("**주머니**에 **[에탄올]**이 없습니다.")
                return
            elif ("빗자루" in part1 and "바닥" in part2) or ("빗자루" in part2 and "바닥" in part1):
                if self.scene_states["scene1"]["is_liquid_cleaned"] and self.scene_states["scene1"]["trash_can_state"] == "empty":
                    self.ui.print_narrative("깨끗해진 바닥을 **[빗자루]**로 쓸어 마무리 청소를 합니다...", is_markdown=True)
                    await asyncio.sleep(2)
                    self._load_scene("scene2")
                elif not self.scene_states["scene1"]["is_liquid_cleaned"]:
                    self.ui.print_narrative("바닥의 끈적한 **[의문의 액체]** 때문에 **[빗자루]**질을 할 수가 없다. 저걸 먼저 어떻게든 해야 한다.", is_markdown=True)
                else:
                    self.ui.print_system_message("아직 **[쓰레기통]**이 정리되지 않은 것 같다. 마저 치우자.", is_markdown=True)
                return
            # 실패 조합 피드백
            elif "컴퓨터" in part1 or "컴퓨터" in part2:
                self.ui.print_system_message("잘못된 암호입니다.")
                return
            elif "시약장" in part1 or "시약장" in part2:
                self.ui.print_system_message("자물쇠가 열리지 않습니다.")
                return
            elif "바닥" in part1 or "바닥" in part2:
                self.ui.print_system_message("**[의문의 액체]**에 직접 사용해야 할 것 같다.", is_markdown=True)
                return

        self.ui.print_system_message("아무 일도 일어나지 않았습니다.")

    async def process_keyword(self, command: str):
        cmd_lower = command.lower()

        if cmd_lower == "법인카드":
            if self.inventory.has("법인카드"): self.inventory.get("법인카드").show_description()
            elif self.current_scene_id == "scene0":
                self.ui.print_system_message("**[법인카드]**를 발견하여 **주머니**에 추가합니다.", is_markdown=True)
                self.ui.print_system_message("어떤 아이템은 이렇게 **주머니**에 보관할 수 있습니다.", is_markdown=True)
                item = Item("법인카드", "긁히지는 않지만 날카로워서 무기나 도구로 쓸 수 있습니다.")
                self.inventory.add(item, silent=True)
                item.show_description()
                if "법인카드" in SCENES["scene0"]["keywords"]: del SCENES["scene0"]["keywords"]["법인카드"]
                self.ui.update_inventory_status(self.inventory.items)
                self.ui.update_sight_status(SCENES["scene0"]["keywords"])
            return

        scene_keywords = SCENES[self.current_scene_id]["keywords"]
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
                        elif state == "empty":
                            self.ui.print_narrative("텅 빈 쓰레기통이다. 더는 아무것도 나오지 않는다.", is_markdown=True)
                    elif original_keyword_name == "박스":
                        if original_keyword_data.get("state") == "opened":
                            self.ui.print_narrative("안에는 아무것도 없는 빈 박스다.", is_markdown=True)
                        else:
                            self.ui.print_narrative("테이프로 칭칭 감겨 있다. 손톱으로는 뜯을 수 없을 것 같다. 날카로운 게 필요하다.", is_markdown=True)
                            if not self.scene_states["scene1"]["combination_tutorial_shown"]:
                                self.ui.print_system_message("아이템을 조합하거나, 특정 대상에 아이템을 사용하여 새로운 행동을 할 수 있습니다. `+` 기호를 사용하여 두 대상을 묶어보세요.\n예시: `법인카드 + 박스`", is_markdown=True)
                                self.scene_states["scene1"]["combination_tutorial_shown"] = True
                    elif original_keyword_name == "실험용 랩 가운":
                        self.ui.print_narrative("새하얀 랩 가운이다. 입으면 왠지 졸업에 한 발짝 다가간 기분이 든다.", is_markdown=True)
                    elif original_keyword_name == "빗자루":
                        self.ui.print_narrative("평범한 빗자루다. 바닥을 청소할 수 있을 것 같다.", is_markdown=True)
                    elif original_keyword_name == "오래된 컴퓨터":
                        if original_keyword_data.get("state") != "solved":
                            self.ui.print_narrative("전원 버튼을 누르자, 잠시 팬이 돌다가 암호 입력창이 뜬다.", is_markdown=True)
                            self.ui.print_system_message("암호를 알아내어 `컴퓨터 + [비밀번호]` 형식으로 입력해야 할 것 같다.", is_markdown=True)
                        else: self.ui.print_system_message("컴퓨터 화면에는 `시약장 비밀번호: 0815` 라는 메모만 띄워져 있다.")
                    elif original_keyword_name == "시약장":
                        self.ui.print_narrative("자물쇠가 걸려있다. 알아낸 비밀번호를 `시약장 + [비밀번호]` 형식으로 입력해보자.", is_markdown=True)
                    elif original_keyword_name == "의문의 액체": self.ui.print_narrative("바닥에 끈적하게 눌어붙은 액체다. 무슨 성분인지 알 수 없지만, 달콤한 향이 나는 것 같다. 핥아볼까?", is_markdown=True)
                    elif original_keyword_name == "바닥": self.ui.print_narrative("바닥 한쪽에 **[의문의 액체]**가 흥건하다. 끈적해서 밟고 싶지 않다.", is_markdown=True)
                    elif original_keyword_name == "벽":
                        state = self.scene_states["scene1"]["wall_state"]
                        if state == "initial":
                            self.ui.print_narrative("벽지를 자세히 보니, 구석에 작은 메모가 붙어있다.", is_markdown=True)
                            self.scene_states["scene1"]["wall_state"] = "memo_discovered"
                        else:
                            self.ui.print_narrative("벽에 붙어있는 메모에는 '컴퓨터 비밀번호: 1에서 시작하고 8로 끝나는 여덟자리 숫자' 라고 적혀있다.", is_markdown=True)
                    elif original_keyword_name == "문":
                        self.ui.print_narrative("이미 끔찍한 곳에 와있는데, 굳이 돌아갈 필요는 없어 보인다.", is_markdown=True)

                return
        
        josa = get_josa(command, "으로는/로는")
        self.ui.print_system_message(f"'{command}'{josa} 아무것도 할 수 없습니다.")
