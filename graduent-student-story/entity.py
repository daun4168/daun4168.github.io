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
