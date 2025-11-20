from scene import Scene
from ui import get_josa
from entity import Item


class Scene1(Scene):
    DATA = {
        "name": "제 2 연구실",
        "initial_text": "문을 열자 퀴퀴한 곰팡이 냄새와 먼지가 뒤섞여 코를 찌른다. 이곳은 신성한 연구실인가, 고고학 발굴 현장인가.\n\n구석에는 정체를 알 수 없는 쓰레기통이 넘칠 듯이 차 있고, 벽 한쪽에는 굳게 닫힌 시약장과 낡은 박스들이 산더미처럼 쌓여 있다.\n먼지 쌓인 오래된 컴퓨터는 켜지기는 할지 의문이며, 바닥에는 정체불명의 의문의 액체가 흥건하다. 그 옆에 빗자루가 굴러다닌다.",
        "keywords": {
            "쓰레기통": {"type": "Object", "state": "hidden"},
            "박스": {"type": "Object", "state": "hidden"},
            "빗자루": {"type": "Object", "state": "hidden"},
            "오래된 컴퓨터": {"type": "Object", "state": "hidden"},
            "의문의 액체": {"type": "Object", "state": "hidden"},
            "시약장": {"type": "Object", "state": "hidden"},
            "바닥": {"type": "Object", "state": "hidden"},
            "벽": {"type": "Object", "state": "hidden"},
            # '메모'는 동적으로 추가되므로 여기서 제외
            "벽면": {"type": "Alias", "target": "벽"},
            "문": {"type": "Object", "state": "hidden"},
            "컴퓨터": {"type": "Alias", "target": "오래된 컴퓨터"},
        },
    }

    @property
    def scene_id(self) -> str:
        return "scene1"

    def _initialize_state(self):
        self.state.update(
            {
                "is_liquid_cleaned": False,
                "trash_can_state": "initial",
                "wall_state": "initial",
                "combination_tutorial_shown": False,
                "keyword_tutorial_shown": False,
            }
        )

    async def process_keyword(self, keyword: str) -> bool:
        cmd_lower = keyword.lower()

        for keyword_name, keyword_data in self.scene_data["keywords"].items():
            is_alias = keyword_data.get("type") == "Alias"
            target_name = keyword_data.get("target", "").lower()

            if cmd_lower == keyword_name.lower() or (is_alias and cmd_lower == target_name):
                original_keyword_name = target_name if is_alias else keyword_name

                original_data = self.scene_data["keywords"].get(original_keyword_name)
                if not original_data:
                    return False  # 키워드가 없으면 무시

                # 숨겨진 키워드는 직접 상호작용 불가 (단, '벽'처럼 다른 키워드를 드러내는 경우는 예외)
                if original_data.get("state") == "hidden" and original_keyword_name not in ["벽", "메모"]:
                    return False

                # '벽'과 '메모'가 아닌 다른 키워드들은 발견 시 일반 메시지만 출력
                if original_keyword_name not in ["벽", "메모"]:
                    self._discover_keyword(original_keyword_name)

                if original_keyword_name == "벽":
                    self._discover_keyword("벽")
                    if self.state["wall_state"] == "initial":
                        self.ui.print_narrative("벽지를 자세히 보니, 구석에 작은 메모가 붙어있다.", is_markdown=True)
                        self.state["wall_state"] = "discovered"

                        # '메모' 키워드를 hidden 상태로 추가하여 [?]가 나타나게 함
                        self.scene_data["keywords"]["메모"] = {"type": "Object", "state": "hidden"}
                        self.ui.update_sight_status(self.scene_data["keywords"])

                        self.ui.print_system_message("시야에 무언가 새로운 것이 포착되었다.", is_markdown=True)

                        if not self.state.get("keyword_tutorial_shown"):
                            self.ui.print_system_message(
                                "새롭게 발견한 것은 관련된 키워드를 입력하여 조사할 수 있습니다.", is_markdown=True
                            )
                            self.state["keyword_tutorial_shown"] = True
                    else:
                        self.ui.print_narrative("구석에 작은 메모가 붙어있다.", is_markdown=True)

                elif original_keyword_name == "메모":
                    # '메모' 키워드를 발견 처리하고, 특별 메시지를 함께 출력
                    is_newly_discovered = self._discover_keyword("메모", show_sight_widened_message=True)

                    # 새로 발견했든 아니든 내용을 보여줌
                    self.ui.print_narrative(
                        "벽에 붙어있는 메모에는 '컴퓨터 비밀번호: 1에서 시작하고 8로 끝나는 여덟자리 숫자' 라고 적혀있다.",
                        is_markdown=True,
                    )

                elif original_keyword_name == "쓰레기통":
                    # (이하 다른 키워드 로직은 동일)
                    trash_state = self.state["trash_can_state"]
                    if trash_state == "initial":
                        self.ui.print_narrative(
                            "쓰레기통을 뒤적거리자, 먹다 남은 **[에너지바 껍질]**을 찾았다. 쓰레기 더미 아래에 무언가 더 있는 것 같다.",
                            is_markdown=True,
                        )
                        if not self.inventory.has("에너지바 껍질"):
                            self.inventory.add(Item("에너지바 껍질", "눅눅하고 비어있다."))
                        self.ui.print_system_message("`쓰레기통`을 다시 한번 입력해 보세요.", is_markdown=True)
                        self.state["trash_can_state"] = "searched_once"
                    elif trash_state == "searched_once":
                        self.ui.print_narrative(
                            "다시 한번 쓰레기통을 뒤지자, 깊숙한 곳에서 녹슨 **[스패너]**를 발견했다. 이제 쓰레기통은 완전히 비었다.",
                            is_markdown=True,
                        )
                        if not self.inventory.has("스패너"):
                            self.inventory.add(Item("스패너", "녹슬었지만 쓸만해 보인다."))
                        self.state["trash_can_state"] = "empty"
                    else:  # empty
                        self.ui.print_narrative("텅 빈 쓰레기통이다. 더는 아무것도 나오지 않는다.", is_markdown=True)

                elif original_keyword_name == "박스":
                    if self.scene_data["keywords"]["박스"].get("state") == "opened":
                        self.ui.print_narrative("안에는 아무것도 없는 빈 박스다.", is_markdown=True)
                    else:
                        self.ui.print_narrative(
                            "테이프로 칭칭 감겨 있다. 손톱으로는 뜯을 수 없을 것 같다. 날카로운 게 필요하다.",
                            is_markdown=True,
                        )
                        if not self.state["combination_tutorial_shown"]:
                            self.ui.print_system_message(
                                "새로운 상호작용을 위해 `+` 기호를 사용할 수 있습니다. **주머니**의 아이템과 **시야**의 **[키워드]**를 조합해 보세요. 아이템끼리, 혹은 키워드끼리 조합하는 것도 가능합니다.\n예시: `법인카드 + 박스`",
                                is_markdown=True,
                            )
                            self.state["combination_tutorial_shown"] = True

                elif original_keyword_name == "실험용 랩 가운":
                    self.ui.print_narrative(
                        "새하얀 랩 가운이다. 입으면 왠지 졸업에 한 발짝 다가간 기분이 든다.", is_markdown=True
                    )
                elif original_keyword_name == "빗자루":
                    self.ui.print_narrative("평범한 빗자루다. 바닥을 청소할 수 있을 것 같다.", is_markdown=True)
                elif original_keyword_name == "오래된 컴퓨터":
                    if self.scene_data["keywords"]["오래된 컴퓨터"].get("state") != "solved":
                        self.ui.print_narrative(
                            "전원 버튼을 누르자, 잠시 팬이 돌다가 암호 입력창이 뜬다.", is_markdown=True
                        )
                        self.ui.print_system_message(
                            "암호를 알아내어 `컴퓨터 + [비밀번호]` 형식으로 입력해야 할 것 같다.", is_markdown=True
                        )
                    else:
                        self.ui.print_system_message("컴퓨터 화면에는 `시약장 비밀번호: 0815` 라는 메모만 띄워져 있다.")
                elif original_keyword_name == "시약장":
                    self.ui.print_narrative("자물쇠가 걸려있다.", is_markdown=True)
                    self.ui.print_system_message(
                        "비밀번호를 알아내서 `시약장 + [비밀번호]` 형식으로 입력해야 할 것 같다.", is_markdown=True
                    )
                elif original_keyword_name == "의문의 액체":
                    self.ui.print_narrative(
                        "바닥에 끈적하게 눌어붙은 액체다. 무슨 성분인지 알 수 없지만, 달콤한 향이 나는 것 같다. 핥아볼까?",
                        is_markdown=True,
                    )
                elif original_keyword_name == "바닥":
                    self.ui.print_narrative(
                        "바닥 한쪽에 **[의문의 액체]**가 흥건하다. 끈적해서 밟고 싶지 않다.", is_markdown=True
                    )
                elif original_keyword_name == "문":
                    self.ui.print_narrative(
                        "이미 끔찍한 곳에 와있는데, 굳이 돌아갈 필요는 없어 보인다.", is_markdown=True
                    )
                else:
                    pass

                return True
        return False

    async def process_combination(self, item1: str, item2: str) -> bool:
        # 성공 조합
        if self.match_pair(item1, item2, "컴퓨터", "12345678"):
            self.ui.print_narrative(
                "암호가 맞았다! 컴퓨터 화면에 메모장 파일 하나가 띄워져 있다.\n\n`시약장 비밀번호: 내 생일 (0815)`",
                is_markdown=True,
            )
            self.scene_data["keywords"]["오래된 컴퓨터"]["state"] = "solved"
            return True

        if self.match_pair(item1, item2, "시약장", "0815"):
            self.ui.print_narrative(
                "철컥, 소리와 함께 **[시약장]** 문이 열렸다. 안에서 **[에탄올]** 병을 발견했다.", is_markdown=True
            )
            if not self.inventory.has("에탄올"):
                self.inventory.add(Item("에탄올", "소독 및 청소용. 마시지 마시오."))
            if "시약장" in self.scene_data["keywords"]:
                del self.scene_data["keywords"]["시약장"]
            self.ui.update_sight_status(self.scene_data["keywords"])
            return True

        if self.match_pair(item1, item2, "박스", "법인카드"):
            if self.inventory.has("법인카드"):
                self.ui.print_narrative(
                    "**[법인카드]** 모서리로 테이프를 잘라냅니다. 안에서 새하얀 **[실험용 랩 가운]**을 발견했습니다!",
                    is_markdown=True,
                )
                self.scene_data["keywords"]["박스"]["state"] = "opened"
                self.scene_data["keywords"]["실험용 랩 가운"] = {"type": "Object", "state": "hidden"}
                self._discover_keyword("실험용 랩 가운")
            else:
                self.ui.print_system_message("**주머니**에 **[법인카드]**가 없습니다.")
            return True

        if self.match_pair(item1, item2, "에탄올", "의문의 액체"):
            if self.inventory.has("에탄올"):
                self.ui.print_narrative(
                    "**[에탄올]**을 붓자, 끈적한 **[의문의 액체]**가 녹아내리며 바닥이 깨끗해졌다!", is_markdown=True
                )
                self.state["is_liquid_cleaned"] = True
                self.inventory.remove("에탄올")
                if "의문의 액체" in self.scene_data["keywords"]:
                    del self.scene_data["keywords"]["의문의 액체"]
                self.ui.update_sight_status(self.scene_data["keywords"])
                self.ui.print_system_message(
                    "이제 **[빗자루]**로 **[바닥]**을 청소할 수 있을 것 같다.", is_markdown=True
                )
            else:
                self.ui.print_system_message("**주머니**에 **[에탄올]**이 없습니다.")
            return True

        if self.match_pair(item1, item2, "빗자루", "바닥"):
            if self.state["is_liquid_cleaned"] and self.state["trash_can_state"] == "empty":
                self.ui.print_narrative("깨끗해진 바닥을 **[빗자루]**로 쓸어 마무리 청소를 합니다...", is_markdown=True)
                self.game.scene_manager.switch_scene("scene2")
            elif not self.state["is_liquid_cleaned"]:
                self.ui.print_narrative(
                    "바닥의 끈적한 **[의문의 액체]** 때문에 **[빗자루]**질을 할 수가 없다. 저걸 먼저 어떻게든 해야 한다.",
                    is_markdown=True,
                )
            else:
                self.ui.print_system_message(
                    "아직 **[쓰레기통]**이 정리되지 않은 것 같다. 마저 치우자.", is_markdown=True
                )
            return True

        # 실패 조합 피드백
        if "컴퓨터" in item1 or "컴퓨터" in item2:
            self.ui.print_system_message("잘못된 암호입니다.")
            return True
        if "시약장" in item1 or "시약장" in item2:
            self.ui.print_system_message("자물쇠가 열리지 않습니다.")
            return True
        if "바닥" in item1 or "바닥" in item2:
            self.ui.print_system_message("**[의문의 액체]**에 직접 사용해야 할 것 같다.", is_markdown=True)
            return True

        return False
