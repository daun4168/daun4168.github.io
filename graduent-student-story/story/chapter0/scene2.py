from scene import Scene
from ui import get_josa


class Ch0Scene2(Scene):
    DATA = {
        "name": "제 2 연구실 (청소 완료)",
        "initial_text": '청소를 마치자마자 교수님이 땀을 뻘뻘 흘리며 거대한 기계를 들고 들어왔습니다.\n\n"자, 이게 내 역작 MK-II야. 배송비를 아껴줄 초공간 양자 전송 장치지. 해외 직구 배송비가 너무 비싸서 직접 만들었어."\n\n교수는 전선을 대충 콘센트에 꽂더니 나를 쳐다봅니다. 기계에서 불안한 웅웅 소리가 납니다.\n\n"테스트하게 저기 탑승구로 들어가. 자네 몸무게가 쌀 한 가마니랑 비슷하니까 딱이야."',
        "keywords": {
            "교수님": {"type": "NPC", "state": "hidden"},
            "MK-II": {"type": "Object", "state": "hidden"},
            "탑승구": {"type": "Object", "state": "hidden"},
            "콘센트": {"type": "Object", "state": "hidden"},
            "전선": {"type": "Object", "state": "hidden"},
        },
    }

    @property
    def scene_id(self) -> str:
        return "ch0scene2"

    def _initialize_state(self):
        self.state.update({"professor_called_out": False, "card_returned": False})

    async def process_keyword(self, keyword: str) -> bool:
        cmd_lower = keyword.lower()
        scene_keywords = self.scene_data["keywords"]

        for keyword_name, keyword_data in scene_keywords.items():
            is_alias = keyword_data.get("type") == "Alias"
            target_name = keyword_data.get("target", "").lower()

            if cmd_lower == keyword_name.lower() or (is_alias and cmd_lower == target_name):
                original_keyword_name = target_name if is_alias else keyword_name

                self._discover_keyword(original_keyword_name)

                if original_keyword_name == "교수님":
                    if self.state["professor_called_out"] and not self.state["card_returned"]:
                        self.ui.print_narrative(
                            '교수님: "**[법인카드]**는 놓고 가게!" 교수님이 나를 빤히 쳐다본다.', is_markdown=True
                        )
                    elif self.state["card_returned"]:
                        self.ui.print_narrative(
                            "교수님은 이미 **[법인카드]**를 받아갔다. 이제 **[탑승구]**를 조이는 일만 남았다.",
                            is_markdown=True,
                        )
                    else:
                        self.ui.print_narrative(
                            '교수님: "뭘 꾸물거려? 어서 **[탑승구]**로 들어가! 아, 그리고 그거 좀 뻑뻑하던데, 알아서 잘 조이고. 공대생이 그정돈 하겠지?"',
                            is_markdown=True,
                        )

                elif original_keyword_name == "MK-II":
                    self.ui.print_narrative(
                        "교수님의 역작 **[MK-II]**다. 초공간 양자 전송 장치라는데, 전선 마감이 청테이프인 것이 불안하다. **[탑승구]** 쪽 경첩이 덜 조여진 것처럼 보인다.",
                        is_markdown=True,
                    )
                    if self.inventory.has("스패너"):
                        self.ui.print_system_message(
                            "**[스패너]**로 대충 고쳐볼까 했지만, 더 망가뜨릴 것 같다.", is_markdown=True
                        )

                elif original_keyword_name == "탑승구":
                    self.ui.print_narrative(
                        "육중한 해치다. 경첩이 헐거워 제대로 닫히지 않을 것 같다. **주머니**에 있는 **[스패너]**로 조이면 될 것 같다.",
                        is_markdown=True,
                    )

                elif original_keyword_name == "콘센트":
                    self.ui.print_narrative(
                        "벽에 꽂힌 **[MK-II]**의 **[콘센트]**다. 헐거워 보이지만, 건드리면 큰일 날 것 같다.",
                        is_markdown=True,
                    )

                elif original_keyword_name == "전선":
                    self.ui.print_narrative(
                        "청테이프로 대충 감아놓은 **[전선]**이다. 교수님의 공학적 감각은 일반인의 상식을 뛰어넘는다.",
                        is_markdown=True,
                    )

                else:
                    return False

                return True
        return False

    async def process_combination(self, item1: str, item2: str) -> bool:
        if self.match_pair(item1, item2, "탑승구", "스패너"):
            if self.inventory.has("스패너"):
                if not self.state["professor_called_out"]:
                    self.ui.print_narrative(
                        "**[스패너]**로 **[탑승구]**의 뻑뻑한 부분을 조이려 하자, 갑자기 교수님이 나를 부른다.",
                        is_markdown=True,
                    )
                    self.ui.print_system_message('교수님: "자네, **[법인카드]**는 놓고 가게!"')
                    self.state["professor_called_out"] = True
                elif self.state["card_returned"]:
                    self.ui.print_narrative(
                        "**[스패너]**로 **[탑승구]**를 단단히 조였다. 이제 정말 출발할 시간이다!", is_markdown=True
                    )
                    self.ui.print_system_message(
                        "프롤로그가 성공적으로 마무리되었습니다. 이 게임은 여기까지 완성되었습니다. 플레이해주셔서 감사합니다!",
                        is_markdown=True,
                    )
                    self.game.user_input.disabled = True
                    self.game.submit_button.disabled = True
                else:
                    self.ui.print_system_message(
                        "교수님이 **[법인카드]**를 놓고 가라고 한다. **[교수님]**에게 **[법인카드]**를 전달해야 할 것 같다.",
                        is_markdown=True,
                    )
            else:
                self.ui.print_system_message(
                    "**주머니**에 **[스패너]**가 없습니다. **[탑승구]**를 조일 수 없습니다.", is_markdown=True
                )
            return True

        if self.match_pair(item1, item2, "교수님", "법인카드"):
            if self.state["professor_called_out"] and not self.state["card_returned"]:
                if self.inventory.has("법인카드"):
                    self.ui.print_narrative(
                        "교수님께 **[법인카드]**를 건네자, 교수님은 만족스러운 표정으로 고개를 끄덕인다.",
                        is_markdown=True,
                    )
                    self.inventory.remove("법인카드")
                    self.state["card_returned"] = True
                    self.ui.print_system_message("이제 **[탑승구]**를 마저 조여야 할 것 같다.", is_markdown=True)
                else:
                    self.ui.print_system_message("**주머니**에 **[법인카드]**가 없습니다.", is_markdown=True)
            else:
                self.ui.print_system_message(
                    "지금은 **[교수님]**에게 **[법인카드]**를 전달할 필요가 없습니다.", is_markdown=True
                )
            return True

        return False
