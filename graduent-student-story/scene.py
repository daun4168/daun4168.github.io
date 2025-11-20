import copy
from ui import get_josa
from const import KeywordState, KeywordType
from logic_handlers import ACTION_HANDLERS, CONDITION_HANDLERS
from schemas import SceneData  # 타입 힌팅용

class Scene:
    def __init__(self, game, ui, inventory, scene_data: SceneData):
        self.game = game
        self.ui = ui
        self.inventory = inventory
        # Pydantic 모델은 mutable하므로 deepcopy 사용 (혹은 scene_data.model_copy(deep=True))
        self.scene_data = copy.deepcopy(scene_data)
        self.state = self.scene_data.initial_state  # 객체 속성 접근

    @property
    def scene_id(self) -> str:
        return self.scene_data.id

    def on_enter(self):
        self.ui.set_location_name(self.scene_data.name)
        self.ui.print_narrative(self.scene_data.initial_text, is_markdown=True)
        self.ui.update_sight_status(self.scene_data.keywords) # ui.py 수정 필요 (아래 참조)

        if self.scene_data.on_enter_actions:
            self._execute_actions(self.scene_data.on_enter_actions)

    def on_redisplay(self):
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        self.ui.print_narrative(self.scene_data.initial_text, is_markdown=True)

    def resolve_alias(self, keyword: str) -> str:
        cmd_lower = keyword.lower()
        for k, v in self.scene_data.keywords.items():
            if k.lower() == cmd_lower:
                if v.type == KeywordType.ALIAS: # 객체 속성 접근
                    return v.target or k
                return k
        return keyword

    async def process_keyword(self, keyword: str) -> bool:
        original_keyword = self.resolve_alias(keyword)
        keyword_data = self.scene_data.keywords.get(original_keyword)

        if not keyword_data:
            return False

        if keyword_data.state == KeywordState.INACTIVE:
            return False

        self._discover_keyword(original_keyword, silent=keyword_data.silent_discovery)

        if keyword_data.interactions:
            for interaction in keyword_data.interactions:
                if self._check_conditions(interaction.conditions):
                    self._execute_actions(interaction.actions)
                    return True

        if keyword_data.description:
            self.ui.print_narrative(keyword_data.description, is_markdown=True)
            return True

        return True

    async def process_combination(self, item1: str, item2: str) -> bool:
        combinations = self.scene_data.combinations
        r_item1 = self.resolve_alias(item1)
        r_item2 = self.resolve_alias(item2)

        for combo in combinations:
            targets = combo.targets
            if len(targets) != 2:
                continue

            input_set = {str(r_item1).lower(), str(r_item2).lower()}
            target_set = {str(t).lower() for t in targets}

            if input_set == target_set:
                if not self._check_keyword_visible(r_item1) or not self._check_keyword_visible(r_item2):
                    return False

                if self._check_conditions(combo.conditions):
                    self._execute_actions(combo.actions)
                    return True

        return False

    def _check_keyword_visible(self, keyword: str) -> bool:
        if self.inventory.has(keyword):
            return True

        if keyword not in self.scene_data.keywords:
            return True

        k_data = self.scene_data.keywords[keyword]
        if k_data.type == KeywordType.ALIAS:
            return True

        if k_data.state == KeywordState.HIDDEN:
            return False

        return True

    def _discover_keyword(self, keyword_name: str, silent: bool = False):
        data = self.scene_data.keywords.get(keyword_name)
        if data and data.state == KeywordState.HIDDEN:
            data.state = KeywordState.DISCOVERED
            self.ui.update_sight_status(self.scene_data.keywords)
            if not silent:
                self.ui.print_system_message(
                    f"**[{keyword_name}]**{get_josa(str(keyword_name), '을/를')} 발견하여 **시야**에 추가합니다.",
                    is_markdown=True,
                )

    def _check_conditions(self, conditions: list) -> bool:
        if not conditions:
            return True
        for cond in conditions:
            # Pydantic 모델이므로 .type, .target, .value 로 접근
            handler = CONDITION_HANDLERS.get(cond.type)
            if handler and not handler.check(self, cond.target, cond.value):
                return False
        return True

    def _execute_actions(self, actions: list):
        for action in actions:
            # Pydantic 모델이므로 .type, .value 로 접근
            handler = ACTION_HANDLERS.get(action.type)
            if handler:
                handler.execute(self, action.value)