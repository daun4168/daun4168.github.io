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

    def _discover_keyword(self, keyword_name: str, show_sight_widened_message: bool = False) -> bool:
        """
        새로운 키워드를 발견 처리하고 관련 메시지를 출력합니다.
        키워드가 새로 발견되었으면 True를 반환합니다.
        """
        keyword_data = self.scene_data["keywords"].get(keyword_name)
        if keyword_data and keyword_data.get("state") == "hidden":
            keyword_data["state"] = "discovered"
            self.ui.update_sight_status(self.scene_data["keywords"])
            self.ui.print_system_message(f"**[{keyword_name}]**{get_josa(keyword_name, '을/를')} 발견하여 **시야**에 추가합니다.", is_markdown=True)
            if show_sight_widened_message:
                self.ui.print_system_message("시야가 넓어진 것 같다.", is_markdown=True)
            return True
        return False

    @property
    @abstractmethod
    def scene_id(self) -> str:
        """각 장면의 고유 ID를 반환합니다."""
        pass

    def on_enter(self):
        """장면에 처음 진입했을 때 호출됩니다."""
        self.ui.set_location_name(self.scene_data["name"])
        self.game.update_health_status()
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
