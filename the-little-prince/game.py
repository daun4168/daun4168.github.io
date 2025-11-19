from pyscript import document
from ui import UIManager
from entity import Entity, Item, Bag


class Game:
    """
    게임의 핵심 로직, 이벤트 핸들러, 명령어 처리 및 상태 관리를 담당합니다.
    모든 명령어는 `eval()`을 통해 실행됩니다.
    """

    def __init__(self):
        # 1. UI 매니저 초기화 및 Entity 연결
        self.ui = UIManager()
        Entity.set_ui_manager(self.ui)

        # 2. DOM 요소 참조 및 이벤트 연결
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.submit_button.onclick = self.handle_click
        self.user_input.onkeypress = self.handle_enter

        # 3. 게임 상태 및 전역 변수 초기화
        self.bag = None
        self.exec_globals = {
            '시작': self.시작,
            '조합': self.조합,
            'Item': Item,
        }

        print("Game Initialized")
        self.ui.print_narrative(
            "**어린 왕자: 사막의 별**\n\n"
            "눈을 뜨자 끝없는 모래 언덕이 펼쳐집니다. "
            "당신은 불시착한 비행기의 조종사입니다.\n\n"
            "모험을 시작하려면 `시작()`을 입력하세요.",
            is_markdown=True
        )

    def handle_click(self, event):
        """버튼 클릭 이벤트 처리"""
        content = self.user_input.value.strip()
        if not content:
            self.user_input.focus()
            return
        self.process_command(content)
        self.user_input.value = ""
        self.user_input.focus()

    def handle_enter(self, event):
        """엔터키 입력 이벤트 처리"""
        if event.key == "Enter":
            self.handle_click(event)

    def process_command(self, command: str):
        """사용자 명령어를 eval로 실행합니다."""
        self.ui.print_user_log(command)
        output = None
        try:
            with Entity.safe_execution():
                output = eval(command, self.exec_globals, self.exec_globals)
        except Exception as e:
            self.ui.print_system_message(f"오류: 알 수 없는 명령이거나 실행 오류가 발생했습니다. ({e.__class__.__name__}: {e})")

        if isinstance(output, Entity):
            output.show()
        elif output is not None and not isinstance(output, Bag):
            self.ui.print_system_message(f"결과: {output}")

    def 조합(self, item_a: Item, item_b: Item) -> Entity | None:
        """두 아이템을 조합합니다."""
        if not self.bag:
            return "게임이 아직 시작되지 않았습니다. `시작()`을 먼저 호출해주세요."

        if not isinstance(item_a, Item) or not isinstance(item_b, Item) or not self.bag.get(item_a.name) or not self.bag.get(item_b.name):
            return "가방에 없거나 조합할 수 없는 아이템입니다."

        key = tuple(sorted([item_a.name, item_b.name]))
        if key == ("돋보기", "깨진 거울 조각"):
            self.bag.remove("돋보기")
            self.bag.remove("깨진 거울 조각")
            new_item = Item("태양열 집광 장치", "강력한 열을 모을 수 있습니다.")
            self.bag.add(new_item)
            self.exec_globals["태양열_집광_장치"] = new_item
            self.ui.print_narrative("두 조각을 합쳐 **태양열 집광 장치**를 만들었습니다!", is_markdown=True)
            return new_item
        return "아무 반응이 없습니다."

    def 시작(self):
        """게임을 시작하고 초기 상태를 설정합니다."""
        if self.bag:
            return "게임이 이미 시작되었습니다."

        # UI 요소에 텍스트 설정 및 표시
        self.ui.set_location_name("사하라 사막")
        self.ui.show_hr_divider()

        # 게임 상태 초기화
        self.bag = Bag()
        items = [
            Item("연필", "평범한 연필입니다."),
            Item("돋보기", "작은 것들을 관찰할 수 있는 돋보기입니다."),
            Item("깨진 거울 조각", "빛을 반사하는 날카로운 조각입니다.")
        ]
        for item in items:
            self.bag.add(item)

        self.exec_globals.update({
            '가방': self.bag, '인벤토리': self.bag, 'i': self.bag,
            '연필': self.bag.get('연필'),
            '돋보기': self.bag.get('돋보기'),
            '거울': self.bag.get('깨진 거울 조각'),
        })

        self.ui.update_inventory_ui(self.bag.items)
        self.ui.print_narrative("비행기가 사막에 불시착했습니다. 이제부터 당신의 이야기가 시작됩니다.", is_markdown=True)
        
        return "게임 시작!"
