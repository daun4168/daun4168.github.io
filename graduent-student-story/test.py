import asyncio
import re

from js import window

# --- 테스트 시나리오 데이터 ---
# 새로운 챕터나 테스트 케이스를 추가할 때는 이 딕셔너리에만 추가하면 됩니다.
TEST_SCENARIOS = {
    0: [
        "일어나기",
        "교수님",
        "문",
        "둘러보기",
        "논문",
        "안경알",
        "문",
        "법인카드",
        "논문",
        "책상",
        "물건",
        "문",
    ],
    1: [
        "쓰레기통",
        "쓰레기통",
        "쓰레기통",
        "박스",
        "법인카드 + 박스",
        "벽면",
        "벽",
        "메모",
        "벽",
        "빗자루",
        "의문의 액체",
        "바닥",
        "시약장",
        "컴퓨터",
        "컴퓨터 : 1234",  # 실패 케이스 테스트
        "컴퓨터 : 12345678",  # 성공 케이스
        "문",
        "시약장 : 0815",
        "에탄올",
        "에탄올 + 바닥",
        "빗자루 + 바닥",
        "에탄올 + 의문의 액체",
        "청소도구함",
        "실험용 랩 가운",
        "청소도구함 + 열쇠",
        "빗자루 + 바닥",
    ],
    2: [
        "MK-II",
        "전선",
        "콘센트",
        "탑승구",
        "교수님",
        "탑승구 + 스패너",
        "법인카드",
        "교수님",
        "교수님 + 법인카드",
        "탑승구 + 스패너",
    ],
    3: [
        "바다",
        "모래사장",
        "모래",
        "MK-II",
        "계기판",
        "통신기",
        "하늘",
        "태양",
        "스패너",
        "통신기 + 스패너",
    ],
    4: [
        "MK-II",
        "야자수",
        "야자수",
        "쓰레기 더미",
        "쓰레기 더미",
        "스패너",
        "야자수 + 스패너",
        "야자수 + 스패너",
        "스패너 + 코코넛",
        "스패너 + 코코넛",
        "모래",
        "바다",
        "숲 입구",
        "난파선 잔해",
        "난파선 잔해",
        "아니오",
        "난파선 잔해",
        "어라",
        "예",
    ],
}


class TestRunner:
    def __init__(self):
        self.game = None

    def set_game(self, game):
        """Game 객체를 설정하여 순환 참조를 해결합니다."""
        self.game = game

    async def run_test_command(self, command: str) -> bool:
        """
        'test'로 시작하는 명령어를 파싱하여 해당 테스트를 실행합니다.
        - `test0`: 0번 테스트 실행
        - `test0-2`: 0번부터 2번까지 순차 실행
        """
        # 1. 실행 환경 및 명령어 체크
        if "localhost" not in window.location.hostname or not command.startswith("test"):
            return False

        if not self.game:
            print("TestRunner Error: Game object is not set.")
            return False

        # 2. 정규식을 이용한 명령어 파싱 (예: test0, test0-2)
        match = re.match(r"test(\d+)(?:-(\d+))?", command)
        if not match:
            return False

        start_idx = int(match.group(1))
        end_idx = int(match.group(2)) if match.group(2) else start_idx

        # 3. 유효성 검사
        if not self._is_valid_range(start_idx, end_idx):
            max_idx = max(TEST_SCENARIOS.keys()) if TEST_SCENARIOS else 0
            self.game.ui.print_system_message(f"오류: 유효하지 않은 테스트 범위입니다. (가능 범위: 0-{max_idx})")
            return True

        # 4. 시나리오 순차 실행
        self.game.ui.print_system_message(f"🧪 테스트 시작: {command}")

        for i in range(start_idx, end_idx + 1):
            await self._run_scenario(i)

        self.game.ui.print_system_message(f"✅ 테스트 완료: {command}")
        return True

    def _is_valid_range(self, start: int, end: int) -> bool:
        """입력된 범위가 유효한지 확인합니다."""
        return start in TEST_SCENARIOS and end in TEST_SCENARIOS and start <= end

    async def _run_scenario(self, scenario_id: int):
        """특정 ID의 시나리오를 실행합니다."""
        commands = TEST_SCENARIOS.get(scenario_id)
        if not commands:
            return

        self.game.ui.print_system_message(f"--- Scene {scenario_id} Test Start ---")

        for cmd in commands:
            # 딜레이를 주어 너무 빠르게 지나가는 것을 방지
            await asyncio.sleep(0.1)
            await self.game.process_command(cmd)
