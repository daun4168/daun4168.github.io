import sys
from unittest.mock import MagicMock

# --- 테스트 환경 설정 ---
# pyscript의 document 객체가 없으므로, 테스트 시에는 이를 모의(Mock) 객체로 대체합니다.
# 이렇게 하면 브라우저 환경이 아닌 일반 Python 환경에서도 코드를 실행할 수 있습니다.
mock_document = MagicMock()
sys.modules['pyscript'] = MagicMock(document=mock_document)

from game import Game, CMD_START, CMD_LOOK_AROUND, CMD_BAG, CMD_EXAMINE
from entity import Entity

class MockUIManager:
    """
    테스트를 위한 가짜 UI 관리자입니다.
    실제 웹 페이지에 출력하는 대신, 모든 메시지를 리스트에 저장합니다.
    """
    def __init__(self):
        self.printed_system_messages = []
        self.printed_narratives = []
        self.created_puzzles = []
        self.updated_bag_status = []

    def print_system_message(self, message: str, is_markdown: bool = False):
        self.printed_system_messages.append(message)

    def print_narrative(self, message: str, is_markdown: bool = False):
        self.printed_narratives.append(message)

    def create_puzzle(self, title: str, hint: str, content: str):
        self.created_puzzles.append({"title": title, "hint": hint, "content": content})
    
    def update_bag_status(self, items: dict):
        self.updated_bag_status.append(items)

    # game.py에서 호출하지만 테스트에 직접 필요하지는 않은 메서드들
    def print_user_log(self, message: str): pass
    def set_location_name(self, name: str): pass
    def show_hr_divider(self): pass
    def set_initial_bag_status(self): pass
    def show(self): pass # Bag.show()에서 호출

def test_initial_command_sequence():
    """
    사용자가 요청한 초기 명령어 시퀀스를 테스트합니다.
    "시작" -> "둘러보기" -> "가방" -> "조사 돋보기" -> "조사 깨진 거울 조각"
    """
    print("--- 테스트 시작: 초기 명령어 시퀀스 ---")

    # 1. 테스트 환경 설정
    mock_ui = MockUIManager()
    game = Game()
    
    # Game 객체와 Entity 클래스가 Mock UI를 사용하도록 설정
    game.ui = mock_ui
    Entity.set_ui_manager(mock_ui)

    # 2. 테스트할 명령어 시퀀스 정의
    commands = [
        CMD_START,
        CMD_LOOK_AROUND,
        CMD_BAG[0],  # CMD_BAG은 리스트이므로 첫 번째 요소를 사용
        f"{CMD_EXAMINE[0]} 돋보기",
        f"{CMD_EXAMINE[0]} 깨진 거울 조각",
        f"{CMD_EXAMINE[0]} 연필",
    ]

    # 3. 명령어 순차 실행
    for cmd in commands:
        print(f"실행: {cmd}")
        game.process_command(cmd)

    # 4. 최종 상태 검증 (Assert)
    # 게임이 시작되었는가?
    assert game.game_started, "게임이 시작되지 않았습니다."
    print("검증 통과: game.game_started == True")

    # 가방을 획득했는가?
    assert game.bag is not None, "가방을 획득하지 못했습니다."
    print("검증 통과: game.bag is not None")

    # 가방에 초기 아이템이 모두 들어있는가?
    initial_items = ["연필", "돋보기", "깨진 거울 조각"]
    assert all(item_name in game.bag.items for item_name in initial_items), "가방에 초기 아이템이 모두 들어있지 않습니다."
    print(f"검증 통과: 가방에 {', '.join(initial_items)} 아이템 존재")

    # 모든 초기 아이템을 조사했는가?
    assert len(game.investigated_items) == len(initial_items), "모든 아이템을 조사하지 않았습니다."
    print(f"검증 통과: {len(game.investigated_items)}개의 아이템 조사 완료")
    
    # 조합 안내 메시지가 출력되었는가?
    combine_prompt = next((msg for msg in mock_ui.printed_system_messages if "조합" in msg), None)
    assert combine_prompt is not None, "조합 안내 메시지가 출력되지 않았습니다."
    print("검증 통과: 조합 안내 메시지 출력")
    
    print("\n--- 모든 테스트 통과! ---")

if __name__ == "__main__":
    test_initial_command_sequence()
