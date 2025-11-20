from const import CommandType, CombinationType
from scene import Scene
from ui import get_josa


class SceneFactory:
    """
    장면(Scene) 인스턴스 생성을 책임지는 팩토리 클래스입니다.
    등록된 장면 데이터를 기반으로 Scene 객체를 생성합니다.
    """

    def __init__(self, game, ui, inventory, player):
        """
        SceneFactory의 생성자입니다.

        Args:
            game: 게임의 메인 인스턴스 (Game 클래스).
            ui: 사용자 인터페이스 관리 객체 (UIManager).
            inventory: 플레이어의 인벤토리 객체 (Inventory).
            player: 플레이어 객체 (Player).
        """
        self.game = game
        self.ui = ui
        self.inventory = inventory
        self.player = player
        # _scene_registry는 장면 ID를 키로, (장면 클래스, 장면 데이터) 튜플을 값으로 저장합니다.
        self._scene_registry: dict[str, (type[Scene], dict)] = {}

    def register_scene(self, scene_id: str, scene_class: type[Scene], scene_data: dict):
        """
        팩토리에 장면 생성에 필요한 정보를 등록합니다.

        Args:
            scene_id (str): 장면을 식별하는 고유 ID.
            scene_class (Type[Scene]): 해당 장면을 생성할 Scene 클래스.
            scene_data (Dict): 해당 장면의 초기 데이터를 담은 딕셔너리.

        Raises:
            TypeError: scene_class가 Scene 클래스의 서브클래스가 아닐 경우 발생합니다.
        """
        # 등록하려는 클래스가 Scene의 서브클래스인지 확인합니다.
        if not issubclass(scene_class, Scene):
            raise TypeError(f"{scene_class.__name__} is not a subclass of Scene.")
        self._scene_registry[scene_id] = (scene_class, scene_data)

    def create_scene(self, scene_id: str) -> Scene | None:
        """
        등록된 정보를 바탕으로 장면 인스턴스를 생성합니다.

        Args:
            scene_id (str): 생성할 장면의 ID.

        Returns:
            Scene | None: 생성된 Scene 인스턴스 또는 등록되지 않은 ID일 경우 None.
        """
        # 요청된 scene_id가 팩토리에 등록되어 있는지 확인합니다.
        if scene_id not in self._scene_registry:
            print(f"Error: Scene '{scene_id}' is not registered in the factory.")
            return None

        # 등록된 장면 클래스와 데이터를 가져옵니다.
        scene_class, scene_data = self._scene_registry[scene_id]

        # Scene 인스턴스를 생성하여 반환합니다.
        # [수정] player 인자 전달 확인
        return scene_class(self.game, self.ui, self.inventory, self.player, scene_data)


class SceneManager:
    """
    장면 전환과 현재 장면의 생명주기를 관리합니다.
    게임의 현재 상태를 나타내는 장면을 관리하고, 사용자 명령을 현재 장면에 전달합니다.
    """

    def __init__(self, scene_factory: SceneFactory, ui):
        """
        SceneManager의 생성자입니다.

        Args:
            scene_factory (SceneFactory): 장면 인스턴스 생성을 위한 팩토리 객체.
            ui: 사용자 인터페이스 관리 객체 (UIManager).
        """
        self.scene_factory = scene_factory
        self.ui = ui
        # 장면 인스턴스를 캐시하여 불필요한 재생성을 방지합니다.
        self.scenes: dict[str, Scene] = {}
        # 현재 활성화된 장면 인스턴스입니다.
        self.current_scene: Scene | None = None

    def switch_scene(self, scene_id: str):
        """
        지정된 ID의 장면으로 전환합니다.
        새로운 장면이 아직 생성되지 않았다면 팩토리를 통해 생성하고 캐시합니다.
        새로운 장면의 on_enter 메서드를 호출하여 장면 진입 로직을 실행합니다.

        Args:
            scene_id (str): 전환할 장면의 ID.
        """
        # 요청된 장면이 캐시에 있는지 확인합니다.
        if scene_id not in self.scenes:
            # 캐시에 없으면 팩토리를 통해 장면 인스턴스를 생성합니다.
            scene_instance = self.scene_factory.create_scene(scene_id)
            if not scene_instance:
                # 장면 생성에 실패하면 시스템 메시지를 출력하고 종료합니다.
                self.ui.print_system_message(f"오류: 장면({scene_id})을 생성할 수 없습니다.")
                return

            # 생성된 장면 인스턴스를 캐시에 저장합니다.
            self.scenes[scene_id] = scene_instance

        # 현재 장면을 새로 전환할 장면으로 설정합니다.
        self.current_scene = self.scenes[scene_id]
        # 새로운 장면의 진입 로직을 실행합니다.
        self.current_scene.on_enter()

    # [추가] 장면 초기화 메서드
    def reset_scene(self, scene_id: str):
        """
        지정된 장면을 캐시에서 제거하여, 다음 진입 시 초기 상태로 새로 생성되게 합니다.
        체크포인트 로드 시 사용됩니다.
        """
        if scene_id in self.scenes:
            del self.scenes[scene_id]

    async def process_command(self, command: str):
        """
        사용자 명령을 처리합니다. 기호에 따라 조합 타입을 구분합니다.
        """
        if self.current_scene:
            # 1. 비밀번호 입력 처리 (콜론 ':' 사용) -> Type: PASSWORD
            if ":" in command:
                parts = [p.strip().lower() for p in command.split(":")]
                if len(parts) == 2:
                    part1, part2 = parts

                    # [수정] process_combination 호출 시 match_type을 PASSWORD로 지정
                    success = await self.current_scene.process_combination(
                        part1, part2, match_type=CombinationType.PASSWORD
                    )

                    if not success:
                        # 실패 시 피드백 (첫 번째 제안 반영)
                        self.ui.print_system_message("비밀번호가 일치하지 않거나, 대상을 찾을 수 없습니다.")
                else:
                    self.ui.print_system_message("잘못된 입력 형식입니다. `대상 : 비밀번호` 형식으로 입력해주세요.")
                return

            # 2. 아이템 조합 명령 처리 (더하기 '+' 사용) -> Type: DEFAULT
            if "+" in command:
                parts = [p.strip().lower() for p in command.split("+")]
                if len(parts) == 2:
                    part1, part2 = parts

                    # [수정] process_combination 호출 시 match_type을 DEFAULT로 지정 (기본값)
                    success = await self.current_scene.process_combination(
                        part1, part2, match_type=CombinationType.DEFAULT
                    )

                    if not success:
                        self.ui.print_system_message("아무 일도 일어나지 않았습니다.")
                else:
                    self.ui.print_system_message("잘못된 조합 형식입니다. `아이템 + 대상` 형식으로 입력해주세요.")
                return

            # 3. 일반 키워드 명령 처리 (기존과 동일)
            if not await self.current_scene.process_keyword(command):
                josa = get_josa(command, "으로는/로는")
                self.ui.print_system_message(f"'{command}'{josa} 아무것도 할 수 없습니다.")

        else:
            # 게임 시작 전 (기존과 동일)
            if command.lower() == CommandType.WAKE_UP:
                self.scene_factory.game.start_game()
            else:
                self.ui.print_system_message(f"`{CommandType.WAKE_UP}`를 입력해야 합니다.")

    def redisplay_current_scene(self):
        """
        현재 장면을 다시 표시합니다.
        주로 '둘러보기' 명령 시 현재 장면의 초기 텍스트와 키워드를 다시 출력하는 데 사용됩니다.
        """
        if self.current_scene:
            self.current_scene.on_redisplay()
