from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE2_DATA = SceneData(
    id=SceneID.CH0_SCENE2,
    name="제 2 연구실 (청소 완료)",
    body='청소를 마치자마자 교수님이 땀을 뻘뻘 흘리며 거대한 기계를 들고 들어왔습니다.\n\n"자, 이게 내 역작 MK-II야. 배송비를 아껴줄 초공간 양자 전송 장치지. 해외 직구 배송비가 너무 비싸서 직접 만들었어."\n\n교수는 전선을 대충 콘센트에 꽂더니 나를 쳐다봅니다. 기계에서 불안한 웅웅 소리가 납니다.\n\n"테스트하게 저기 탑승구로 들어가. 자네 몸무게가 쌀 한 가마니랑 비슷하니까 딱이야."',
    initial_state={
        "professor_called_out": False,  # 교수가 카드를 달라고 소리쳤는지 여부
        "card_returned": False,  # 카드가 반납되었는지 여부
    },
    keywords={
        KeywordId.PROFESSOR: KeywordData(
            type=KeywordType.NPC,
            state=KeywordState.HIDDEN,
            interactions=[
                # 1. 카드를 아직 안 줬고, 교수가 달라고 소리친 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
                        Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='교수님: "내 말 안 들리나? **[법인카드]** 놓고 가라고! 그게 내 목숨보다 중요한 거야!"',
                        )
                    ],
                ),
                # 2. 카드를 이미 반납한 상태
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="card_returned", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='교수님: "뭘 꾸물거려? 어서 **[탑승구]**로 들어가! 좌표 설정 다 끝났어... 아마도?"',
                        )
                    ],
                ),
                # 3. 기본 상태 (아직 소리치지 않음, 카드 안 줌)
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='교수님: "어서 들어가게. 아, **[탑승구]** 경첩이 좀 헐거우니까 자네가 알아서 좀 조이고."',
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
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="교수님의 역작 **[MK-II]**다. 초공간 양자 전송 장치라는데, 전선 마감이 청테이프인 것이 심히 불안하다.\n**[탑승구]** 쪽 경첩이 덜 조여진 것처럼 덜렁거린다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.HATCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # [네거티브 피드백] 수리하지 않고 그냥 탑승하려고 할 때
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="그냥 들어가려니 문이 덜렁거려서 닫히질 않는다. 이대로 가동했다간 우주 미아가 될 것이다. 무언가로 단단히 조여야 한다.",
                        )
                    ]
                )
            ],
            # 설명을 조금 더 간접적으로 수정
            description="사람 하나가 겨우 들어갈 만한 좁은 입구다. 경첩이 헐거워서 손으로 만지면 덜그럭거린다. 꽉 조일만한 게 필요하다.",
        ),
        KeywordId.OUTLET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="벽에 꽂힌 **[MK-II]**의 **[콘센트]**다. 피복이 벗겨져 있어 보기만 해도 짜릿하다. 건드리면 졸업하기 전에 요단강을 건널 것 같다.",
        ),
        KeywordId.WIRE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="청테이프로 대충 감아놓은 **[전선]**이다. 교수님의 공학적 감각은 일반인의 상식을 아득히 뛰어넘는다.",
        ),
        KeywordId.LAB_COAT: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.DISCOVERED,
            description="주머니에 챙겨둔 실험용 랩 가운이다. 마지막 순간에 격식을 갖추기 위해 꺼내두었다.",
        ),
    },
    combinations=[
        # [수정] 스패너로 탑승구 수리 시도 (카드를 아직 안 줬을 때 -> 방해 이벤트 발생)
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),  # 카드를 아직 안 줬다면
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 **[탑승구]**의 볼트를 조이려는 찰나, 교수님이 다급하게 소리친다.",
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value='교수님: "잠깐! 자네 주머니에 **[법인카드]**! 그거 놓고 타야지! 가지고 가면 횡령이야!"',
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "professor_called_out", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="교수님이 **[법인카드]**를 회수하려 합니다."),
            ],
        ),
        # [수정] 스패너로 탑승구 수리 시도 (카드를 이미 줬을 때 -> 성공 및 씬 이동)
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value='**[스패너]**로 **[탑승구]**를 단단히 조이자마자, 기계가 요란한 소리를 내며 진동하기 시작한다!\n\n교수님: "좋아! 가동 시작! 좌표는... 어... 대충 거기로 설정했어! 살아서 돌아오게!"\n\n시야가 하얗게 점멸하고, 엄청난 중력이 몸을 짓누른다. 의식이 희미해진다...',
                ),
                Action(
                    type=ActionType.MOVE_SCENE,
                    value=SceneID.CH1_SCENE0,
                ),
            ],
        ),
        # [수정] 교수님에게 법인카드 반납 (언제든지 가능하도록 조건 완화)
        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.CORP_CARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value='교수님께 **[법인카드]**를 건네자, 교수님은 빛보다 빠른 속도로 카드를 낚아채 주머니에 넣는다.\n\n교수님: "그래, 이건 연구실의 자산... 아니, 내 영혼과도 같은 거지."',
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CORP_CARD),
                Action(type=ActionType.UPDATE_STATE, value={"key": "card_returned", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 방해 없이 **[탑승구]**를 수리할 수 있습니다."),
            ],
        ),
        # [네거티브 피드백] 스패너 + 교수님
        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value='**[스패너]**를 들어 올리자 교수님이 기겁하며 뒤로 물러선다.\n\n교수님: "이보게! 대학원생의 분노는 이해하지만, 폭력은 안 돼! 졸업은 해야지!"',
                )
            ],
        ),
        # [네거티브 피드백] 스패너 + 콘센트/전선
        Combination(
            targets=[KeywordId.OUTLET, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="금속 **[스패너]**를 전기가 흐르는 **[콘센트]**에 갖다 대는 건 자살 행위나 마찬가지다. 아직은 살고 싶다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.WIRE, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="이 엉성한 **[전선]**을 건드렸다간 기계가 폭발할지도 모른다. 교수님이 보고 있다.",
                )
            ],
        ),
    ],
)
