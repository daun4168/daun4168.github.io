import sys
from game import Game
from ui import UIManager
from entity import Inventory
from test import TestRunner

if __name__ == "__main__":
    print(sys.version)

    # 의존성 주입 (Dependency Injection)
    ui_manager = UIManager()
    inventory = Inventory()
    test_runner = TestRunner()

    # Game 클래스는 필요한 의존성을 주입받아 생성됨
    game = Game(ui_manager=ui_manager, inventory=inventory, test_runner=test_runner)
