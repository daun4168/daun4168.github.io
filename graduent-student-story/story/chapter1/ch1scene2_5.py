from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_5_DATA = SceneData(
    id=SceneID.CH1_SCENE2_5,
    name="지하 복도",
    body=(
        "지하로 내려오자마자 매캐한 화학 약품 냄새가 코를 찌릅니다.\n\n"
        "바닥 곳곳이 녹아내려 걷기 힘듭니다.\n\n"
        "복도 중앙에는 천장에서 떨어진 황산이 산성 웅덩이를 이루어 지하 연구실 문 앞을 가로막고 있습니다.\n\n"
        "오른쪽에는 주방 문이 반쯤 열려 있고, 구석에는 녹슨 양동이가 굴러다닙니다.\n\n"
        "뒤쪽 계단으로 올라가면 중앙 복도로 돌아갈 수 있습니다."
    ),
    initial_state={
        "acid_neutralized": False,
        "bucket_found": False,
        "hallway_inspected": False,
        "acid_collected": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.BUCKET_OBJ: KeywordData(type=KeywordType.ALIAS, target=KeywordId.RUSTY_BUCKET_OBJ),
        KeywordId.HALLWAY: KeywordData(type=KeywordType.ALIAS, target=KeywordId.CENTER_HALLWAY),
        KeywordId.PUDDLE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.ACID_PUDDLE),
        KeywordId.LAB: KeywordData(type=KeywordType.ALIAS, target=KeywordId.BASEMENT_LAB),
        KeywordId.LAB_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.BASEMENT_LAB),
        KeywordId.BASEMENT_LAB_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.BASEMENT_LAB),
        KeywordId.KITCHEN_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.KITCHEN),
        # 0. 나가는 길 (중앙 복도)
        KeywordId.CENTER_HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="위층으로 올라가는 계단입니다. 신선한 공기가 그립습니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "hallway_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[중앙 복도]**로 올라가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="지하 복도를 벗어나 중앙 복도로 올라갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_0),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 할 일이 남았습니다.")
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 주방 문 (2-6 이동)
        KeywordId.KITCHEN: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "썩은 내가 진동하는 **[주방]**으로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="코를 막고 주방 안으로 들어갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_6),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="마음의 준비가 필요합니다.")
                                ],
                            },
                        )
                    ]
                )
            ],
        ),
        # 2. 연구실 문 (2-7 이동 - 장애물)
        KeywordId.BASEMENT_LAB: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 웅덩이 있음
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산성 웅덩이가 길을 막고 있습니다. 무리해서 지나가다간 다리가 녹아내릴 겁니다.",
                        )
                    ],
                ),
                # Case 2: 웅덩이 중화됨
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "안전해진 통로를 지나 **[연구실]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="연구실 문을 열고 들어갑니다. 서늘한 기운이 느껴집니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_7),
                                ],
                                "cancel_actions": [Action(type=ActionType.PRINT_NARRATIVE, value="잠시만요.")],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 3. 산성 웅덩이
        KeywordId.ACID_PUDDLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="가성소다로 중화되어 하얗게 변했습니다. 이제 밟고 지나갈 수 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.ACID_PUDDLE, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="치이익- 소리를 내며 끓고 있는 노란 액체입니다. 강염기성 물질로 중화해야 합니다.",
                        )
                    ]
                ),
            ],
        ),
        # 4. 녹슨 양동이 (파밍)
        KeywordId.RUSTY_BUCKET_OBJ: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bucket_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="구석에 처박힌 양동이를 주웠습니다. 바닥이 녹슬어 물은 새겠지만, 가루 같은 건 담을 수 있겠습니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.RUSTY_BUCKET, "description": "가루를 담을 수 있는 낡은 양동이."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "bucket_found", "value": True}),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RUSTY_BUCKET_OBJ, "state": KeywordState.INACTIVE},
                        ),
                    ],
                ),
                # Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="양동이가 있던 자리엔 먼지뿐입니다.")])
            ],
        ),
        # --- UNSEEN 오브젝트 (지하 복도) ---
        "냄새": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="코털이 다 타버릴 것 같다. 공짜 코털 제모는 고맙지만, 폐까지 제모하고 싶진 않다.",
        ),
        "바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="치즈 퐁듀처럼 흐물흐물하게 녹아내렸다. 밟는 순간 내 발도 퐁듀 재료가 될 것이다.",
        ),
        "천장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="침을 흘리듯 황산을 뚝뚝 흘리고 있다. 배관공을 부르기엔 이미 늦은 것 같다. 우산을 쓰고 싶다.",
        ),
        "황산": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="색깔만 보면 레모네이드다. 하지만 마시는 순간 식도부터 위장까지 하이패스가 뚫릴 것이다.",
        ),
        "계단": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="나의 소중한 생명줄이다. 당장이라도 도망치고 싶지만, 빈손으로 돌아가면 굶어 죽는다. 진퇴양난이다.",
        ),
        "화학 약품": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="MSDS(물질안전보건자료)를 안 봐도 알겠다. '흡입 시 치명적임', '피부 접촉 시 화상'. 분명 이렇게 적혀있을 냄새다.",
        ),
        "공기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="무겁고 끈적하다. 산소보다 유독가스의 비율이 더 높은 것 같다. 숨을 쉴 때마다 폐가 절여지는 기분이다.",
        ),
        "구석": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="어둠과 먼지, 그리고 정체불명의 곰팡이가 삼위일체를 이루고 있다. 저기엔 바퀴벌레도 살지 못할 것이다.",
        ),
        "조명": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="전압이 불안정한지 계속 깜빡거린다. 공포 영화 클리셰가 완벽하게 갖춰져 있다. 귀신이 나와도 이상하지 않다.",
        ),
        "중앙": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="가장 중요한 길목을 황산 웅덩이가 점거하고 있다. 레벨 디자이너가 누군지 몰라도 악취미가 분명하다.",
        ),
    },
    combinations=[
        # 1. 산성 용액 채취 (소스통 + 웅덩이)
        Combination(
            targets=[KeywordId.SAUCE_BOTTLE, KeywordId.ACID_PUDDLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="빈 소스통을 이용해 바닥에 남은 산성 용액을 조심스럽게 담았습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SAUCE_BOTTLE),
                Action(
                    type=ActionType.ADD_ITEM, value={"name": KeywordId.ACID_SOURCE, "description": "황산이 든 소스통."}
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_collected", "value": True}),
            ],
        ),
        # 2. 웅덩이 중화 (가성소다 양동이 + 웅덩이)
        Combination(
            targets=[KeywordId.FILLED_BUCKET, KeywordId.ACID_PUDDLE],
            # 샘플 채취 여부에 따른 분기 (안전을 위해) - 여기서는 자유도를 위해 경고 없이 허용하거나 경고 추가 가능
            # 이번엔 심플하게 채취 후 중화 권장 로직
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="가성소다를 웅덩이에 들이부었습니다. 보글거리는 거품과 함께 맹독성 액체가 중화되어 투명해졌습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FILLED_BUCKET),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_neutralized", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.ACID_PUDDLE, KeywordId.POTATO_STARCH],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="전분 가루를 웅덩이에 뿌려봤자 조금 걸쭉해질 뿐, 산성이 중화되지는 않습니다.\n\n강산성을 무력화시키려면 염기성 성분의 다른 가루가 필요합니다.",
                )
            ],
        ),
        # 1-3. 양동이 + 산성 웅덩이 (실패 - 부상)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.ACID_PUDDLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="으악! 양동이가 너무 커서 액체가 출렁거렸습니다. 손등에 산성 용액이 튀었습니다!",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),  # 체력 감소
                Action(
                    type=ActionType.PRINT_SYSTEM, value="화상을 입었습니다. 좀 더 다루기 쉬운 작은 용기가 필요합니다."
                ),
            ],
        ),
        # 샘플 채취 전 경고
        Combination(
            targets=[KeywordId.FILLED_BUCKET, KeywordId.ACID_PUDDLE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "잠깐, 이 웅덩이를 지금 다 중화시켜 버리면 나중에 산성 물질이 필요할 때 구할 곳이 없어집니다.\n\n"
                        "어딘가에 샘플을 좀 떠둔 뒤에 붓는 게 좋겠습니다."
                    ),
                )
            ],
        ),
    ],
)
