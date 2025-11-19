import asyncio
from js import window


COMMANDS_GAME_START = [
    "시작",
    "둘러보기",
    "가방",
    "조사",
    "조사 돋보기",
    "조사 연필",
    "조사 색연필",
    "조사 거울",
    "조합",
    "조합 연필 거울",
    "힌트",
    "조합 돋보기 거울",
    "사용",
    "사용 집광기",
    "사용 돋보기 녹슨핀",
    "힌트",
    "사용 집광기 녹슨핀",
    "조사 일기",
    "힌트",
    "조합 연필 일기",
    "조사 일기",
]

COMMANDS_CHAPTER_1 = [
    "정답",
    "힌트1",
    "모자",
    "힌트2",

]


class TestRunner:
    def __init__(self, game):
        self.game = game
        self.test_sequences = {
            "test1": self._run_test1_sequence,
        }

    async def run_test_command(self, command: str):
        if "localhost" not in window.location.hostname or not command.startswith("test"):
            return False

        test_func = self.test_sequences.get(command)
        if test_func:
            await test_func()
            return True
            
        return False

    async def _execute_sequence(self, commands):
        for cmd in commands:
            await self.game.process_command(cmd)
            await asyncio.sleep(0.05)

    async def _run_test1_sequence(self):
        await self._execute_sequence(COMMANDS_GAME_START)
