import asyncio
import copy

# const에서 KeywordState, KeywordType 추가 임포트 (필수)
from const import ChapterID, CommandType, KeywordState, KeywordType, SceneID
from entity import Entity, Inventory, Player
from pyscript import document
from scene import Scene
from scene_manager import SceneFactory, SceneManager

# --- 장면 클래스와 데이터 임포트 ---
from story.chapter0 import CH0_SCENE0_DATA, CH0_SCENE1_DATA, CH0_SCENE2_DATA
from story.chapter1 import (
    CH1_COMMON_DATA,
    CH1_SCENE0_DATA,
    CH1_SCENE1_DATA,
    CH1_SCENE2_0_DATA,
    CH1_SCENE2_1_DATA,
    CH1_SCENE2_2_DATA,
    CH1_SCENE2_3_DATA,
    CH1_SCENE2_4_DATA,
    CH1_SCENE2_5_DATA,
    CH1_SCENE2_6_DATA,
    CH1_SCENE2_7_DATA,
    CH1_SCENE3_0_DATA,
    CH1_SCENE3_1_DATA,
    CH1_SCENE3_2_DATA,
    CH1_SCENE3_3_DATA,
    CH1_SCENE3_4_DATA,
    CH1_SCENE4_0_DATA,
    CH1_SCENE5_DATA,
    CH1_SCENE6_DATA,
    CH1_SCENE7_DATA,
    CH1_SCENE8_DATA,
    CH1_SCENE9_DATA,
    CH1_SCENE10_DATA,
)
from test import TestRunner
from ui import UIManager

# [추가] 한글 초성 리스트 (유니코드 순서)
CHOSUNG_LIST = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

# --- 게임 데이터 ---
INTRO_TEXT = (
    "당신은 10년차 대학원생입니다.\n\n<br>"
    "...아니, 사실 '학생'이라 불리기엔 너무 늙었고, \n\n"
    "'연구원'이라 불리기엔 통장에 찍히는 돈이 너무 적습니다.\n\n<br>"
    "동기들은 5년 전에 모두 탈출했습니다. 대기업 과장, 스타트업 대표...\n\n"
    "하지만 당신은 아직 이곳에 남아있습니다.\n\n<br>"
    "왜냐고요?\n\n"
    '"자네, 이번 데이터만 잘 나오면 졸업 시켜주겠네."\n\n'
    "매 학기 반복되는 그 달콤한 거짓말. 희망 고문.\n\n<br>"
    "당신의 몸은 커피와 핫식스로 이루어져 있고,\n\n"
    "당신의 영혼은 이미 연구실 서버실 어딘가에 저당 잡혔습니다.\n\n<br>"
    "그리고 오늘...\n\n"
    "드디어 운명의 날이 밝았습니다.\n\n"
)


class Game:
    """
    게임의 주요 로직을 관리하고, 각 컴포넌트를 초기화하고 연결합니다.
    """

    def __init__(self, ui_manager: UIManager, inventory: Inventory, player: Player, test_runner: TestRunner):
        # --- 의존성 주입 ---
        self.ui = ui_manager
        self.inventory = inventory
        self.player = player
        self.test_runner = test_runner
        self.checkpoint_data = None
        self.pending_confirmation = None

        Entity.set_ui_manager(self.ui)

        # --- 컴포넌트 생성 및 연결 ---
        scene_factory = self._create_and_register_scenes()
        self.scene_manager = SceneManager(scene_factory, self.ui)

        # --- HTML 요소 바인딩 ---
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")

        # [히스토리 기능]
        self.command_history = []
        self.history_index = 0

        # [자동 완성 기능] 상태 변수
        self.tab_matches = []  # 현재 매칭된 후보 리스트
        self.tab_index = 0  # 현재 보여주는 후보의 인덱스
        self.original_prefix = ""  # [핵심] 사용자가 탭 누르기 전 입력했던 원본 문자열

        # 이벤트 핸들러 바인딩
        self.user_input.onkeydown = self._handle_keydown
        self.submit_button.onclick = self._handle_click

        # --- 게임 상태 초기화 ---
        self.game_started = False
        self.num_total_inputs = 0
        self.chapter_states = {ChapterID.CH1: CH1_COMMON_DATA.initial_state.copy()}

        self.test_runner.set_game(self)
        self._initialize_game_ui()

    def _create_and_register_scenes(self) -> SceneFactory:
        factory = SceneFactory(self, self.ui, self.inventory, self.player)

        # 챕터 0 씬 등록
        factory.register_scene(SceneID.CH0_SCENE0, Scene, CH0_SCENE0_DATA)
        factory.register_scene(SceneID.CH0_SCENE1, Scene, CH0_SCENE1_DATA)
        factory.register_scene(SceneID.CH0_SCENE2, Scene, CH0_SCENE2_DATA)
        # 챕터 1 씬 등록
        factory.register_scene(SceneID.CH1_SCENE0, Scene, CH1_SCENE0_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE1, Scene, CH1_SCENE1_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_0, Scene, CH1_SCENE2_0_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_1, Scene, CH1_SCENE2_1_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_2, Scene, CH1_SCENE2_2_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_3, Scene, CH1_SCENE2_3_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_4, Scene, CH1_SCENE2_4_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_5, Scene, CH1_SCENE2_5_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_6, Scene, CH1_SCENE2_6_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE2_7, Scene, CH1_SCENE2_7_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE3_0, Scene, CH1_SCENE3_0_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE3_1, Scene, CH1_SCENE3_1_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE3_2, Scene, CH1_SCENE3_2_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE3_3, Scene, CH1_SCENE3_3_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE3_4, Scene, CH1_SCENE3_4_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE4_0, Scene, CH1_SCENE4_0_DATA, CH1_COMMON_DATA)
        # factory.register_scene(SceneID.CH1_SCENE4, Scene, CH1_SCENE4_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE5, Scene, CH1_SCENE5_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE6, Scene, CH1_SCENE6_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE7, Scene, CH1_SCENE7_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE8, Scene, CH1_SCENE8_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE9, Scene, CH1_SCENE9_DATA, CH1_COMMON_DATA)
        factory.register_scene(SceneID.CH1_SCENE10, Scene, CH1_SCENE10_DATA, CH1_COMMON_DATA)

        return factory

    def _initialize_game_ui(self):
        self.user_input.disabled = True
        self.submit_button.disabled = True
        self.ui.set_location_name("어둠 속")
        self.ui.update_sight_status({})
        self.ui.update_inventory_status(self.inventory.items)
        self.ui.update_stamina_status(self.player.current_stamina, self.player.max_stamina)

        asyncio.ensure_future(self.run_intro())

    async def run_intro(self):
        self.ui.print_plain(INTRO_TEXT, is_markdown=True)

        self.ui.print_system_message(f"`{CommandType.WAKE_UP}`를 입력하면 눈을 뜹니다...")
        self.user_input.disabled = False
        self.submit_button.disabled = False
        self.user_input.focus()

    def start_game(self):
        self.game_started = True
        self.scene_manager.switch_scene(SceneID.CH0_SCENE0)

    def _handle_click(self, event):
        content = self.user_input.value.strip()
        if not content:
            return

        # 히스토리 저장
        self.command_history.append(content)
        self.history_index = len(self.command_history)

        # [자동 완성 리셋] 제출 시 초기화
        self.tab_matches = []
        self.original_prefix = ""

        asyncio.ensure_future(self.process_command(content))
        self.user_input.value = ""
        self.user_input.focus()

    def _get_autocomplete_candidates(self) -> list[str]:
        """
        자동 완성 후보군을 생성합니다.
        """
        candidates = set()
        candidates.add(CommandType.LOOK_AROUND)

        # 1. 인벤토리 아이템 추가
        for item in self.inventory.items.values():
            candidates.add(item.name)

        # 2. 현재 씬의 시야 내 키워드 추가
        current_scene = self.scene_manager.current_scene
        if current_scene:
            # [주의] scene_data 구조에 맞춰 접근
            for key, data in current_scene.scene_data.keywords.items():
                if data.type == KeywordType.ALIAS:
                    continue
                if data.state == KeywordState.DISCOVERED:
                    name = data.display_name if data.display_name else key
                    candidates.add(name)

        return list(candidates)

    def _get_chosung(self, text: str) -> str:
        """
        문자열을 받아 초성만으로 이루어진 문자열을 반환합니다.
        예: '가방' -> 'ㄱㅂ', 'User' -> 'User'
        """
        result = []
        for char in text:
            code = ord(char)
            # 한글 유니코드 범위 (가 ~ 힣) 확인
            if 0xAC00 <= code <= 0xD7A3:
                # (글자코드 - 시작코드) // (중성개수 * 종성개수) = 초성인덱스
                chosung_index = (code - 0xAC00) // 588
                result.append(CHOSUNG_LIST[chosung_index])
            else:
                result.append(char)
        return "".join(result)

    def _is_hangul_prefix_match(self, input_str: str, candidate_str: str) -> bool:
        """
        한글 입력 중간 단계(받침 미완성)를 포함하여 prefix가 일치하는지 확인합니다.
        예: '두' -> '둘러보기' (Match), '가바' -> '가방' (Match)
        """
        if len(input_str) > len(candidate_str):
            return False

        # 1. 마지막 글자를 제외한 앞부분이 정확히 일치하는지 확인
        if input_str[:-1] != candidate_str[:len(input_str) - 1]:
            return False

        # 2. 마지막 글자 비교
        last_in = input_str[-1]
        last_cand = candidate_str[len(input_str) - 1]

        # 정확히 일치하면 True (예: '둘' -> '둘러보기')
        if last_in == last_cand:
            return True

        # 3. 한글 유니코드 로직을 이용한 '초성+중성' 일치 확인
        # 입력된 마지막 글자가 받침이 없는 한글(가~힣)인지 확인
        code_in = ord(last_in)
        if 0xAC00 <= code_in <= 0xD7A3:
            # (코드 - 0xAC00) % 28 == 0 이면 종성(받침)이 없는 글자임
            if (code_in - 0xAC00) % 28 == 0:
                # 후보 글자(last_cand)가 입력 글자(last_in)로부터
                # 같은 초성+중성 그룹(0~27 범위 내)에 있는지 확인
                # 예: '두'(base) ~ '둫'(base+27) 사이에 '둘'(base+8)이 포함됨
                code_cand = ord(last_cand)
                diff = code_cand - code_in
                if 0 <= diff < 28:
                    return True

        return False

    def _handle_keydown(self, event):
        """
        키보드 입력 핸들러
        """
        key = event.key
        # [수정] Shift 키 눌림 상태를 안전하게 확인
        is_shift = getattr(event, "shiftKey", False) or getattr(event, "shift_key", False)

        # [자동 완성 로직] - Tab 키
        if key == "Tab":
            event.preventDefault()
            origin_user_input: str = self.user_input.value

            # '+' 기호 처리 (기존 코드 유지)
            idx = origin_user_input.rfind("+")
            if idx != -1:
                left = origin_user_input[:idx] + "+ "
                right = origin_user_input[idx + 1:]
            else:
                left = ""
                right = origin_user_input
            right = right.strip()

            if not self.tab_matches:
                if not right:
                    return

                candidates = self._get_autocomplete_candidates()
                self.original_prefix = right

                # [자음 검색 판단] (기존 코드 유지)
                is_chosung_search = False
                if self.original_prefix and 0x3131 <= ord(self.original_prefix[0]) <= 0x314E:
                    is_chosung_search = True

                self.tab_matches = []
                for c in candidates:
                    # [수정된 부분] 매칭 조건 3가지
                    # 1. 완전한 prefix 일치 (startswith)
                    # 2. 한글 받침 미완성 매칭 ('두' -> '둘') [NEW]
                    # 3. 초성 매칭 ('ㄷ' -> '둘')

                    if c.startswith(self.original_prefix):
                        self.tab_matches.append(c)

                    elif self._is_hangul_prefix_match(self.original_prefix, c):
                        self.tab_matches.append(c)

                    elif is_chosung_search:
                        c_chosung = self._get_chosung(c)
                        if c_chosung.startswith(self.original_prefix):
                            self.tab_matches.append(c)

                self.tab_matches.sort()
                self.tab_index = 0

            if self.tab_matches:
                match = self.tab_matches[self.tab_index]
                self.user_input.value = left + match
                if not is_shift:
                    self.tab_index = (self.tab_index + 1) % len(self.tab_matches)
                else:
                    self.tab_index = (self.tab_index - 1) % len(self.tab_matches)

            return

        # [자동 완성 리셋]
        if key not in ["Shift", "Control", "Alt", "Meta", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]:
            self.tab_matches = []
            self.original_prefix = ""

        # [IME 중복 입력 방지]
        if event.isComposing:
            return

        # [제출]
        if key == "Enter":
            event.preventDefault()
            self._handle_click(event)

        # [위쪽 화살표] -> 히스토리(기본) OR 스크롤(Shift)
        elif key == "ArrowUp":
            event.preventDefault()

            if is_shift:
                # [Shift + Up] 스크롤 올리기
                scroll_area = document.getElementById("content-scroll-area")
                if scroll_area:
                    scroll_amount = scroll_area.clientHeight * 0.66
                    scroll_area.scrollTop -= scroll_amount
            else:
                # [Up] 히스토리 이전
                if self.history_index > 0:
                    self.history_index -= 1
                    self.user_input.value = self.command_history[self.history_index]

        # [아래쪽 화살표] -> 히스토리(기본) OR 스크롤(Shift)
        elif key == "ArrowDown":
            event.preventDefault()

            if is_shift:
                # [Shift + Down] 스크롤 내리기
                scroll_area = document.getElementById("content-scroll-area")
                if scroll_area:
                    scroll_amount = scroll_area.clientHeight * 0.66
                    scroll_area.scrollTop += scroll_amount
            else:
                # [Down] 히스토리 다음
                if self.history_index < len(self.command_history) - 1:
                    self.history_index += 1
                    self.user_input.value = self.command_history[self.history_index]
                else:
                    self.history_index = len(self.command_history)
                    self.user_input.value = ""

    async def process_command(self, command: str):
        self.num_total_inputs += 1
        self.ui.print_user_log(command)

        if await self.test_runner.run_test_command(command):
            return

        if not self.game_started:
            await self.scene_manager.process_command(command)
            return

        cmd_lower = command.lower()

        if self.pending_confirmation:
            await self.scene_manager.process_confirmation(command)
            return

        if cmd_lower == CommandType.LOOK_AROUND:
            self.scene_manager.redisplay_current_scene()
            return

        if self.inventory.has(cmd_lower):
            self.inventory.get(cmd_lower).show_description()
            return

        await self.scene_manager.process_command(command)

    def save_checkpoint(self, scene_id: str):
        self.checkpoint_data = {
            "inventory_items": copy.deepcopy(self.inventory.items),
            "player_stamina": self.player.current_stamina,
            "player_max_stamina": self.player.max_stamina,
            "scene_id": scene_id,
        }

    def load_checkpoint(self):
        if not self.checkpoint_data:
            self.ui.print_system_message("저장된 체크포인트가 없습니다. 처음부터 시작합니다.")
            self.start_game()
            return

        self.inventory._items = copy.deepcopy(self.checkpoint_data["inventory_items"])
        self.ui.update_inventory_status(self.inventory.items)

        self.player.current_stamina = self.checkpoint_data["player_stamina"]
        self.player.max_stamina = self.checkpoint_data["player_max_stamina"]
        self.ui.update_stamina_status(self.player.current_stamina, self.player.max_stamina)

        target_scene = self.checkpoint_data["scene_id"]
        self.scene_manager.reset_scene()
        self.scene_manager.switch_scene(target_scene)
