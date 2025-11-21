from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID, CombinationType
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

# --- [Scene 1: 그늘진 해변 (베이스캠프)] ---
CH1_SCENE1_DATA = SceneData(
    id=SceneID.CH1_SCENE1,
    name="그늘진 해변 (베이스캠프)",
    initial_text=(
        "\"헥헥... 죽는 줄 알았네.\"\n\n"
        "당신은 젖 먹던 힘을 다해 MK-II를 거대한 야자수 그늘 아래로 옮기는 데 성공했습니다. "
        "기계도 나도 더 이상 직사광선에 고통받지 않아도 됩니다. 이곳은 이제 나의 훌륭한 베이스캠프입니다.\n\n"
        "그늘 밖은 여전히 용광로 같습니다. 동쪽 해변 끝에는 난파선 잔해가 아지랑이 너머로 보이고, "
        "북쪽에는 숲 입구가 보입니다. 바로 앞에는 파도에 떠밀려온 쓰레기 더미가 쌓여 있고, "
        "시원한 바다와 따뜻한 모래사장이 펼쳐져 있습니다.\n\n"
        "일단은 안전합니다. 이제 어떻게 할까요?"
    ),
    initial_state={
        "wreck_path_inspected": False,
        "pending_move_wreck": False,
        "tree_inspected": False,
        "coconut_obtained": False,  # [추가] 코코넛 획득 여부
        "crab_caught": False,
        "searched_trash": False,
        "has_shelter": False,
    },
    on_enter_actions=[
        # 체력 UI 표시 (자동 저장은 제거됨)
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # 1. 모래사장 (안전 지대)
        KeywordId.SAND: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="그늘 아래의 모래는 적당히 따뜻하다. 밖의 모래는 용암처럼 뜨겁겠지만, 여기선 찜질방 수준이다. 안전하다.",
        ),

        # 2. 바다 (모호한 설명 - 학습 효과)
        KeywordId.SEA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "보기만 해도 시원해 보인다. 하지만 이것은 염분 농도 3.5%의 수용액이다. "
                "마시면 삼투압 현상으로 탈수가 가속화된다는 건 상식이다. "
                "경험적으로든 이론적으로든, 다시는 입에 대고 싶지 않다."
            ),
        ),

        # 3. 난파선 잔해 (이동 포인트 - 확인 절차 포함)
        KeywordId.WRECKAGE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 처음 조사할 때 (정보 습득)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=False)
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동쪽을 보니 **[난파선 잔해]**가 꽤 멀리 있다.\n"
                                "가는 길에 그늘이 하나도 없어서, 저기까지 가려면 땀 좀 뺄 것 같다. (체력 소모 예상)"
                            )
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한번 **[난파선 잔해]**를 선택하면 이동 여부를 결정합니다."
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wreck_path_inspected", "value": True})
                    ]
                ),
                # Case 2: 두 번째 선택 (이동 의사 확인)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="pending_move_wreck", value=False)
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[난파선 잔해]**로 이동하시겠습니까?\n"
                                "뜨거운 모래사장을 건너야 하므로 **체력이 2 소모**됩니다.\n\n"
                                "**[예]** / **[아니오]**"
                            )
                        ),
                        # 예/아니오 키워드 활성화
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.YES, "state": KeywordState.HIDDEN}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.NO, "state": KeywordState.HIDDEN}),
                        # 대기 상태로 변경
                        Action(type=ActionType.UPDATE_STATE, value={"key": "pending_move_wreck", "value": True})
                    ]
                )
            ]
        ),

        # 4. 예 (이동 확정)
        KeywordId.YES: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.INACTIVE,  # 평소엔 숨김
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="pending_move_wreck", value=True)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="뜨거운 태양을 뚫고 난파선을 향해 걷기 시작합니다..."),
                        Action(type=ActionType.MODIFY_STAMINA, value=-2),  # 체력 소모
                        # 상태 초기화 (돌아왔을 때를 위해)
                        Action(type=ActionType.UPDATE_STATE, value={"key": "pending_move_wreck", "value": False}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.YES, "state": KeywordState.HIDDEN}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.NO, "state": KeywordState.HIDDEN}),
                        # 씬 이동 (CH1_SCENE2는 난파선 씬 ID - 추후 구현 필요)
                        Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2)
                    ]
                )
            ]
        ),

        # 5. 아니오 (이동 취소)
        KeywordId.NO: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="pending_move_wreck", value=True)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="지금은 베이스캠프 그늘에서 쉬는 게 낫겠습니다. 괜히 힘 뺄 필요 없죠."),
                        # 상태 초기화
                        Action(type=ActionType.UPDATE_STATE, value={"key": "pending_move_wreck", "value": False}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.YES, "state": KeywordState.HIDDEN}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.NO, "state": KeywordState.HIDDEN}),
                    ]
                )
            ]
        ),

        # 6. 숲 입구 (진입 불가)
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="울창한 밀림이다. 억센 덩굴로 막혀 있어, **[정글도]** 같은 날카로운 도구가 없으면 들어갈 수 없다.",
        ),

        # 7. MK-II (수리 대상)
        KeywordId.MK_II: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description="그늘에 두니 엔진 열기가 조금 식은 것 같다. 하지만 여전히 작동 불능이다. **[냉각수]**와 **[전력]** 공급이 시급하다."
        ),

        # 8. 쓰레기 더미 (안전한 파밍)
        KeywordId.TRASH_PILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="searched_trash", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="역겨운 냄새를 참으며 쓰레기를 뒤진다. 베이스캠프 바로 앞이라 안전하게 파밍할 수 있다.\n쓸만해 보이는 **[빈 페트병]**과 **[비닐]** 조각을 발견했다."
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-3),  # 안전해서 소모량 적음
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.PLASTIC_BOTTLE, "description": "찌그러진 페트병이다."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.VINYL, "description": "구멍 나지 않은 튼튼한 비닐이다."}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "searched_trash", "value": True}),
                    ]
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="더 이상 쓸만한 건 없다.")])
            ]
        ),

        # 9. 야자수 (물리 법칙 교육)
        KeywordId.PALM_TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 1. 첫 번째 접촉 (조사): 코코넛 존재 확인
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="tree_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="매우 높다. 올라가는 건 불가능하다. 위를 보니 **[코코넛]**이 매달려 있다. 무언가 도구로 충격을 주면 떨어질지도 모른다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "tree_inspected", "value": True}),
                    ]
                ),
                # 2. 두 번째 이후 접촉 (발로 차기): 체력 감소
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="야자수를 있는 힘껏 발로 찼다! ...꿈쩍도 안 한다. 발가락이 부러질 것 같다."),
                        Action(type=ActionType.MODIFY_STAMINA, value=-3),
                        Action(type=ActionType.PRINT_SYSTEM, value="[경고] 맨몸으로 도전하다 체력이 감소했습니다."),
                    ]
                )
            ]
        ),
    },

    # 조합식
    combinations=[
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.SPANNER],
            conditions=[
                # 코코넛을 아직 얻지 않았을 때만 가능
                Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=False)
            ],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="**[스패너]**를 던져 **[코코넛]**을 정확히 맞췄다. 툭, 하고 열매가 떨어진다. 훌륭한 투구였다."),
                Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.COCONUT, "description": "단단한 껍질의 열매."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "coconut_obtained", "value": True}),
            ]
        ),
        # 이미 얻었을 때의 피드백
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=True)
            ],
            actions=[
                Action(type=ActionType.PRINT_SYSTEM, value="이미 코코넛을 떨어뜨렸습니다. 더 이상 열매가 없습니다.")
            ]
        )
    ]
)