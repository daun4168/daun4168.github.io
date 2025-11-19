from ui import UIManager, get_josa


class Entity:
    """
    게임 내 모든 개체의 기본 클래스.
    UI 출력 기능을 가집니다.
    """
    _ui: UIManager = None  # UI 매니저 정적 참조

    @classmethod
    def set_ui_manager(cls, ui_manager: UIManager):
        """모든 엔티티가 공유할 UI 매니저 설정"""
        cls._ui = ui_manager

    def show(self):
        """기본 show 동작"""
        if self._ui:
            self._ui.print_system_message("아무 일도 일어나지 않았습니다..")


class Item(Entity):
    def __init__(self, name: str, description: str):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item('{self.name}')"

    def show(self):
        """아이템 설명 출력"""
        if self._ui:
            self._ui.print_narrative(f"**[{self.name}]**\n{self.description}", is_markdown=True)


class Bag(Entity):
    def __init__(self):
        super().__init__()
        self._items = {}

    def add(self, item: Item):
        self._items[item.name] = item
        if self._ui:
            josa = get_josa(item.name, "을/를")
            self._ui.update_inventory_ui(self._items)
            self._ui.print_system_message(f"'{item.name}'{josa} 가방에 추가했습니다.")

    def remove(self, item_name: str) -> Item | None:
        item = self._items.pop(item_name, None)
        if item and self._ui:
            self._ui.update_inventory_ui(self._items)
        return item

    def get(self, item_name: str) -> Item | None:
        return self._items.get(item_name)

    def show(self):
        if self._ui:
            item_list = ', '.join(self._items.keys())
            if not item_list:
                item_list = "가방이 비어 있습니다."
            self._ui.print_narrative(f"**[가방]**\n현재 가지고 있는 도구: {item_list}")

    @property
    def items(self):
        return self._items
