import copy
from ui import get_josa
from const import KeywordState, ActionType, ConditionType, KeywordType
# [신규] 핸들러 레지스트리 임포트
from logic_handlers import ACTION_HANDLERS, CONDITION_HANDLERS


class Scene:
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

        if keyword_data.get("state") == KeywordState.INACTIVE:
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

            input_set = {str(r_item1).lower(), str(r_item2).lower()}
            target_set = {str(t).lower() for t in targets}

            if input_set == target_set:
                if not self._check_keyword_visible(r_item1) or not self._check_keyword_visible(r_item2):
                    return False

                if self._check_conditions(combo.get("conditions", [])):
                    self._execute_actions(combo.get("actions", []))
                    return True

        return False

    def _check_keyword_visible(self, keyword: str) -> bool:
        if self.inventory.has(keyword):
            return True

        if keyword not in self.scene_data["keywords"]:
            return True

        k_data = self.scene_data["keywords"][keyword]
        if k_data.get("type") == KeywordType.ALIAS:
            return True

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
                    f"**[{keyword_name}]**{get_josa(str(keyword_name), '을/를')} 발견하여 **시야**에 추가합니다.",
                    is_markdown=True,
                )

    # --- [변경됨] 전략 패턴이 적용된 메서드들 ---

    def _check_conditions(self, conditions: list) -> bool:
        if not conditions:
            return True

        for cond in conditions:
            # Enum 변환 (안전 장치)
            try:
                ctype = ConditionType(cond.get("type"))
            except ValueError:
                ctype = cond.get("type")

            handler = CONDITION_HANDLERS.get(ctype)

            if not handler:
                print(f"Warning: No handler for condition type '{ctype}'")
                continue  # 혹은 return False 처리

            # 핸들러에게 위임 (Delegate)
            if not handler.check(self, cond.get("target"), cond.get("value")):
                return False

        return True

    def _execute_actions(self, actions: list):
        for action in actions:
            # Enum 변환
            try:
                atype = ActionType(action.get("type"))
            except ValueError:
                atype = action.get("type")

            handler = ACTION_HANDLERS.get(atype)

            if handler:
                # 핸들러에게 위임 (Delegate)
                handler.execute(self, action.get("value"))
            else:
                print(f"Warning: No handler for action type '{atype}'")