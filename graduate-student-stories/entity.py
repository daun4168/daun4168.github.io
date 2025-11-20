from ui import UIManager

class Entity:
    """게임 내 모든 객체의 부모 클래스"""
    ui: UIManager = None

    @classmethod
    def set_ui_manager(cls, ui_manager: UIManager):
        cls.ui = ui_manager

class Item(Entity):
    """이름과 설명을 가지는 아이템 클래스"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Bag(Entity):
    """Item 객체들을 관리하는 가방 클래스"""
    def __init__(self):
        self.items: dict[str, Item] = {}

    def add(self, item: Item):
        self.items[item.name] = item
        self.ui.update_inventory(self.get_item_names())

    def remove(self, item_name: str) -> Item | None:
        item = self.items.pop(item_name, None)
        self.ui.update_inventory(self.get_item_names())
        return item

    def has(self, item_name: str) -> bool:
        return item_name in self.items

    def get_item_names(self) -> list[str]:
        return list(self.items.keys())
