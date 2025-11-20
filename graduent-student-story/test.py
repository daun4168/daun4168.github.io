import asyncio
import re

from js import window

# --- 테스트 케이스별 명령어 목록 ---

# Scene 0: 교수님 오피스
COMMANDS_SCENE_0 = [
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
]

COMMANDS_SCENE_1 = [
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
    "컴퓨터 : 1234",
    "컴퓨터 : 12345678",
    "문",
    "시약장 : 0815",
    "에탄올",
    "에탄올 + 바닥",
    "빗자루 + 바닥",
    "에탄올 + 의문의 액체",
    "빗자루 + 바닥",
]

COMMANDS_SCENE_2 = [
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
]


class TestRunner:
    def __init__(self):
        self.game = None
        # 테스트 함수들을 리스트로 관리하여 확장성 확보
        self.sequences = [
            self._run_scene0_sequence,
            self._run_scene1_sequence,
            self._run_scene2_sequence,
        ]

    def set_game(self, game):
        """Game 객체를 설정하여 순환 참조를 해결합니다."""
        self.game = game

    async def run_test_command(self, command: str):
        """
        'test'로 시작하는 명령어를 파싱하여 해당 테스트를 실행합니다.
        - `test0`: 0번 테스트 실행
        - `test0-2`: 0번, 1번, 2번 테스트를 순차적으로 실행
        """
        if "localhost" not in window.location.hostname or not command.startswith("test"):
            return False

        if not self.game:
            print("TestRunner: Game object not set.")
            return False

        match = re.match(r"test(\d+)(?:-(\d+))?", command)
        if not match:
            return False

        start_index = int(match.group(1))
        end_index = int(match.group(2)) if match.group(2) else start_index

        if start_index >= len(self.sequences) or end_index >= len(self.sequences):
            self.game.ui.print_system_message(
                f"오류: 존재하지 않는 테스트 번호입니다. (사용 가능한 범위: 0-{len(self.sequences) - 1})"
            )
            return True

        for i in range(start_index, end_index + 1):
            await self.sequences[i]()

        self.game.ui.print_system_message(f"테스트 실행 완료: {command}")
        return True

    async def _execute_sequence(self, commands):
        """주어진 명령어 목록을 순차적으로 실행합니다."""
        for cmd in commands:
            await self.game.process_command(cmd)
            await asyncio.sleep(0.1)  # 각 명령어 사이의 최소 딜레이

    async def _run_scene0_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_0)

    async def _run_scene1_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_1)

    async def _run_scene2_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_2)
