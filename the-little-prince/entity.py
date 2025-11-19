from ui import UIManager, get_josa


class Entity:
    """게임 내 모든 개체의 기본 클래스."""
    _ui: UIManager = None

    @classmethod
    def set_ui_manager(cls, ui_manager: UIManager):
        cls._ui = ui_manager

    def show(self):
        if self._ui:
            self._ui.print_system_message("특별한 점을 찾지 못했다.")


class Item(Entity):
    """이름, 설명, 그리고 별칭(aliases)을 가지는 아이템 개체."""
    def __init__(self, name: str, description: str, aliases: list[str] = None):
        super().__init__()
        self.name = name
        self.description = description
        self.aliases = aliases if aliases else []

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item('{self.name}')"

    def show(self):
        """아이템의 이름, 설명, 그리고 단축어를 화면에 표시합니다."""
        if self._ui:
            full_description = f"**[{self.name}]**\n{self.description}"
            if self.aliases:
                alias_str = ", ".join(f"`{a}`" for a in self.aliases)
                full_description += f"\n(단축어: {alias_str})"
            self._ui.print_narrative(full_description, is_markdown=True)


class Bag(Entity):
    """아이템을 담을 수 있는 가방 개체."""
    def __init__(self):
        super().__init__()
        self._items = {}

    def add(self, item: Item, silent: bool = False):
        self._items[item.name] = item
        if self._ui and not silent:
            josa = get_josa(item.name, "을/를")
            self._ui.print_system_message(f"'{item.name}'{josa} 가방에 추가했습니다.")

    def remove(self, item_name: str) -> Item | None:
        item = self._items.pop(item_name, None)
        if item and self._ui:
            self._ui.update_bag_status(self.items)
        return item

    def get(self, item_name: str) -> Item | None:
        return self._items.get(item_name)

    def show(self):
        """가방 안의 아이템 전체 이름과 대표 단축어를 함께 표시합니다."""
        if self._ui:
            if not self._items:
                item_list_str = "가방이 비어 있습니다."
            else:
                display_names = []
                for item in self._items.values():
                    name = item.name
                    if item.aliases:
                        name += f" (단축어: `{item.aliases[0]}`)"
                    display_names.append(name)
                item_list_str = ", ".join(display_names)
            
            self._ui.print_narrative(f"**[가방]**\n현재 가지고 있는 도구: {item_list_str}", is_markdown=True)

    @property
    def items(self) -> dict:
        return self._items
