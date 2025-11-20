from abc import ABC, abstractmethod
from ui import get_josa


class Scene(ABC):
    """모든 장면의 기반이 되는 추상 클래스입니다."""

    def __init__(self, game, ui, inventory, scene_data):
        self.game = game
        self.ui = ui
        self.inventory = inventory
        # scene_data를 깊은 복사하여 원본 데이터가 수정되지 않도록 함
        import copy

        self.scene_data = copy.deepcopy(scene_data)
        self.state = {}
        self._initialize_state()

    def resolve_alias(self, keyword: str) -> str:
        """키워드가 별칭인 경우 원본 키워드를 반환하고, 그렇지 않으면 원래 키워드를 반환합니다."""
        # 소문자로 일관성 있게 처리
        keyword_lower = keyword.lower()
        for k, v in self.scene_data["keywords"].items():
            if k.lower() == keyword_lower:
                if v.get("type") == "Alias":
                    return v.get("target", keyword)
                return k  # 원본 키워드의 원래 대소문자를 반환
        return keyword  # 일치하는 키워드가 없으면 원본 입력 반환

    def match_pair(self, part1: str, part2: str, target1: str, target2: str) -> bool:
        """두 쌍의 문자열이 순서에 상관없이 일치하는지 확인합니다. 별칭을 자동으로 처리합니다."""
        p1 = self.resolve_alias(part1)
        p2 = self.resolve_alias(part2)
        t1 = self.resolve_alias(target1)
        t2 = self.resolve_alias(target2)
        return (p1.lower() == t1.lower() and p2.lower() == t2.lower()) or (
            p1.lower() == t2.lower() and p2.lower() == t1.lower()
        )

    def _discover_keyword(self, keyword_name: str, show_sight_widened_message: bool = False) -> bool:
        """
        새로운 키워드를 발견 처리하고 관련 메시지를 출력합니다.
        키워드가 새로 발견되었으면 True를 반환합니다.
        """
        # resolve_alias를 통해 원본 키워드 이름을 가져옴
        original_keyword = self.resolve_alias(keyword_name)
        keyword_data = self.scene_data["keywords"].get(original_keyword)

        if keyword_data and keyword_data.get("state") == "hidden":
            keyword_data["state"] = None  # 'hidden'이 아닌 상태로 변경
            self.ui.update_sight_status(self.scene_data["keywords"])
            self.ui.print_system_message(
                f"**[{original_keyword}]**{get_josa(original_keyword, '을/를')} 발견하여 **시야**에 추가합니다.",
                is_markdown=True,
            )
            if show_sight_widened_message:
                self.ui.print_system_message("시야가 넓어진 것 같다.", is_markdown=True)
            return True
        return False

    async def handle_combination(self, item1: str, item2: str) -> bool:
        """
        process_combination의 래퍼. 조합 전에 발견되지 않은 키워드가 있는지 확인합니다.
        """
        resolved_item1 = self.resolve_alias(item1)
        resolved_item2 = self.resolve_alias(item2)

        # 조합에 사용된 키워드가 'hidden' 상태인지 확인
        keyword1_data = self.scene_data["keywords"].get(resolved_item1)
        if keyword1_data and keyword1_data.get("state") == "hidden":
            return False  # 발견되지 않았으면 "아무 일도 일어나지 않았습니다" 출력

        keyword2_data = self.scene_data["keywords"].get(resolved_item2)
        if keyword2_data and keyword2_data.get("state") == "hidden":
            return False  # 발견되지 않았으면 "아무 일도 일어나지 않았습니다" 출력

        # 검사를 통과하면 실제 조합 로직 호출
        return await self.process_combination(item1, item2)

    @property
    @abstractmethod
    def scene_id(self) -> str:
        """각 장면의 고유 ID를 반환합니다."""
        pass

    def on_enter(self):
        """장면에 처음 진입했을 때 호출됩니다."""
        self.ui.set_location_name(self.scene_data["name"])
        self.ui.print_narrative(self.scene_data["initial_text"], is_markdown=True)
        self.ui.update_sight_status(self.scene_data["keywords"])
        self.run_enter_logic()

    def on_redisplay(self):
        """사용자가 '둘러보기'를 입력했을 때 호출됩니다."""
        self.ui.print_system_message("주변을 다시 둘러봅니다.", is_markdown=True)
        self.ui.print_narrative(self.scene_data["initial_text"], is_markdown=True)

    @abstractmethod
    def _initialize_state(self):
        """장면의 내부 상태를 초기화합니다."""
        pass

    def run_enter_logic(self):
        """장면 진입 시 실행될 추가적인 로직 (선택 사항)."""
        pass

    @abstractmethod
    async def process_keyword(self, keyword: str) -> bool:
        """
        키워드 입력을 처리합니다.
        처리되었으면 True, 아니면 False를 반환합니다.
        """
        pass

    @abstractmethod
    async def process_combination(self, item1: str, item2: str) -> bool:
        """
        아이템 조합을 처리합니다.
        처리되었으면 True, 아니면 False를 반환합니다.
        """
        pass
