# scene.py
import copy
from ui import get_josa
from entity import Item
from const import KeywordState, ActionType, ConditionType, KeywordType


class Scene:
    """데이터 기반(Data-Driven) 장면 엔진"""

    def __init__(self, game, ui, inventory, scene_data):
        self.game = game
        self.ui = ui
        self.inventory = inventory
        self.scene_data = copy.deepcopy(scene_data)
        self.state = self.scene_data.get("initial_state", {})

    @property
    def scene_id(self) -> str:
        return self.scene_data.get("id", "unknown")

    def on_enter(self):
        self.ui.set_location_name(self.scene_data["name"])
        self.ui.print_narrative(self.scene_data["initial_text"], is_markdown=True)
        self.ui.update_sight_status(self.scene_data["keywords"])

        if "on_enter_actions" in self.scene_data:
            self._execute_actions(self.scene_data["on_enter_actions"])

    def on_redisplay(self):
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        self.ui.print_narrative(self.scene_data["initial_text"], is_markdown=True)

    def resolve_alias(self, keyword: str) -> str:
        cmd_lower = keyword.lower()
        for k, v in self.scene_data["keywords"].items():
            if k.lower() == cmd_lower:
                if v.get("type") == KeywordType.ALIAS:
                    return v.get("target", k)
                return k
        return keyword

    async def process_keyword(self, keyword: str) -> bool:
        original_keyword = self.resolve_alias(keyword)
        keyword_data = self.scene_data["keywords"].get(original_keyword)

        if not keyword_data:
            return False

        silent_discovery = keyword_data.get("silent_discovery", False)
        self._discover_keyword(original_keyword, silent=silent_discovery)

        if "interactions" in keyword_data:
            for interaction in keyword_data["interactions"]:
                if self._check_conditions(interaction.get("conditions", [])):
                    self._execute_actions(interaction.get("actions", []))
                    return True

        if "description" in keyword_data:
            self.ui.print_narrative(keyword_data["description"], is_markdown=True)
            return True

        return True

    async def process_combination(self, item1: str, item2: str) -> bool:
        combinations = self.scene_data.get("combinations", [])

        r_item1 = self.resolve_alias(item1)
        r_item2 = self.resolve_alias(item2)

        for combo in combinations:
            targets = combo.get("targets", [])
            if len(targets) != 2:
                continue

            input_set = {r_item1.lower(), r_item2.lower()}
            target_set = {t.lower() for t in targets}

            if input_set == target_set:
                if not self._check_keyword_visible(r_item1) or not self._check_keyword_visible(r_item2):
                    return False

                if self._check_conditions(combo.get("conditions", [])):
                    self._execute_actions(combo.get("actions", []))
                    return True

        return False

    def _check_keyword_visible(self, keyword: str) -> bool:
        # 1. 인벤토리에 있는 아이템이면 무조건 사용 가능
        if self.inventory.has(keyword):
            return True

        # 2. 데이터에 없는 단순 문자열(비번 등)은 True
        if keyword not in self.scene_data["keywords"]:
            return True

        k_data = self.scene_data["keywords"][keyword]
        if k_data.get("type") == KeywordType.ALIAS:
            return True

            # 3. Hidden 상태면 사용 불가
        if k_data.get("state") == KeywordState.HIDDEN:
            return False

        return True

    def _discover_keyword(self, keyword_name: str, silent: bool = False):
        data = self.scene_data["keywords"].get(keyword_name)
        if data and data.get("state") == KeywordState.HIDDEN:
            data["state"] = KeywordState.DISCOVERED
            self.ui.update_sight_status(self.scene_data["keywords"])
            if not silent:
                self.ui.print_system_message(
                    f"**[{keyword_name}]**{get_josa(keyword_name, '을/를')} 발견하여 **시야**에 추가합니다.",
                    is_markdown=True,
                )

    def _check_conditions(self, conditions: list) -> bool:
        if not conditions:
            return True

        for cond in conditions:
            ctype = cond.get("type")
            target = cond.get("target")
            val = cond.get("value")

            if ctype == ConditionType.HAS_ITEM:
                if not self.inventory.has(target):
                    return False
            elif ctype == ConditionType.NOT_HAS_ITEM:
                if self.inventory.has(target):
                    return False
            elif ctype == ConditionType.STATE_IS:
                # 상태값이 일치하지 않으면 False
                if self.state.get(target) != val:
                    return False
            elif ctype == ConditionType.STATE_NOT:
                if self.state.get(target) == val:
                    return False

        return True

    def _execute_actions(self, actions: list):
        for action in actions:
            atype = action.get("type")
            val = action.get("value")

            if atype == ActionType.PRINT_NARRATIVE:
                self.ui.print_narrative(val, is_markdown=True)

            elif atype == ActionType.PRINT_SYSTEM:
                self.ui.print_system_message(val, is_markdown=True)

            elif atype == ActionType.ADD_ITEM:
                new_item = Item(val["name"], val["description"])
                is_silent = val.get("silent", False)
                self.inventory.add(new_item, silent=is_silent)

            elif atype == ActionType.REMOVE_ITEM:
                self.inventory.remove(val)

            elif atype == ActionType.REMOVE_KEYWORD:
                target = action.get("target")
                if target in self.scene_data["keywords"]:
                    del self.scene_data["keywords"][target]
                    self.ui.update_sight_status(self.scene_data["keywords"])

            elif atype == ActionType.UPDATE_STATE:
                if "key" in val:
                    self.state[val["key"]] = val["value"]
                if "keyword" in val:
                    k_name = val["keyword"]
                    if k_name in self.scene_data["keywords"]:
                        self.scene_data["keywords"][k_name]["state"] = val["state"]
                        self.ui.update_sight_status(self.scene_data["keywords"])

            elif atype == ActionType.MOVE_SCENE:
                self.game.scene_manager.switch_scene(val)

            # [중요] 엔딩 처리가 여기에 포함되어 있어야 합니다.
            elif atype == ActionType.GAME_END:
                self.ui.print_narrative(val, is_markdown=True)
                self.ui.print_system_message("--- GAME OVER ---", is_markdown=True)
                # 입력 막기
                if self.game:
                    self.game.user_input.disabled = True
                    self.game.submit_button.disabled = True
