from pyscript import document
from ui import UIManager, get_josa
from entity import Entity, Item, Bag


class Game:
    """
    게임의 핵심 로직, 이벤트 핸들러, 명령어 처리 및 상태 관리를 담당합니다.
    파서 기반의 명령어 처리 시스템을 사용합니다.
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

        # 3. 게임 상태 초기화
        self.bag = None
        self.game_started = False
        self.has_checked_bag = False  # 튜토리얼 진행 상태

        print("Game Initialized")
        self.ui.print_narrative(
            "**어린 왕자: 사막의 별**\n\n"
            "눈을 뜨자 끝없는 모래 언덕이 펼쳐집니다. "
            "당신은 불시착한 비행기의 조종사입니다.\n\n"
            "모험을 시작하려면 `시작`을 입력하세요.",
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
        """사용자 명령어를 파싱하고 실행합니다."""
        self.ui.print_user_log(command)
        
        parts = command.lower().strip().split()
        if not parts:
            return

        verb = parts[0]
        args = parts[1:]

        if not self.game_started:
            if verb == "시작":
                self._start_game()
            else:
                self.ui.print_system_message("모험을 시작하려면 `시작`을 입력하세요.")
            return

        if verb == "조합":
            if len(args) == 2:
                self._combine_items(args[0], args[1])
            else:
                self.ui.print_system_message("사용법: `조합 <아이템1> <아이템2>`")
        elif verb in ["가방", "i"]:
            self.bag.show()
            if not self.has_checked_bag:
                self.ui.print_system_message("아이템의 자세한 설명을 보려면 `조사 <이름>` (예: `조사 연필`)을 입력하세요.")
                self.has_checked_bag = True
        elif verb in ["조사", "보기"]:
             if len(args) == 1:
                self._examine(args[0])
             else:
                self.ui.print_system_message("사용법: `조사 <대상>`")
        else:
            josa = get_josa(command, "은/는")
            self.ui.print_system_message(f"'{command}'{josa} 알 수 없는 명령어입니다.")

    def _combine_items(self, name_a: str, name_b: str):
        """두 아이템을 조합합니다."""
        if name_a == '거울': name_a = '깨진 거울 조각'
        if name_b == '거울': name_b = '깨진 거울 조각'

        item_a = self.bag.get(name_a)
        item_b = self.bag.get(name_b)

        if not item_a or not item_b:
            self.ui.print_system_message("가방에 없는 물건이거나, 이름을 잘못 입력했습니다.")
            return

        key = tuple(sorted([item_a.name, item_b.name]))
        if key == ("돋보기", "깨진 거울 조각"):
            self.bag.remove("돋보기")
            self.bag.remove("깨진 거울 조각")
            new_item = Item("태양열 집광 장치", "강력한 열을 모을 수 있습니다.")
            self.bag.add(new_item)
            self.ui.print_narrative("두 조각을 합쳐 **태양열 집광 장치**를 만들었습니다!", is_markdown=True)
            return

        self.ui.print_system_message("두 아이템을 조합했지만 아무 일도 일어나지 않았습니다.")

    def _examine(self, target_name: str):
        """대상을 조사합니다."""
        if target_name == '거울': target_name = '깨진 거울 조각'
        
        item = self.bag.get(target_name)
        if item:
            item.show()
            return
        
        josa = get_josa(target_name, "은/는")
        self.ui.print_system_message(f"'{target_name}'{josa} 조사할 수 없는 대상입니다.")

    def _start_game(self):
        """게임을 시작하고 초기 상태를 설정합니다."""
        if self.game_started:
            self.ui.print_system_message("게임이 이미 시작되었습니다.")
            return

        self.game_started = True
        
        self.ui.set_location_name("사하라 사막")
        self.ui.show_hr_divider()

        self.bag = Bag()
        items = [
            Item("연필", "평범한 연필입니다."),
            Item("돋보기", "작은 것들을 관찰할 수 있는 돋보기입니다."),
            Item("깨진 거울 조각", "빛을 반사하는 날카로운 조각입니다.")
        ]
        for item in items:
            self.bag.add(item)

        self.ui.update_inventory_ui(self.bag.items)
        self.ui.print_narrative("비행기가 사막에 불시착했습니다. 이제부터 당신의 이야기가 시작됩니다.", is_markdown=True)
        self.ui.print_system_message("게임 시작! `가방`을 입력해 소지품을 확인해보세요.")
