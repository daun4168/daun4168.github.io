import asyncio
from pyscript import document
from ui import UIManager
from entity import Entity, Item, Bag

# --- 게임 데이터 ---
SCENES = {
    "scene_0": {
        "name": "교수님 오피스",
        "initial_text": "자네, 이번 주말에 뭐 하나? 아, 물어본 건 아냐. 할 일 없지? 연구실 제2섹터가 너무 더러워서 실험 장비를 들일 수가 없네. 싹 치워놔. 그는 책상 위에 툭 던져져 있는 법인카드를 턱짓으로 가리켰다. 다 챙겼으면 뒤에 있는 문으로 나가서 바로 시작해.",
        "keywords": {
            "교수님": {
                "type": "Interaction", "display_name": "[교수님]",
                "reaction": "교수님이 재촉합니다. '뭘 꾸물거려? 빨리 가서 청소 안 하고!'"
            },
            "법인카드": {
                "type": "Item", "display_name": "[법인카드]",
                "reaction": "법인카드를 챙겼습니다. 한도 초과지만 날카로워서 쓸만합니다.",
                "description": "한도 초과된 카드. 날카로운 모서리를 가지고 있다."
            },
            "문": {
                "type": "Portal", "display_name": "[문]",
                "reaction": "연구실로 이동합니다...",
                "next_scene": "scene_1",
                "condition": {"item": "법인카드", "message": "교수님이 주신 법인카드를 챙기지 않으면 문을 열 수 없을 것 같다."}
            }
        }
    },
    "scene_1": {
        "name": "제 2 연구실 (청소 전)",
        "initial_text": "쾌퀴한 곰팡이 냄새. 이곳은 돼지우리인가 연구실인가. 구석에는 쓰레기통이 넘칠 듯이 차 있고, 벽면에는 박스들이 산더미처럼 쌓여 있다. 바닥에 굴러다니는 빗자루를 보니 한숨부터 나온다.",
        "keywords": {
            "쓰레기통": {
                "type": "Item_Container", "display_name": "[쓰레기통]",
                "reaction": "쓰레기통을 뒤져 쓸만한 [스패너]와 [에너지바 껍질]을 챙겼습니다.",
                "items": [
                    {"name": "스패너", "description": "녹슨 스패너. 어딘가에 쓸 수 있을 것 같다."},
                    {"name": "에너지바 껍질", "description": "끈적한 에너지바 껍질."}
                ]
            },
            "박스": {
                "type": "Interaction", "display_name": "[박스]",
                "condition": {"item": "법인카드", "yes": "법인카드로 테이프를 뜯고 [실험용 랩 가운]을 획득했습니다!", "no": "테이프가 너무 단단해서 손톱으로는 뜯을 수 없습니다. 날카로운 게 필요합니다."},
                "effect": {"item": "실험용 랩 가운", "description": "깨끗한 랩 가운. 입으면 왠지 기분이 좋아진다.", "hp_change": 5}
            },
            "빗자루": {
                "type": "Trigger", "display_name": "[빗자루]",
                "reaction": "청소를 시작합니다. 먼지가 풀풀 날립니다... (청소 완료)",
                "next_scene": "scene_2"
            }
        }
    },
    "scene_2": {
        "name": "제 2 연구실 (청소 후/사건 발생)",
        "initial_text": "청소를 마치자마자 교수님이 거대한 기계를 들고 들어왔습니다. \"자, 이게 내 역작 MK-II야. 배송비를 아껴줄 양자 전송 장치지.\" 교수는 전선을 대충 연결하더니 나를 쳐다봅니다. \"테스트하게 저기 탑승구로 들어가.\"",
        "keywords": {
            "교수님": {"type": "Interaction", "reaction": "잔말 말고 들어가! 논문 심사 받고 싶으면!"},
            "MK-II": {"type": "Interaction", "aliases": ["기계"], "reaction": "위태로워 보이는 기계입니다. 전선 마감이 엉망입니다."},
            "탑승구": {
                "type": "End_Prologue", "reaction": "어쩔 수 없이 탑승구로 들어갑니다...",
                "final_text": "위이이잉- 펑! ...좌표 계산 오류..."
            }
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

        self.game_started = False
        self.hp = 0
        self.bag = Bag()
        self.current_scene_id = None
        self.discovered_keywords = []

        self.ui.print_narrative(
            "**대학원생의 생존기**\n\n"
            "게임을 시작하려면 `시작`을 입력하세요.",
            is_markdown=True
        )

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

        if not self.game_started:
            if command.lower() == "시작":
                self.start_game()
            else:
                self.ui.print_system_message("게임을 시작하려면 `시작`을 입력하세요.")
            return

        scene_data = SCENES[self.current_scene_id]
        command_lower = command.lower()
        
        found_keyword = None
        for target, data in scene_data["keywords"].items():
            aliases = data.get("aliases", [])
            if target.lower() in command_lower or any(alias.lower() in command_lower for alias in aliases):
                found_keyword = target
                break

        if found_keyword:
            self._process_keyword(found_keyword, scene_data["keywords"][found_keyword])
        else:
            self.ui.print_system_message("그건 논문에 도움이 안 됩니다.")
        
        self._update_ui()

    def start_game(self):
        self.game_started = True
        self.hp = 10
        self.bag = Bag()
        self.load_scene("scene_0")

    def load_scene(self, scene_id: str):
        self.current_scene_id = scene_id
        self.discovered_keywords = []
        scene_data = SCENES[scene_id]

        self.ui.clear_output()
        self.ui.print_narrative(scene_data["initial_text"])
        self._update_ui()

    def _update_ui(self):
        scene_data = SCENES[self.current_scene_id]
        
        masked_keywords = []
        for target, data in scene_data["keywords"].items():
            display_name = data.get("display_name")
            if display_name:
                 masked_keywords.append(display_name if target in self.discovered_keywords else "[???]")

        self.ui.update_status(scene_data["name"], self.hp, masked_keywords)
        self.ui.update_inventory(self.bag.get_item_names())

    def _process_keyword(self, keyword: str, data: dict):
        # 키워드 첫 발견 시 처리
        if keyword not in self.discovered_keywords:
            self.discovered_keywords.append(keyword)

        # 반응 텍스트 출력
        if "reaction" in data:
            self.ui.print_narrative(data["reaction"])

        keyword_type = data["type"]

        if keyword_type == "Item":
            if not self.bag.has(keyword):
                item = Item(keyword, data["description"])
                self.bag.add(item)
                # 아이템 획득 후 지역 키워드에서 제거되도록 처리
                if "display_name" in data:
                    data.pop("display_name")

        elif keyword_type == "Portal":
            condition = data.get("condition")
            if condition:
                if not self.bag.has(condition["item"]):
                    self.ui.print_system_message(condition["message"])
                    return
            self.load_scene(data["next_scene"])

        elif keyword_type == "Item_Container":
            for item_data in data.get("items", []):
                if not self.bag.has(item_data["name"]):
                    item = Item(item_data["name"], item_data["description"])
                    self.bag.add(item)
            if "display_name" in data:
                data.pop("display_name")


        elif keyword_type == "Interaction":
            condition = data.get("condition")
            if condition:
                if self.bag.has(condition["item"]):
                    self.ui.print_narrative(condition["yes"])
                    effect = data.get("effect")
                    if effect and not self.bag.has(effect["item"]):
                        item = Item(effect["item"], effect["description"])
                        self.bag.add(item)
                        self.hp += effect.get("hp_change", 0)
                        if "display_name" in data:
                            data.pop("display_name")
                else:
                    self.ui.print_narrative(condition["no"])
        
        elif keyword_type == "Trigger":
            self.load_scene(data["next_scene"])

        elif keyword_type == "End_Prologue":
            asyncio.ensure_future(self._end_prologue(data["final_text"]))

    async def _end_prologue(self, final_text: str):
        self.ui.print_narrative(final_text)
        # 여기서 화면 암전 효과 등을 추가할 수 있습니다.
        # 예: document.body.style.backgroundColor = "black"
        await asyncio.sleep(2)
        self.ui.clear_output()
        self.ui.print_narrative("Chapter 1. 무인도에서 눈을 뜨다. (Coming Soon)")
        self.user_input.disabled = True
        self.submit_button.disabled = True
