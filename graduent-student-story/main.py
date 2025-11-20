import sys
from game import Game, SceneLoader
from ui import UIManager
from entity import Inventory
from test import TestRunner

if __name__ == "__main__":
    print(sys.version)
    
    # 의존성 주입 (Dependency Injection)
    ui_manager = UIManager()
    scene_loader = SceneLoader()
    inventory = Inventory()
    test_runner = TestRunner()
    
    game = Game(
        ui_manager=ui_manager,
        scene_loader=scene_loader,
        inventory=inventory,
        test_runner=test_runner
    )
