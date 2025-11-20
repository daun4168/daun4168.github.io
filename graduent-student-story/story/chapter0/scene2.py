from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE2_DATA = SceneData(
    id=SceneID.CH0_SCENE2,
    name="제 2 연구실 (청소 완료)",
    initial_text='청소를 마치자마자 교수님이 땀을 뻘뻘 흘리며 거대한 기계를 들고 들어왔습니다.\n\n"자, 이게 내 역작 MK-II야. 배송비를 아껴줄 초공간 양자 전송 장치지. 해외 직구 배송비가 너무 비싸서 직접 만들었어."\n\n교수는 전선을 대충 콘센트에 꽂더니 나를 쳐다봅니다. 기계에서 불안한 웅웅 소리가 납니다.\n\n"테스트하게 저기 탑승구로 들어가. 자네 몸무게가 쌀 한 가마니랑 비슷하니까 딱이야."',
    initial_state={
        "professor_called_out": False,
        "card_returned": False,
    },
    keywords={
        KeywordId.PROFESSOR: KeywordData(
            type=KeywordType.NPC,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
                        Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='교수님: "**[법인카드]**는 놓고 가게!" 교수님이 나를 빤히 쳐다본다.',
                        )
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="card_returned", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="교수님은 이미 **[법인카드]**를 받아갔다. 이제 **[탑승구]**를 조이는 일만 남았다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='교수님: "뭘 꾸물거려? 어서 **[탑승구]**로 들어가! 아, 그리고 그거 좀 뻑뻑하던데, 알아서 잘 조이고. 공대생이 그정돈 하겠지?"',
                        )
                    ]
                ),
            ],
        ),
        KeywordId.MK_II: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="교수님의 역작 **[MK-II]**다. 초공간 양자 전송 장치라는데, 전선 마감이 청테이프인 것이 불안하다. **[탑승구]** 쪽 경첩이 덜 조여진 것처럼 보인다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[스패너]**로 대충 고쳐볼까 했지만, 더 망가뜨릴 것 같다.",
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="교수님의 역작 **[MK-II]**다. 초공간 양자 전송 장치라는데, 전선 마감이 청테이프인 것이 불안하다. **[탑승구]** 쪽 경첩이 덜 조여진 것처럼 보인다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.HATCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="육중한 해치다. 경첩이 헐거워 제대로 닫히지 않을 것 같다. **주머니**에 있는 **[스패너]**로 조이면 될 것 같다.",
        ),
        KeywordId.OUTLET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="벽에 꽂힌 **[MK-II]**의 **[콘센트]**다. 헐거워 보이지만, 건드리면 큰일 날 것 같다.",
        ),
        KeywordId.WIRE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="청테이프로 대충 감아놓은 **[전선]**이다. 교수님의 공학적 감각은 일반인의 상식을 뛰어넘는다.",
        ),
        KeywordId.LAB_COAT: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.DISCOVERED,
            description="주머니에 챙겨둔 실험용 랩 가운이다. 마지막 순간에 격식을 갖추기 위해 꺼내두었다.",
        ),
    },
    combinations=[
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 **[탑승구]**의 뻑뻑한 부분을 조이려 하자, 갑자기 교수님이 나를 부른다.",
                ),
                Action(type=ActionType.PRINT_SYSTEM, value='교수님: "자네, **[법인카드]**는 놓고 가게!"'),
                Action(type=ActionType.UPDATE_STATE, value={"key": "professor_called_out", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="교수님이 **[법인카드]**를 놓고 가라고 한다. **[교수님]**에게 **[법인카드]**를 전달해야 할 것 같다.",
                )
            ],
        ),

        # [수정] 여기가 핵심 변경 부분입니다.
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 **[탑승구]**를 단단히 조이자마자, 기계가 요란한 소리를 내며 진동하기 시작한다!\n\n교수님: \"좋아! 가동 시작! 좌표는... 어... 대충 거기로 설정했어! 살아서 돌아오게!\"\n\n시야가 하얗게 점멸하고, 엄청난 중력이 몸을 짓누른다. 의식이 희미해진다...",
                ),
                # 게임 종료 대신 씬 이동 액션 사용
                Action(
                    type=ActionType.MOVE_SCENE,
                    value=SceneID.CH1_SCENE0,  # 챕터 1의 불시착 씬으로 이동
                ),
            ],
        ),

        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.CORP_CARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD),
                Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="교수님께 **[법인카드]**를 건네자, 교수님은 만족스러운 표정으로 고개를 끄덕인다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CORP_CARD),
                Action(type=ActionType.UPDATE_STATE, value={"key": "card_returned", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 **[탑승구]**를 마저 조여야 할 것 같다."),
            ],
        ),
        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.CORP_CARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD),
                Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="지금은 **[교수님]**에게 **[법인카드]**를 전달할 필요가 없습니다.",
                )
            ],
        ),
    ],
)