import asyncio
from pyscript import document

from ui import UIManager
from entity import Entity, Item, Inventory
from scene_manager import SceneFactory, SceneManager
from test import TestRunner

# --- 장면 클래스와 데이터 임포트 ---
from story.chapter0.scene0 import Scene0
from story.chapter0.scene1 import Scene1
from story.chapter0.scene2 import Scene2


# --- 상수 정의 ---
CMD_INVENTORY = ["주머니"]
CMD_START = "일어나기"
CMD_LOOK_AROUND = "둘러보기"

# --- 게임 데이터 ---
INTRO_TEXT = [
    "당신은 10년차 대학원생입니다.\n...아니, 사실 '학생'이라 불리기엔 너무 늙었고, '연구원'이라 불리기엔 통장에 찍히는 돈이 너무 적습니다.",
    "동기들은 5년 전에 모두 탈출했습니다. 대기업 과장, 스타트업 대표...\n하지만 당신은 아직 이곳에 남아있습니다.",
    '왜냐고요?\n"자네, 이번 데이터만 잘 나오면 졸업 시켜주겠네."\n매 학기 반복되는 그 달콤한 거짓말. 희망 고문.',
    "당신의 몸은 커피와 핫식스로 이루어져 있고,\n당신의 영혼은 이미 연구실 서버실 어딘가에 저당 잡혔습니다.",
    "그리고 오늘...\n드디어 운명의 날이 밝았습니다.",
]


class Game:
    """
    게임의 주요 로직을 관리하고, 각 컴포넌트를 초기화하고 연결합니다.
    (Composition Root 역할)
    """

    def __init__(self, ui_manager: UIManager, inventory: Inventory, test_runner: TestRunner):
        # --- 의존성 주입 ---
        self.ui = ui_manager
        self.inventory = inventory
        self.test_runner = test_runner
        Entity.set_ui_manager(self.ui)  # Entity 클래스에 UI 매니저 설정

        # --- 컴포넌트 생성 및 연결 ---
        scene_factory = self._create_and_register_scenes()
        self.scene_manager = SceneManager(scene_factory, self.ui)

        # --- HTML 요소 바인딩 ---
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.user_input.onkeypress = self._handle_enter
        self.submit_button.onclick = self._handle_click

        # --- 게임 상태 초기화 ---
        self.health = 100.0
        self.max_health = 100.0
        self.current_scene_id: str | None = None  # SceneManager가 관리하지만, 기존 로직 유지를 위해 남겨둠
        self.game_started = False

        self.test_runner.set_game(self)
        self._initialize_game_ui()

    def _create_and_register_scenes(self) -> SceneFactory:
        """SceneFactory를 생성하고 모든 장면을 등록합니다."""
        factory = SceneFactory(self, self.ui, self.inventory)

        # 장면에 필요한 모든 클래스와 데이터를 팩토리에 등록
        factory.register_scene("scene0", Scene0, Scene0.DATA)
        factory.register_scene("scene1", Scene1, Scene1.DATA)
        factory.register_scene("scene2", Scene2, Scene2.DATA)

        return factory

    def _initialize_game_ui(self):
        """게임 시작 전 UI를 초기화합니다."""
        self.user_input.disabled = True
        self.submit_button.disabled = True
        self.ui.set_location_name("어둠 속")
        self.ui.update_sight_status({})
        self.ui.update_inventory_status(self.inventory.items)
        asyncio.ensure_future(self.run_intro())

    async def run_intro(self):
        """게임 인트로를 비동기적으로 실행합니다."""
        for paragraph in INTRO_TEXT:
            self.ui.print_narrative(paragraph, is_markdown=True)
            await asyncio.sleep(0.5)
        self.ui.print_system_message(f"`{CMD_START}`를 입력하면 눈을 뜹니다...")
        self.user_input.disabled = False
        self.submit_button.disabled = False
        self.user_input.focus()

    def _start_game(self):
        """게임의 첫 장면을 시작합니다."""
        self.game_started = True
        self.health = 15.0  # 기존 로직 유지
        self.update_health_status()
        self.scene_manager.switch_scene("scene0")  # 첫 장면 ID

    def update_health_status(self):
        """UI의 체력 상태를 업데이트합니다."""
        self.ui.update_health_status(self.health, self.max_health)

    def _handle_click(self, event):
        """입력 버튼 클릭 이벤트를 처리합니다."""
        content = self.user_input.value.strip()
        if not content:
            return
        asyncio.ensure_future(self.process_command(content))
        self.user_input.value = ""
        self.user_input.focus()

    def _handle_enter(self, event):
        """Enter 키 입력 이벤트를 처리합니다."""
        if event.key == "Enter":
            self._handle_click(event)

    async def process_command(self, command: str):
        """사용자 입력을 받아 적절한 핸들러로 전달합니다."""
        self.ui.print_user_log(command)
        if await self.test_runner.run_test_command(command):
            return

        # 게임 시작 전 명령어 처리
        if not self.game_started:
            # SceneManager가 current_scene이 없을 때 '일어나기'를 처리함
            await self.scene_manager.process_command(command)
            return

        # 공용 명령어 처리
        cmd_lower = command.lower()
        if cmd_lower in CMD_INVENTORY:
            self.inventory.show()
            return
        if cmd_lower == CMD_LOOK_AROUND.lower():
            self.scene_manager.redisplay_current_scene()
            return

        # 아이템 설명 보기
        if self.inventory.has(cmd_lower):
            self.inventory.get(cmd_lower).show_description()
            return

        # 그 외 모든 명령어는 SceneManager를 통해 현재 장면에 위임
        await self.scene_manager.process_command(command)
