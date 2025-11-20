import asyncio

from const import CommandType, SceneID  # 상수를 사용하기 위해 임포트
from entity import Entity, Inventory
from pyscript import document
from scene import Scene
from scene_manager import SceneFactory, SceneManager

# --- 장면 클래스와 데이터 임포트 ---
# 데이터 파일 임포트
from story.chapter0 import CH0_SCENE0_DATA, CH0_SCENE1_DATA, CH0_SCENE2_DATA
from test import TestRunner
from ui import UIManager

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
    이 클래스는 게임의 전체적인 흐름을 제어하는 Composition Root 역할을 합니다.
    """

    def __init__(self, ui_manager: UIManager, inventory: Inventory, test_runner: TestRunner):
        """
        Game 클래스의 생성자입니다. 필요한 의존성을 주입받고 게임 컴포넌트를 초기화합니다.

        Args:
            ui_manager (UIManager): 사용자 인터페이스 관리를 위한 객체.
            inventory (Inventory): 플레이어의 아이템 인벤토리 관리를 위한 객체.
            test_runner (TestRunner): 테스트 명령 처리를 위한 객체.
        """
        # --- 의존성 주입 ---
        # 외부에서 주입받은 객체들을 내부 필드로 저장합니다.
        self.ui = ui_manager
        self.inventory = inventory
        self.test_runner = test_runner
        # 모든 Entity 객체가 UI 매니저를 사용할 수 있도록 설정합니다.
        Entity.set_ui_manager(self.ui)

        # --- 컴포넌트 생성 및 연결 ---
        # SceneFactory를 생성하고 모든 장면 데이터를 등록합니다.
        scene_factory = self._create_and_register_scenes()
        # SceneManager를 초기화하여 장면 전환 및 관리를 담당하게 합니다.
        self.scene_manager = SceneManager(scene_factory, self.ui)

        # --- HTML 요소 바인딩 ---
        # HTML 문서에서 사용자 입력 필드와 제출 버튼 요소를 가져옵니다.
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        # Enter 키 입력과 버튼 클릭 이벤트에 핸들러를 연결합니다.
        self.user_input.onkeypress = self._handle_enter
        self.submit_button.onclick = self._handle_click

        # --- 게임 상태 초기화 ---
        # 게임 시작 여부를 나타내는 플래그입니다.
        self.game_started = False

        # TestRunner에 현재 게임 인스턴스를 설정합니다.
        self.test_runner.set_game(self)
        # 게임 UI를 초기 상태로 설정하고 인트로를 시작합니다.
        self._initialize_game_ui()

    def _create_and_register_scenes(self) -> SceneFactory:
        """
        SceneFactory를 생성하고 게임 내 모든 장면 데이터를 등록합니다.

        Returns:
            SceneFactory: 모든 장면이 등록된 SceneFactory 객체.
        """
        # 게임 인스턴스, UI 매니저, 인벤토리를 사용하여 SceneFactory를 초기화합니다.
        factory = SceneFactory(self, self.ui, self.inventory)

        # 각 장면 ID에 해당하는 장면 클래스와 데이터를 팩토리에 등록합니다.
        factory.register_scene(SceneID.CH0_SCENE0, Scene, CH0_SCENE0_DATA)
        factory.register_scene(SceneID.CH0_SCENE1, Scene, CH0_SCENE1_DATA)
        factory.register_scene(SceneID.CH0_SCENE2, Scene, CH0_SCENE2_DATA)

        return factory

    def _initialize_game_ui(self):
        """
        게임 시작 전 UI 요소를 초기 상태로 설정합니다.
        사용자 입력 비활성화, 초기 위치 설정, 인벤토리 업데이트 등을 수행합니다.
        """
        # 사용자 입력 필드와 버튼을 비활성화하여 인트로 중 입력을 막습니다.
        self.user_input.disabled = True
        self.submit_button.disabled = True
        # 초기 게임 위치 이름을 설정합니다.
        self.ui.set_location_name("어둠 속")
        # 시야 상태와 인벤토리 상태를 초기화하여 UI에 반영합니다.
        self.ui.update_sight_status({})
        self.ui.update_inventory_status(self.inventory.items)
        # 비동기적으로 인트로 텍스트를 실행합니다.
        asyncio.ensure_future(self.run_intro())

    async def run_intro(self):
        """
        게임 시작 시 인트로 텍스트를 순차적으로 출력합니다.
        각 문단 사이에 잠시 대기 시간을 두어 읽기 편하게 합니다.
        """
        # 정의된 인트로 텍스트의 각 문단을 출력합니다.
        for paragraph in INTRO_TEXT:
            self.ui.print_narrative(paragraph, is_markdown=True)
            await asyncio.sleep(0.5)  # 각 문단 출력 후 0.5초 대기

        # 인트로가 끝난 후 사용자에게 게임 시작 명령을 안내합니다.
        self.ui.print_system_message(f"`{CommandType.WAKE_UP}`를 입력하면 눈을 뜹니다...")
        # 사용자 입력 필드와 버튼을 다시 활성화합니다.
        self.user_input.disabled = False
        self.submit_button.disabled = False
        # 사용자 입력 필드에 포커스를 줍니다.
        self.user_input.focus()

    def start_game(self):
        """
        게임을 실제로 시작하고 첫 번째 장면으로 전환합니다.
        """
        self.game_started = True  # 게임 시작 플래그를 True로 설정합니다.
        self.scene_manager.switch_scene(SceneID.CH0_SCENE0)  # 첫 장면으로 전환합니다.

    def _handle_click(self, event):
        """
        입력 버튼 클릭 이벤트를 처리합니다.
        사용자 입력 값을 가져와 처리하고 입력 필드를 초기화합니다.
        """
        # 사용자 입력 필드의 값을 가져와 앞뒤 공백을 제거합니다.
        content = self.user_input.value.strip()
        if not content:  # 입력 내용이 없으면 아무것도 하지 않습니다.
            return
        # 비동기적으로 명령을 처리합니다.
        asyncio.ensure_future(self.process_command(content))
        self.user_input.value = ""  # 입력 필드를 비웁니다.
        self.user_input.focus()  # 입력 필드에 다시 포커스를 줍니다.

    def _handle_enter(self, event):
        """
        Enter 키 입력 이벤트를 처리합니다.
        Enter 키가 눌리면 클릭 이벤트와 동일하게 처리합니다.
        """
        if event.key == "Enter":  # 눌린 키가 Enter인지 확인합니다.
            self._handle_click(event)  # _handle_click 메서드를 호출하여 명령을 처리합니다.

    async def process_command(self, command: str):
        """
        사용자로부터 입력받은 명령을 처리합니다.
        테스트 명령, 게임 시작 전 명령, 인벤토리/둘러보기 명령, 아이템 설명 보기, 장면 명령 등을 처리합니다.

        Args:
            command (str): 사용자가 입력한 명령 문자열.
        """
        self.ui.print_user_log(command)  # 사용자가 입력한 명령을 UI에 출력합니다.

        # 테스트 명령이 있는지 확인하고 처리합니다.
        if await self.test_runner.run_test_command(command):
            return  # 테스트 명령이 처리되었으면 더 이상 진행하지 않습니다.

        # 게임이 아직 시작되지 않은 상태(인트로 중)의 명령을 처리합니다.
        if not self.game_started:
            await self.scene_manager.process_command(command)
            return

        cmd_lower = command.lower()  # 명령어를 소문자로 변환하여 비교에 용이하게 합니다.

        # 인벤토리 명령 처리 (현재는 아무것도 하지 않음, 인벤토리 UI는 자동으로 업데이트됨)
        if cmd_lower == CommandType.INVENTORY:
            # 인벤토리 명령은 현재 별도의 로직 없이 UI 업데이트만으로 충분합니다.
            pass

        # 둘러보기 명령 처리
        if cmd_lower == CommandType.LOOK_AROUND:
            self.scene_manager.redisplay_current_scene()  # 현재 장면의 텍스트를 다시 출력합니다.
            return

        # 명령어가 인벤토리 아이템 이름과 일치하는지 확인하고 설명을 보여줍니다.
        if self.inventory.has(cmd_lower):
            self.inventory.get(cmd_lower).show_description()  # 해당 아이템의 설명을 UI에 출력합니다.
            return

        # 위의 모든 명령에 해당하지 않으면 현재 장면의 명령 처리기로 전달합니다.
        await self.scene_manager.process_command(command)
