from typing import Dict, Type
from scene import Scene
from ui import get_josa


class SceneFactory:
    """장면(Scene) 인스턴스 생성을 책임지는 팩토리 클래스입니다."""

    def __init__(self, game, ui, inventory):
        self.game = game
        self.ui = ui
        self.inventory = inventory
        self._scene_registry: Dict[str, (Type[Scene], Dict)] = {}

    def register_scene(self, scene_id: str, scene_class: Type[Scene], scene_data: Dict):
        """팩토리에 장면 생성에 필요한 정보를 등록합니다."""
        if not issubclass(scene_class, Scene):
            raise TypeError(f"{scene_class.__name__} is not a subclass of Scene.")
        self._scene_registry[scene_id] = (scene_class, scene_data)

    def create_scene(self, scene_id: str) -> Scene | None:
        """등록된 정보를 바탕으로 장면 인스턴스를 생성합니다."""
        if scene_id not in self._scene_registry:
            print(f"Error: Scene '{scene_id}' is not registered in the factory.")
            return None

        scene_class, scene_data = self._scene_registry[scene_id]
        return scene_class(self.game, self.ui, self.inventory, scene_data)


class SceneManager:
    """장면 전환과 현재 장면의 생명주기를 관리합니다."""

    def __init__(self, scene_factory: SceneFactory, ui):
        self.scene_factory = scene_factory
        self.ui = ui
        self.scenes: Dict[str, Scene] = {}  # 장면 인스턴스 캐시
        self.current_scene: Scene | None = None

    def switch_scene(self, scene_id: str):
        """지정된 ID의 장면으로 전환합니다."""
        if scene_id not in self.scenes:
            scene_instance = self.scene_factory.create_scene(scene_id)
            if not scene_instance:
                self.ui.print_system_message(f"오류: 장면({scene_id})을 생성할 수 없습니다.")
                return
            self.scenes[scene_id] = scene_instance

        self.current_scene = self.scenes[scene_id]
        self.scene_factory.game.current_scene_id = scene_id
        self.current_scene.on_enter()

    def _is_valid_combination_part(self, part: str) -> bool:
        """조합에 사용된 요소가 유효한지(인벤토리 아이템 또는 발견된 키워드) 확인합니다."""
        # 1. 인벤토리에 있는 아이템인가?
        if self.scene_factory.inventory.has(part):
            return True

        # 2. 현재 씬의 발견된 키워드인가?
        if self.current_scene:
            for name, data in self.current_scene.scene_data["keywords"].items():
                # 별명(alias)도 확인
                is_alias = data.get("type") == "Alias"
                target_name = data.get("target", "").lower()

                # 키워드 이름 또는 별명이 일치하고, 상태가 'discovered'인지 확인
                if part == name.lower() or (is_alias and part == target_name):
                    # 원본 키워드 데이터 가져오기
                    original_keyword_name = target_name if is_alias else name
                    original_data = self.current_scene.scene_data["keywords"].get(original_keyword_name, {})
                    if original_data.get("state") == "discovered":
                        return True
        return False

    async def process_command(self, command: str):
        """현재 장면에 명령어를 전달하고 처리합니다."""
        if self.current_scene:
            if "+" in command:
                parts = [p.strip().lower() for p in command.split("+")]
                if len(parts) == 2:
                    part1, part2 = parts
                    # 조합 유효성 검사
                    if not self._is_valid_combination_part(part1):
                        self.ui.print_system_message(f"'{part1}'{get_josa(part1, '은/는')} 사용할 수 없는 대상입니다.")
                        return
                    if not self._is_valid_combination_part(part2):
                        self.ui.print_system_message(f"'{part2}'{get_josa(part2, '은/는')} 사용할 수 없는 대상입니다.")
                        return

                    if not await self.current_scene.process_combination(part1, part2):
                        self.ui.print_system_message("아무 일도 일어나지 않았습니다.")
                else:
                    self.ui.print_system_message("잘못된 조합 형식입니다. `아이템 + 대상` 형식으로 입력해주세요.")
            else:
                if not await self.current_scene.process_keyword(command):
                    josa = get_josa(command, "으로는/로는")
                    self.ui.print_system_message(f"'{command}'{josa} 아무것도 할 수 없습니다.")
        else:
            # 게임 시작 전 등 current_scene이 없을 때의 처리
            if command.lower() == "일어나기":
                self.scene_factory.game._start_game()
            else:
                self.ui.print_system_message("`일어나기`를 입력해야 합니다.")

    def redisplay_current_scene(self):
        """현재 장면을 다시 표시합니다."""
        if self.current_scene:
            self.current_scene.on_redisplay()
