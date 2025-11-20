import asyncio
from pyscript import document

from ui import UIManager
from entity import Entity, Item, Inventory
from scene_manager import SceneFactory, SceneManager
from test import TestRunner
from const import SceneID, CommandType  # 상수를 사용하기 위해 임포트

# --- 장면 클래스와 데이터 임포트 ---
# 데이터 파일 임포트
from story.chapter0 import CH0_SCENE0_DATA, CH0_SCENE1_DATA, CH0_SCENE2_DATA
from scene import Scene

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
        self.game_started = False

        self.test_runner.set_game(self)
        self._initialize_game_ui()

    def _create_and_register_scenes(self) -> SceneFactory:
        factory = SceneFactory(self, self.ui, self.inventory)

        factory.register_scene(SceneID.CH0_SCENE0, Scene, CH0_SCENE0_DATA)
        factory.register_scene(SceneID.CH0_SCENE1, Scene, CH0_SCENE1_DATA)
        factory.register_scene(SceneID.CH0_SCENE2, Scene, CH0_SCENE2_DATA)

        return factory

    def _initialize_game_ui(self):
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

        # CommandType.WAKE_UP 사용
        self.ui.print_system_message(f"`{CommandType.WAKE_UP}`를 입력하면 눈을 뜹니다...")
        self.user_input.disabled = False
        self.submit_button.disabled = False
        self.user_input.focus()

    def start_game(self):
        self.game_started = True
        self.scene_manager.switch_scene(SceneID.CH0_SCENE0)

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
        self.ui.print_user_log(command)
        if await self.test_runner.run_test_command(command):
            return

        if not self.game_started:
            await self.scene_manager.process_command(command)
            return

        cmd_lower = command.lower()

        # CommandType Enum 사용
        if cmd_lower == CommandType.INVENTORY:
            pass

        if cmd_lower == CommandType.LOOK_AROUND:
            self.scene_manager.redisplay_current_scene()
            return

        if self.inventory.has(cmd_lower):
            self.inventory.get(cmd_lower).show_description()
            return

        await self.scene_manager.process_command(command)
