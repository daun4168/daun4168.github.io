from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Condition, Interaction, KeywordData, SceneData

ENDING_MESSAGE = """
# **【엔딩】**

---
\n\n
당신은 무인도에서의 긴 여정을 마치고  
조용한 기계음과 함께 제 2 연구실로 되돌아왔습니다.

익숙한 먼지 냄새,  
빛바랜 모니터,  
낡은 시약장…

모든 것이 그대로인데,  
왠지 모르게 조금씩 달라 보입니다.

---

그리고,  
당신의 여정을 조용히 함께했던 스패너는  
어딘가로 사라져 있습니다.

> “출발할 때는… 분명 손에 있었는데.”

연구실 구석에도,  
공구함 속에도,  
책상 아래에도…

스패너는 없습니다.

마치 누군가 당신보다 먼저 돌아와  
그 작은 금속을 들고 어딘가로 향해 버린 것처럼.

---

이야기는 잠시 멈추어 숨을 고릅니다.  
그러나 끝난 것은 아닙니다.

연구실에 남은 미세한 흔적,  
그리고 사라진 스패너 한 자루.

---

다음 장에서는,  
그 스패너가 남긴 자취를 따라  
또 다른 여정이 시작될지도 모릅니다.

당신의 발걸음 역시… 다시 이어질 준비를 하고 있습니다.

"""

ENDING_INTERACTION = Interaction(
    conditions=[
        Condition(type=ConditionType.STATE_IS, target="lab_overview_inspected", value=True),
        Condition(type=ConditionType.STATE_IS, target="mk2_panel_inspected", value=True),
        Condition(type=ConditionType.STATE_IS, target="ending_note_inspected", value=True),
        Condition(type=ConditionType.STATE_IS, target="ending_message_shown", value=False),
    ],
    actions=[
        Action(
            type=ActionType.PRINT_NARRATIVE,
            value=(
                "연구실을 다시 한 바퀴 둘러보자, 이곳이 더 이상 단순한 출발점이 아니라는 사실이 또렷해진다.\n\n"
                "당신은 이 방에서 떠나 이 섬을 돌았고, 다시 여기로 돌아왔다.\n"
                "하지만, 떠나기 전과는 다른 눈으로 세상을 보게 되었다."
            ),
        ),
        Action(
            type=ActionType.PRINT_SYSTEM,
            value=ENDING_MESSAGE,
        ),
        Action(
            type=ActionType.UPDATE_STATE,
            value={"key": "ending_message_shown", "value": True},
        ),
    ],
)

CH1_SCENE10_DATA = SceneData(
    id=SceneID.CH1_SCENE10,
    name="제 2 연구실 (귀환)",
    body=(
        "MK-II의 모터음이 점점 가라앉더니, 갑자기 모든 소리가 흩어지고 시야가 어둡게 말려 들어간다.\n\n"
        "그리고——\n\n"
        "당신은 다시 제 2 연구실 바닥 위에 서 있다.\n\n"
        "먼지 쌓인 모니터, 테이프로 덕지덕지 붙인 박스, 시약장의 냄새까지… 모든 것이 익숙하다.\n"
        "그런데, 어딘가 아주 미세하게 낯설다.\n\n"
        "MK-II는 조용히 숨을 고르는 듯 멈춰 있고, 연구실 공기는 출발 전보다 조금 더 차분해져 있다.\n"
        "정말로 돌아온 걸까, 아니면 아주 비슷한 어딘가일까.\n\n"
        "일단은 숨을 고른다. 그리고 천천히, 주변을 살펴보기로 한다."
    ),
    initial_state={
        "lab_overview_inspected": False,  # 연구실 전반을 본 적 있는지
        "mk2_panel_inspected": False,  # 귀환 후 MK-II를 다시 살펴봤는지
        "ending_note_discovered": False,  # 책상에서 메모를 발견했는지
        "ending_note_inspected": False,  # 메모 내용을 읽었는지
        "ending_message_shown": False,  # 엔딩 시스템 메시지를 이미 보여줬는지
    },
    on_enter_actions=[
        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SPANNER),
        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FIRE_AXE),
        Action(type=ActionType.SHOW_STAMINA_UI, value=False),
    ],
    keywords={
        # 연구실 전체
        KeywordId.LAB_ROOM: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "익숙한 제 2 연구실이다. 쓰레기통, 책상, 시약장, 그리고 한쪽 구석의 MK-II.\n"
                "모든 것이 제자리에 있는 것 같으면서도, 어딘가 조금씩 달라 보인다."
            ),
            interactions=[
                # 처음 연구실을 둘러볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="lab_overview_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "연구실을 둘러보니, 출발 전과 거의 같은 풍경이 펼쳐져 있다.\n\n"
                                "쓰레기통은 여전히 반쯤 차 있고, 박스는 테이프로 칭칭 감겨 있으며, 시약장에는 냄새 나는 병들이 줄지어 서 있다.\n"
                                "그럼에도 어딘가 다른 느낌이 드는 이유는, 아마도 이 방이 아니라 당신 자신이 변했기 때문일 것이다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lab_overview_inspected", "value": True},
                        ),
                    ],
                ),
                ENDING_INTERACTION,
                # 그 외 반복 조사
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "익숙한 연구실이다. 하지만 이제 이 방은, 첫 출발점이라기보다는 "
                                "한 번 돌아온 뒤 다시 떠나기 좋은 기점처럼 느껴진다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 귀환 후 MK-II
        KeywordId.QUANTUM_CAULDRON: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "제 2 연구실 구석에 서 있는 MK-II. 외형은 이전과 크게 다르지 않지만, "
                "어딘가 세척된 듯 금속 표면이 조금 더 반짝인다."
            ),
            interactions=[
                # 귀환 후 처음 MK-II를 자세히 볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_panel_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II 외장을 손으로 쓸어보니, 출발 전보다 덜 거칠게 느껴진다.\n\n"
                                "패널 옆 공구함을 열어 보지만, 안에 있어야 할 **[스패너]**는 어디에도 없다.\n"
                                "당신이 이 섬으로 떠날 때 손에 쥐고 있던 바로 그 공구다.\n\n"
                                "연구실 바닥, 책상 아래, 기체 뒤편까지 둘러봐도 스패너는 보이지 않는다.\n"
                                "마치 누군가가, 당신이 없는 사이에 이 방을 스쳐 지나가 스패너만 조용히 가져간 것처럼."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "mk2_panel_inspected", "value": True},
                        ),
                    ],
                ),
                # 다시 MK-II를 볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_panel_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II는 조용히 서 있다. 스패너가 없다는 사실만이, 이 귀환이 단순한 되감기가 아니었다는 것을 말해 준다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 책상/작업대: 수상한 메모 발견
        KeywordId.LAB_DESK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "연구실 중앙의 책상이다. 모니터와 키보드, 굴러다니는 메모지와 연구 노트들이 어지럽게 놓여 있다."
            ),
            interactions=[
                # 메모를 아직 발견하지 않았을 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ending_note_discovered", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "책상 위의 서류들을 정리하다 보니, 한쪽 모서리에 접어 둔 작은 메모지가 눈에 들어온다.\n"
                                "종이 가장자리는 살짝 그을린 흔적이 있어, 마치 먼 곳을 다녀온 여행 기념품처럼 보인다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "ending_note_discovered", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.ENDING_NOTE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[수상한 메모]**가 시야에 추가되었습니다.",
                        ),
                    ],
                ),
                # 이미 메모를 발견한 뒤 책상을 볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ending_note_discovered", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="책상 위에는 이미 펼쳐 본 메모와 낡은 연구 노트들이 흩어져 있다.",
                        )
                    ],
                ),
            ],
        ),
        # 수상한 메모 (다음편 암시)
        KeywordId.ENDING_NOTE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            silent_discovery=True,
            description="책상 모서리에 끼워져 있던, 모서리가 살짝 그을린 작은 메모지다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ending_note_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "메모를 펼쳐 보니 익숙한 필체가 눈에 들어온다.\n\n"
                                '  "MK-II 수리, 잘 봤다.\n'
                                "   이번엔 네 차례였고,\n"
                                '   다음은… 스패너의 차례다."\n\n'
                                "아래에는 이해할 수 없는 기호와 좌표 같은 숫자들이 적혀 있다.\n"
                                "마치 스패너를 들고 어딘가로 떠난 누군가가, 다음 목적지를 살짝 흘리고 간 것처럼."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "ending_note_inspected", "value": True},
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="모든 조사가 완료되었다면, 연구실을 다시 한 번 둘러보세요.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ending_note_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="메모에는 여전히 같은 문장과, 의미를 알 수 없는 기호들이 당신을 조용히 바라보고 있다.",
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # 이 엔딩 씬에서는 별도의 퍼즐 조합은 없다.
    ],
)
