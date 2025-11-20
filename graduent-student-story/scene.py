import copy
from ui import get_josa
from const import KeywordState, KeywordType
from logic_handlers import ACTION_HANDLERS, CONDITION_HANDLERS
from schemas import SceneData  # 타입 힌팅용


class Scene:
    """
    게임 내 하나의 장면(Scene)을 나타내는 클래스입니다.
    장면의 데이터, 상태, 키워드 및 상호작용 로직을 관리합니다.
    """

    def __init__(self, game, ui, inventory, scene_data: SceneData):
        """
        Scene 클래스의 생성자입니다.

        Args:
            game: 게임의 메인 인스턴스 (Game 클래스).
            ui: 사용자 인터페이스 관리 객체 (UIManager).
            inventory: 플레이어의 인벤토리 객체 (Inventory).
            scene_data (SceneData): 해당 장면의 초기 데이터를 담은 Pydantic 모델.
        """
        self.game = game
        self.ui = ui
        self.inventory = inventory
        # Pydantic 모델은 mutable하므로 deepcopy를 사용하여 원본 데이터의 변경을 방지합니다.
        # (혹은 scene_data.model_copy(deep=True)를 사용할 수도 있습니다.)
        self.scene_data = copy.deepcopy(scene_data)
        # 장면의 동적 상태를 초기화합니다.
        self.state = self.scene_data.initial_state

    @property
    def scene_id(self) -> str:
        """
        현재 장면의 고유 ID를 반환합니다.
        """
        return self.scene_data.id

    def on_enter(self):
        """
        장면에 진입할 때 실행되는 로직입니다.
        장면 이름 설정, 초기 텍스트 출력, 시야 상태 업데이트 및 진입 액션 실행을 담당합니다.
        """
        self.ui.set_location_name(self.scene_data.name)  # UI에 현재 장면 이름을 설정합니다.
        self.ui.print_narrative(self.scene_data.initial_text, is_markdown=True)  # 초기 설명 텍스트를 출력합니다.
        # 현재 장면의 키워드 상태를 UI에 업데이트하여 시야에 보이는 키워드를 표시합니다.
        self.ui.update_sight_status(self.scene_data.keywords)

        # 장면에 진입할 때 실행될 액션들이 있다면 실행합니다.
        if self.scene_data.on_enter_actions:
            self._execute_actions(self.scene_data.on_enter_actions)

    def on_redisplay(self):
        """
        현재 장면을 다시 표시할 때 실행되는 로직입니다.
        주로 '둘러보기' 명령 시 사용되며, 시스템 메시지와 초기 텍스트를 다시 출력합니다.
        """
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        self.ui.print_narrative(self.scene_data.initial_text, is_markdown=True)

    def resolve_alias(self, keyword: str) -> str:
        """
        주어진 키워드가 별칭(Alias)인 경우, 실제 대상 키워드를 찾아 반환합니다.
        별칭이 아니거나 찾을 수 없으면 원래 키워드를 반환합니다.

        Args:
            keyword (str): 사용자가 입력한 키워드.

        Returns:
            str: 실제 대상 키워드 또는 원래 키워드.
        """
        cmd_lower = keyword.lower()
        for k, v in self.scene_data.keywords.items():
            if k.lower() == cmd_lower:
                # 키워드가 별칭 타입인 경우, target을 반환하고 없으면 원래 키워드를 반환합니다.
                if v.type == KeywordType.ALIAS:
                    return v.target or k
                return k  # 별칭이 아니면 해당 키워드를 반환합니다.
        return keyword  # 일치하는 키워드가 없으면 원래 키워드를 반환합니다.

    async def process_keyword(self, keyword: str) -> bool:
        """
        사용자가 입력한 단일 키워드를 처리합니다.
        키워드의 별칭을 해석하고, 상호작용 조건에 따라 액션을 실행하거나 설명을 출력합니다.

        Args:
            keyword (str): 사용자가 입력한 키워드.

        Returns:
            bool: 키워드 처리에 성공했으면 True, 아니면 False.
        """
        original_keyword = self.resolve_alias(keyword)  # 별칭을 실제 키워드로 해석합니다.
        keyword_data = self.scene_data.keywords.get(original_keyword)  # 키워드 데이터를 가져옵니다.

        if not keyword_data:
            return False  # 해당 키워드가 없으면 처리 실패.

        if keyword_data.state == KeywordState.INACTIVE:
            return False  # 키워드가 비활성 상태이면 처리 실패.

        # 키워드를 발견 상태로 업데이트하고 UI에 반영합니다.
        self._discover_keyword(original_keyword, silent=keyword_data.silent_discovery)

        # 키워드에 정의된 상호작용(interactions)을 순회하며 조건을 확인합니다.
        if keyword_data.interactions:
            for interaction in keyword_data.interactions:
                if self._check_conditions(interaction.conditions):  # 조건이 충족되면
                    self._execute_actions(interaction.actions)  # 해당 액션들을 실행합니다.
                    return True  # 상호작용 처리 성공.

        # 상호작용이 없거나 조건이 충족되지 않았지만 설명이 있다면 설명을 출력합니다.
        if keyword_data.description:
            self.ui.print_narrative(keyword_data.description, is_markdown=True)
            return True  # 설명 출력 성공.

        return True  # 키워드 자체는 유효하므로 True 반환 (아무 액션도 없어도).

    async def process_combination(self, item1: str, item2: str) -> bool:
        """
        두 개의 키워드(아이템 + 대상 등) 조합을 처리합니다.
        장면에 정의된 조합(combinations)을 확인하고, 조건이 충족되면 액션을 실행합니다.

        Args:
            item1 (str): 첫 번째 키워드.
            item2 (str): 두 번째 키워드.

        Returns:
            bool: 조합 처리에 성공했으면 True, 아니면 False.
        """
        combinations = self.scene_data.combinations  # 현재 장면의 모든 조합 데이터를 가져옵니다.
        r_item1 = self.resolve_alias(item1)  # 첫 번째 키워드의 별칭을 해석합니다.
        r_item2 = self.resolve_alias(item2)  # 두 번째 키워드의 별칭을 해석합니다.

        for combo in combinations:
            targets = combo.targets
            if len(targets) != 2:  # 조합은 항상 두 개의 대상을 가집니다.
                continue

            # 입력된 두 키워드와 조합의 대상 키워드를 소문자 집합으로 만들어 순서에 상관없이 비교합니다.
            input_set = {str(r_item1).lower(), str(r_item2).lower()}
            target_set = {str(t).lower() for t in targets}

            if input_set == target_set:  # 입력된 키워드가 조합의 대상과 일치하는 경우
                # 조합에 사용된 키워드들이 현재 시야에 보이는지 확인합니다.
                if not self._check_keyword_visible(r_item1) or not self._check_keyword_visible(r_item2):
                    return False  # 보이지 않는 키워드라면 처리 실패.

                if self._check_conditions(combo.conditions):  # 조합의 조건이 충족되면
                    self._execute_actions(combo.actions)  # 해당 액션들을 실행합니다.
                    return True  # 조합 처리 성공.

        return False  # 일치하는 조합이 없으면 처리 실패.

    def _check_keyword_visible(self, keyword: str) -> bool:
        """
        주어진 키워드가 현재 플레이어에게 보이는 상태인지 확인합니다.
        인벤토리에 있거나, 장면 키워드 중 HIDDEN 상태가 아니면 보이는 것으로 간주합니다.

        Args:
            keyword (str): 확인할 키워드.

        Returns:
            bool: 키워드가 보이면 True, 아니면 False.
        """
        # 키워드가 인벤토리에 있으면 항상 보이는 것으로 간주합니다.
        if self.inventory.has(keyword):
            return True

        # 키워드가 현재 장면의 키워드 목록에 없으면 보이는 것으로 간주합니다 (예: 일반 명사).
        if keyword not in self.scene_data.keywords:
            return True

        k_data = self.scene_data.keywords[keyword]
        # 별칭 타입 키워드는 항상 보이는 것으로 간주합니다.
        if k_data.type == KeywordType.ALIAS:
            return True

        # 키워드가 HIDDEN 상태이면 보이지 않는 것으로 간주합니다.
        if k_data.state == KeywordState.HIDDEN:
            return False

        return True  # 그 외의 경우는 보이는 것으로 간주합니다.

    def _discover_keyword(self, keyword_name: str, silent: bool = False):
        """
        키워드를 '발견됨' 상태로 변경하고, 필요하면 UI에 발견 메시지를 출력합니다.

        Args:
            keyword_name (str): 발견할 키워드의 이름.
            silent (bool): True면 발견 메시지를 출력하지 않습니다.
        """
        data = self.scene_data.keywords.get(keyword_name)
        # 키워드가 존재하고 HIDDEN 상태일 경우에만 처리합니다.
        if data and data.state == KeywordState.HIDDEN:
            data.state = KeywordState.DISCOVERED  # 상태를 DISCOVERED로 변경합니다.
            self.ui.update_sight_status(self.scene_data.keywords)  # UI의 시야 상태를 업데이트합니다.
            if not silent:  # silent 모드가 아닐 경우 발견 메시지를 출력합니다.
                self.ui.print_system_message(
                    f"**[{keyword_name}]**{get_josa(str(keyword_name), '을/를')} 발견하여 **시야**에 추가합니다.",
                    is_markdown=True,
                )

    def _check_conditions(self, conditions: list) -> bool:
        """
        주어진 조건 목록을 모두 확인하여 모든 조건이 충족되는지 검사합니다.

        Args:
            conditions (list): Condition 객체들의 리스트.

        Returns:
            bool: 모든 조건이 충족되면 True, 하나라도 충족되지 않으면 False.
        """
        if not conditions:
            return True  # 조건 목록이 비어있으면 항상 True를 반환합니다.
        for cond in conditions:
            # Pydantic 모델이므로 .type, .target, .value 속성으로 접근합니다.
            handler = CONDITION_HANDLERS.get(cond.type)  # 조건 타입에 맞는 핸들러를 가져옵니다.
            # 핸들러가 존재하고 조건 검사에 실패하면 False를 반환합니다.
            if handler and not handler.check(self, cond.target, cond.value):
                return False
        return True  # 모든 조건이 충족되면 True를 반환합니다.

    def _execute_actions(self, actions: list):
        """
        주어진 액션 목록을 순차적으로 실행합니다.

        Args:
            actions (list): Action 객체들의 리스트.
        """
        for action in actions:
            # Pydantic 모델이므로 .type, .value 속성으로 접근합니다.
            handler = ACTION_HANDLERS.get(action.type)  # 액션 타입에 맞는 핸들러를 가져옵니다.
            if handler:
                handler.execute(self, action.value)  # 핸들러를 통해 액션을 실행합니다.
