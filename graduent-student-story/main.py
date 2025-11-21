import sys

from entity import Inventory, Player
from game import Game
from test import TestRunner
from ui import UIManager

if __name__ == "__main__":
    print(sys.version)

    # 의존성 주입 (Dependency Injection)
    ui_manager = UIManager()
    inventory = Inventory()
    test_runner = TestRunner()

    # 초기 체력을 70으로 설정하여 생성
    player = Player(max_stamina=70)

    # Game 클래스는 필요한 의존성을 주입받아 생성됨
    game = Game(ui_manager=ui_manager, inventory=inventory, player=player, test_runner=test_runner)
