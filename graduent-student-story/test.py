import asyncio
from js import window

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
    "빗자루",
    "의문의 액체",
    "바닥",
    "시약장",
    "컴퓨터",
    "컴퓨터 + 1234",
    "컴퓨터 + 12345678",
    "문",
    "시약장 + 0815",
    "에탄올",
    "에탄올 + 바닥",
    "빗자루 + 바닥",
    "에탄올 + 의문의 액체",
]

COMMANDS_SCENE_2 = [
    "MK-II",
]

class TestRunner:
    def __init__(self, game):
        self.game = game
        self.test_sequences = {
            "test0": self._run_scene0_sequence,
            "test1": self._run_scene1_sequence,
            "test2": self._run_scene2_sequence,
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
            await asyncio.sleep(0.5)

    async def _run_scene0_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_0)

    async def _run_scene1_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_1)

    async def _run_scene2_sequence(self):
        await self._execute_sequence(COMMANDS_SCENE_2)
