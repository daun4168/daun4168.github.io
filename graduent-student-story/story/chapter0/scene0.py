from scene import Scene
from ui import get_josa
from entity import Item


class Scene0(Scene):
    DATA = {
        "name": "교수님 오피스",
        "initial_text": '눈을 뜨자 익숙한 풍경이 보인다. 책상 위에 쌓인 논문 탑, 그리고 그 뒤에서 번뜩이는 안경알.\n\n"자네, 정신이 드나? 서서 조는 기술이 아주 일취월장했어."\n\n교수님이 혀를 차며 나를 바라본다. 10년째 듣는 잔소리다. 타격감도 없다.\n\n"연구실 제2섹터 청소나 하게. 외부 손님이 온다니까. 필요한 물건 있으면 저기 법인카드 가져가서 사고. 한도는 초과됐지만 포인트는 남았을 거야."\n\n교수님은 턱짓으로 책상을 가리켰다.\n\n"다 챙겼으면 뒤에 있는 문으로 나가. 난 사우나... 아니, 미팅 준비해야 하니까."',
        "keywords": {
            "교수님": {"type": "NPC", "state": "hidden"},
            "법인카드": {"type": "Item", "state": "hidden"},
            "문": {"type": "Portal", "state": "hidden", "target": "scene1"},
            "논문": {"type": "Object", "state": "hidden"},
            "책상": {"type": "Object", "state": "hidden"},
            "안경알": {"type": "Object", "state": "hidden"},
        },
    }

    @property
    def scene_id(self) -> str:
        return "scene0"

    def _initialize_state(self):
        self.state["look_around_tutorial_shown"] = False

    def run_enter_logic(self):
        self.ui.print_system_message(
            "이제부터 상호작용 방식이 바뀝니다. 본문에 등장하는 특정 단어, 즉 **[키워드]**를 직접 입력하여 주변을 탐색할 수 있습니다.\n\n본문을 자세히 읽고 상호작용할 단어를 찾아 입력해 보세요. 발견한 **[키워드]**는 상단의 **시야**에 표시됩니다.\n\n예를 들어, `교수님`을 입력해볼까요?",
            is_markdown=True,
        )

    async def process_keyword(self, keyword: str) -> bool:
        cmd_lower = keyword.lower()

        # '법인카드'는 인벤토리에 없을 때만 특별 처리
        if cmd_lower == "법인카드":
            if not self.inventory.has("법인카드"):
                self.ui.print_system_message("**[법인카드]**를 발견하여 **주머니**에 추가합니다.", is_markdown=True)
                self.ui.print_system_message("어떤 아이템은 이렇게 **주머니**에 보관할 수 있습니다.", is_markdown=True)
                item = Item("법인카드", "긁히지는 않지만 날카로워서 무기나 도구로 쓸 수 있습니다.")
                self.inventory.add(item, silent=True)
                item.show_description()
                if "법인카드" in self.scene_data["keywords"]:
                    del self.scene_data["keywords"]["법인카드"]
                self.ui.update_inventory_status(self.inventory.items)
                self.ui.update_sight_status(self.scene_data["keywords"])
                return True
            # 이미 인벤토리에 있다면, Game 클래스의 공통 로직이 처리하므로 여기서는 False 반환
            return False

        # 일반 키워드 처리
        scene_keywords = self.scene_data["keywords"]
        for keyword_name, keyword_data in scene_keywords.items():
            is_alias = keyword_data.get("type") == "Alias"
            target_name = keyword_data.get("target", "").lower()

            if cmd_lower == keyword_name.lower() or (is_alias and cmd_lower == target_name):
                original_keyword_name = target_name if is_alias else keyword_name
                original_keyword_data = scene_keywords[original_keyword_name] if is_alias else keyword_data

                # 숨겨진 키워드 발견 처리
                if original_keyword_data.get("state") == "hidden":
                    original_keyword_data["state"] = "discovered"
                    self.ui.update_sight_status(scene_keywords)
                    self.ui.print_system_message(
                        f"**[{original_keyword_name}]**{get_josa(original_keyword_name, '을/를')} 발견하여 **시야**에 추가합니다.",
                        is_markdown=True,
                    )

                # 키워드별 로직
                if original_keyword_name == "교수님":
                    self.game.health -= 1
                    self.game.update_health_status()
                    self.ui.print_narrative(
                        "뭘 꾸물거려? 빨리 가서 청소 안 하고! 이번 학기 졸업하기 싫나?", is_markdown=True
                    )
                    if not self.state["look_around_tutorial_shown"]:
                        self.ui.print_system_message(
                            "막혔을 때는 `둘러보기`를 입력하여 주변을 다시 살필 수 있습니다.", is_markdown=True
                        )
                        self.state["look_around_tutorial_shown"] = True
                elif original_keyword_name == "문":
                    if self.inventory.has("법인카드"):
                        self.ui.print_system_message(
                            "문을 나섭니다. 새로운 장소에서는 **시야**가 초기화되지만, **주머니** 속의 물건은 그대로 유지됩니다.",
                            is_markdown=True,
                        )
                        self.game.scene_manager.switch_scene("scene1")
                    else:
                        self.ui.print_system_message(
                            "이 문으로 나갈 수 있을 것 같다. 하지만 아직 무언가 잊은 기분이 든다."
                        )
                elif original_keyword_name == "논문":
                    self.game.health -= 0.5
                    self.game.update_health_status()
                    self.ui.print_narrative(
                        "읽어야 할 논문이 산더미처럼 쌓여있다. 보기만 해도 숨이 막힌다.", is_markdown=True
                    )
                elif original_keyword_name == "책상":
                    self.ui.print_narrative(
                        "교수님의 책상이다. 각종 서류와 논문이 어지럽게 널려있다.", is_markdown=True
                    )
                elif original_keyword_name == "안경알":
                    self.ui.print_narrative(
                        "교수님의 안경알이 빛을 번뜩인다. 저 너머의 눈은 웃고 있는지, 화를 내고 있는지 알 수 없다.",
                        is_markdown=True,
                    )
                else:
                    # 키워드는 존재하지만 특별한 로직이 없는 경우
                    return False

                return True  # 키워드 처리 완료

        return False  # 처리된 키워드가 없음

    async def process_combination(self, item1: str, item2: str) -> bool:
        # scene0에서는 조합 로직이 없음
        return False
