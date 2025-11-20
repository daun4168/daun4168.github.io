from ui import UIManager, get_josa


class Entity:
    _ui: UIManager = None

    @classmethod
    def set_ui_manager(cls, ui_manager: UIManager):
        cls._ui = ui_manager

    def show(self):
        if self._ui:
            self._ui.print_system_message("특별한 점을 찾지 못했다.")


class Item(Entity):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item('{self.name}')"

    def show_description(self):
        """아이템의 이름과 설명을 화면에 표시합니다."""
        if self._ui:
            self._ui.print_narrative(f"**[{self.name}]**\n{self.description}", is_markdown=True)


class Inventory(Entity):
    def __init__(self):
        super().__init__()
        self._items = {}

    def add(self, item: Item, silent: bool = False):
        self._items[item.name] = item
        if self._ui:
            if not silent:
                self._ui.print_system_message(
                    f"**[{item.name}]**{get_josa(item.name, '을/를')} **주머니**에 넣었습니다.", is_markdown=True
                )
            self._ui.update_inventory_status(self.items)

    def remove(self, item_name: str):
        if item_name in self._items:
            del self._items[item_name]
            if self._ui:
                self._ui.update_inventory_status(self.items)

    def has(self, item_name: str) -> bool:
        return item_name in self._items

    def get(self, item_name: str) -> Item | None:
        return self._items.get(item_name)

    def show(self):
        if self._ui:
            self._ui.update_inventory_status(self._items)

    @property
    def items(self) -> dict:
        return self._items


class Player(Entity):
    """
    플레이어의 생명력(체력)과 상태를 관리하는 클래스입니다.
    """

    def __init__(self, max_stamina: int = 100):
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina

    def modify_stamina(self, amount: int) -> int:
        """
        체력을 증감시키고 결과를 반환합니다.
        0 이하로 떨어지거나 최대치를 넘지 않도록 보정합니다.
        """
        prev_stamina = self.current_stamina
        # 체력 보정 로직 (0 ~ Max 사이 유지)
        self.current_stamina = max(0, min(self.current_stamina + amount, self.max_stamina))

        if self._ui:
            # UI 업데이트
            self._ui.update_stamina_status(self.current_stamina, self.max_stamina)

            # 체력 변화 시스템 메시지 출력
            if amount < 0:
                self._ui.print_system_message(f"체력이 {-amount} 감소했습니다.", is_markdown=True)
            elif amount > 0:
                self._ui.print_system_message(f"체력이 {amount} 회복되었습니다.", is_markdown=True)

        return self.current_stamina

    def is_dead(self) -> bool:
        """체력이 0 이하인지 확인합니다."""
        return self.current_stamina <= 0
