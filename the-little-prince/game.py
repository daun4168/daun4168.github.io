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
        self.ui.set_initial_bag_status()

        # 2. DOM 요소 참조 및 이벤트 연결
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.submit_button.onclick = self.handle_click
        self.user_input.onkeypress = self.handle_enter

        # 3. 게임 상태 초기화
        self.bag = None
        self.game_started = False
        self.has_checked_bag = False

        print("Game Initialized")
        self.ui.print_narrative(
            "**어린 왕자: 사막의 별**\n\n"
            "눈을 뜨자 끝없는 모래 언덕이 펼쳐집니다. "
            "당신은 불시착한 비행기의 조종사입니다.\n\n"
            "모험을 시작하려면 `시작`을 입력하세요.",
            is_markdown=True
        )

    def handle_click(self, event):
        content = self.user_input.value.strip()
        if not content:
            self.user_input.focus()
            return
        self.process_command(content)
        self.user_input.value = ""
        self.user_input.focus()

    def handle_enter(self, event):
        if event.key == "Enter":
            self.handle_click(event)

    def process_command(self, command: str):
        self.ui.print_user_log(command)
        
        parts = command.strip().split()
        if not parts:
            return

        verb = parts[0].lower()
        arg_string = " ".join(parts[1:])

        if not self.game_started:
            if verb == "시작":
                self._start_game()
            else:
                self.ui.print_system_message("모험을 시작하려면 `시작`을 입력하세요.")
            return

        if verb == "조합":
            if arg_string:
                self._combine_items(arg_string)
            else:
                self.ui.print_system_message("사용법: `조합 <아이템1> <아이템2>`")
        elif verb in ["가방", "i"]:
            self.bag.show()
            if not self.has_checked_bag:
                self.ui.update_inventory_ui(self.bag.items)
                self.ui.print_system_message("상단에 있는 가방의 상태가 업데이트 되었습니다.")
                self.ui.print_system_message("아이템의 자세한 설명을 보려면 `조사 <이름>` (예: `조사 연필`)을 입력하세요.")
                self.has_checked_bag = True
        elif verb in ["조사", "보기"]:
             if arg_string:
                self._examine(arg_string)
             else:
                self.ui.print_system_message("사용법: `조사 <대상>`")
        else:
            josa = get_josa(command, "은/는")
            self.ui.print_system_message(f"'{command}'{josa} 알 수 없는 명령어입니다.")

    def _find_item_by_name(self, name: str) -> Item | None:
        """가방에서 대소문자 구분 없이 아이템을 찾습니다."""
        # '거울'을 '깨진 거울 조각'의 별칭으로 처리
        if name.lower() == '거울':
            name = '깨진 거울 조각'
            
        for item_name, item_obj in self.bag.items.items():
            if item_name.lower() == name.lower():
                return item_obj
        return None

    def _combine_items(self, combined_name: str):
        """'아이템1 아이템2' 형식의 문자열을 받아 조합을 시도합니다."""
        parts = combined_name.split()
        
        # 모든 가능한 분할 지점을 테스트합니다.
        for i in range(1, len(parts)):
            name_a = " ".join(parts[:i])
            name_b = " ".join(parts[i:])
            
            item_a = self._find_item_by_name(name_a)
            item_b = self._find_item_by_name(name_b)

            if item_a and item_b:
                # 실제 조합 로직
                key = tuple(sorted([item_a.name, item_b.name]))
                if key == ("돋보기", "깨진 거울 조각"):
                    self.bag.remove("돋보기")
                    self.bag.remove("깨진 거울 조각")
                    new_item = Item("태양열 집광 장치", "강력한 열을 모을 수 있습니다.")
                    self.bag.add(new_item)
                    self.ui.update_inventory_ui(self.bag.items)
                    self.ui.print_narrative("두 조각을 합쳐 **태양열 집광 장치**를 만들었습니다!", is_markdown=True)
                    return
        
        self.ui.print_system_message("의미 있는 조합이 아니거나, 가방에 없는 물건입니다.")

    def _examine(self, target_name: str):
        """대상을 조사합니다."""
        item = self._find_item_by_name(target_name)
        if item:
            item.show()
            return
        
        josa = get_josa(target_name, "은/는")
        self.ui.print_system_message(f"'{target_name}'{josa} 조사할 수 없는 대상입니다.")

    def _start_game(self):
        if self.game_started:
            self.ui.print_system_message("게임이 이미 시작되었습니다.")
            return

        self.game_started = True
        
        self.ui.set_location_name("사하라 사막")
        self.ui.set_initial_bag_status()
        self.ui.show_hr_divider()

        self.bag = Bag()
        items = [
            Item("연필", "평범한 연필입니다."),
            Item("돋보기", "작은 것들을 관찰할 수 있는 돋보기입니다."),
            Item("깨진 거울 조각", "빛을 반사하는 날카로운 조각입니다.")
        ]
        for item in items:
            self.bag._items[item.name] = item

        self.ui.print_narrative("비행기가 사막에 불시착했습니다. 이제부터 당신의 이야기가 시작됩니다.", is_markdown=True)
        self.ui.print_system_message("게임 시작! `가방`을 입력해 소지품을 확인해보세요.")
