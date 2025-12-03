from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE3_2_DATA = SceneData(
    id=SceneID.CH1_SCENE3_2,
    name="배양실",
    body=(
        '"으으... 뼛속까지 시리네."\n\n'
        "투명한 유리관들이 줄지어 늘어서 있는 배양실입니다.\n"
        "유리관 안에는 흙이 채워져 있고, 매미 사육장이 보입니다.\n\n"
        "벽에는 고장 난 온도 조절기가 전선이 끊어진 채 방치되어 있고,\n"
        "그 옆에는 연구 소장이 남긴 듯한 연구 일지가 붙어 있습니다.\n\n"
    ),
    initial_state={
        "valve_installed": False,
        "thermostat_fixed": False,
        "temp_step": 0,
        "hallway_inspected": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.LOG: KeywordData(type=KeywordType.ALIAS, target=KeywordId.RESEARCH_LOG),
        KeywordId.CAGE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.CICADA_CAGE),
        # 0. 나가기 (연구동 복도)
        KeywordId.HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="문틈으로 연구동 복도의 불빛이 보입니다. 이곳은 너무 추워서 오래 있기 힘듭니다.",
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
                                "prompt": "추운 배양실을 나가 **[연구동 중앙 복도]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="옷깃을 여미며 서둘러 복도로 나갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 확인할 것이 남았습니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 연구 일지 (핵심 힌트)
        KeywordId.RESEARCH_LOG: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            name="연구 일지",
            description=(
                "< 연구 소장의 메모 >\n\n"
                "세상은 멍청한 구분선들로 가득 차 있다.\n\n"
                "온도 조절기의 눈금도, 키보드의 하이픈도 모두 본질을 가리는 방해물일 뿐이다.\n\n"
                "인위적인 경계선들을 모두 무시하고, 공평하게 나눠야 한다.\n\n"
                "그때 비로소 매미는 노래할 것이다."
            ),
        ),
        # 2. 온도 조절기 (퍼즐 오브젝트)
        KeywordId.THERMOSTAT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 수리 완료 (힌트 적용 확인)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "수리된 온도 조절기가 윙윙거리며 돌아갑니다.\n\n"
                                "기계에는 '저온 | 적정 | 고온'이라는 3단계 눈금이 그어져 있지만,\n\n"
                                "연구 일지의 내용대로라면 이 눈금은 무시해야 합니다.\n\n"
                                "다이얼을 돌리는 대신, 원하는 온도를 정확히 입력해야 작동할 것 같습니다.\n\n"
                                "사전에 설정되지 않은 온도에는 반응하지 않는 것 같습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"원하는 온도를 `{KeywordId.THERMOSTAT} : [온도]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                # Case 2: 밸브만 끼움
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="valve_installed", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "황동 밸브를 끼워놨지만, 손으로 돌리기엔 너무 뻑뻑합니다.\n\n"
                                "제대로 고정하려면 **도구**로 꽉 조여야 합니다."
                            ),
                        )
                    ],
                ),
                # Case 3: 초기 상태
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "냉각수 배관의 밸브 손잡이가 통째로 뽑혀 나갔습니다.\n\n"
                                "이 상태로는 조절이 불가능합니다. 톱니에 맞는 **밸브**를 찾아와야 합니다."
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 3. 매미 사육장 (반응)
        # 3. 매미 사육장 (temp_step에 따른 반응 분기)
        KeywordId.CICADA_CAGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Step 4: 35도 (광란)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="temp_step", value=4)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "사육장 안이 찜통더위입니다. 매미들이 짝을 찾기 위해 발악하듯 울어댑니다.\n\n"
                                "🔊 **'맴!맴!맴!맴!맴!맴!맴!'**\n\n"
                                "빠르고 불규칙한 소음이 고막을 때립니다. 정신이 하나도 없습니다."
                            ),
                        )
                    ],
                ),
                # Step 3: 30도 (장음)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="temp_step", value=3)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "한여름의 절정 같은 날씨입니다. 매미들이 활기차게 합창합니다.\n\n"
                                "🔊 **'찌르르르-'**\n\n"
                                "길고 우렁찬 소리가 끊이지 않고 이어집니다."
                            ),
                        )
                    ],
                ),
                # Step 2: 20도 (단음 3회)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="temp_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "초여름처럼 선선합니다. 매미 몇 마리가 점잖게 울고 있습니다.\n\n"
                                "🔊 **'맴- 맴- 맴-'**\n\n"
                                "정확히 세 번씩 끊어서 소리를 냅니다."
                            ),
                        )
                    ],
                ),
                # Step 1: 5도 (침묵)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="temp_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "사육장 유리에 성에가 꼈습니다. 흙 속은 고요합니다.\n\n"
                                "🔊 **(......)**\n\n"
                                "너무 추워서 매미들이 동면 상태에 들어갔습니다. 아무 소리도 들리지 않습니다."
                            ),
                        )
                    ],
                ),
                # Default: 초기 상태 (온도 설정 전)
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "냉방 시스템이 고장 났는지 냉기가 감돕니다.\n"
                                "매미 유충들은 흙 깊은 곳에 숨어 꼼짝도 하지 않습니다.\n\n"
                                "온도를 높여줘야 반응이 있을 것 같습니다."
                            ),
                        )
                    ]
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (배양실) ---
        "유리관": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="내 키보다 큰 거대한 시험관들이다. 안에 든 게 외계인이 아니라 매미라니, 스케일이 큰 건지 작은 건지 모르겠다.",
        ),
        "흙": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="유리관 안을 가득 채우고 있다. 단면도로 개미집을 관찰하는 기분이다. 물론 개미 대신 징그러운 유충들이 있지만.",
        ),
        "벽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="결로 현상 때문에 물방울이 맺혀 있다. 건물이 울고 있는 것 같다. 나도 울고 싶다.",
        ),
    },
    # 조합 (수리 로직)
    combinations=[
        # 1단계: 황동 밸브 + 온도 조절기
        Combination(
            targets=[KeywordId.BRASS_VALVE, KeywordId.THERMOSTAT],
            conditions=[Condition(type=ConditionType.STATE_IS, target="valve_installed", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="주워온 황동 밸브를 파이프 톱니에 끼워 맞췄습니다. 헐거워서 헛돕니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "valve_installed", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BRASS_VALVE),
            ],
        ),
        # 2단계: 스패너 + 온도 조절기
        Combination(
            targets=[KeywordId.THERMOSTAT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="valve_installed", value=True),
                Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너로 밸브를 꽉 조였습니다. 이제 온도 조절이 가능합니다.\n\n"
                        "내 마음대로 사육장 온도를 맞출 수 있게 되었습니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "thermostat_fixed", "value": True}),
            ],
        ),
        # [온도 조절] 1단계: 20도 (침묵)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.THERMOSTAT, "5"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="위잉- 온도가 5℃로 내려갑니다.\n\n너무 추워서인지 매미들이 흙 속으로 깊이 숨어버려 아무 소리도 들리지 않습니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "temp_step", "value": 1}),
            ],
        ),
        # [온도 조절] 2단계: 25도 (소리 패턴 A)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.THERMOSTAT, "20"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="위잉- 온도가 20℃에 맞춰집니다.\n\n매미 몇 마리가 기어나와 울기 시작합니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "temp_step", "value": 2}),
            ],
        ),
        # [온도 조절] 3단계: 30도 (소리 패턴 B)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.THERMOSTAT, "30"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="위잉- 온도가 30℃로 올라갑니다.\n\n활발해진 매미들이 합창합니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "temp_step", "value": 3}),
            ],
        ),
        # [온도 조절] 4단계: 35도 (소리 패턴 C - 광란)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.THERMOSTAT, "35"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="thermostat_fixed", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="위잉- 온도가 35℃까지 치솟습니다. 열대야 같은 더위입니다.\n\n매미들이 미친 듯이 울어댑니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "temp_step", "value": 4}),
            ],
        ),
    ],
)
