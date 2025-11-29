from const import (
    ActionType, CombinationType, ConditionType, KeywordId,
    KeywordState, KeywordType, SceneID
)
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_7_DATA = SceneData(
    id=SceneID.CH1_SCENE2_7,
    name="지하 연구실",
    body=(
        '"으스스하네... 여긴 냉동 창고를 개조한 건가?"\n\n'
        "서늘한 냉기가 감도는 은밀한 연구실입니다.벽면은 방음재로 덮여 있고, 알 수 없는 기계 장치들이 웅웅거립니다.\n"
        "중앙에는 **[연구용 책상]**이 있고, 그 위에는 **[약품 트레이]**가 놓여 있습니다. 벽 쪽에는 기름때 묻은 **[작업대]**가 있습니다.\n\n"
        "가장 안쪽 구석에는 육중한 **[전자 금고]**가 붉은 빛을 내고 있고, 반대편 벽에는 **[소방 도끼]**가 단단히 고정되어 있습니다.\n"
    ),
    initial_state={
        "safe_powered": False,
        "safe_opened": False,
        "axe_obtained": False,
        "batteries_found": False,
        "workbench_inspected": False,
        "corridor_inspected": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.HALLWAY: KeywordData(type=KeywordType.ALIAS, target=KeywordId.TOXIC_CORRIDOR),

        # 0. 나가는 길 (지하 복도)
        KeywordId.TOXIC_CORRIDOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="corridor_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="복도로 나가는 문입니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "corridor_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="corridor_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[지하 복도]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="연구실을 나갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_5),
                                ],
                                "cancel_actions": [Action(type=ActionType.PRINT_NARRATIVE, value="아직 조사가 안 끝났습니다.")],
                            },
                        )
                    ]
                )
            ]
        ),

        # 1. 연구용 책상 (건전지 파밍)
        KeywordId.LAB_DESK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="batteries_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="책상 서랍을 열자 **[건전지]** 5개와 **[배터리 케이스]**가 굴러다닙니다. 실험용으로 쓰던 것 같습니다."
                        ),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_CASE, "description": "3구 직렬 배터리 홀더."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_1, "description": "낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_2, "description": "낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_3, "description": "낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_4, "description": "낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_5, "description": "낡은 건전지."}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "batteries_found", "value": True}),
                    ]
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="이미 다 챙겼습니다.")])
            ]
        ),

        # [신규] 1-1. 약품 트레이 (금고 힌트)
        KeywordId.MEDICINE_TRAY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "책상 위에 놓인 스테인리스 트레이입니다. 먹다 남은 알약들이 포장된 채로 놓여 있습니다.\n"
                                "포장지 뒷면에 성분명이 적혀 있습니다.\n\n"
                                "💊 **[ C ]** (탄소)\n"
                                "💊 **[ Ca ]** (칼슘)\n"
                                "💊 **[ Fe ]** (철분)"
                            )
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="금고 비밀번호의 단서인 것 같습니다. (주기율표 참고)"),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.PUZZLE_NOTE, "state": KeywordState.DISCOVERED}),
                    ]
                )
            ]
        ),

        # 2. 작업대 (멀티미터)
        KeywordId.WORKBENCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="workbench_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="기름에 찌든 작업대입니다. 벽에는 고정된 **[멀티미터]**와 **[정비 메모]**가 붙어 있습니다."
                        ),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.MULTIMETER, "state": KeywordState.DISCOVERED}),
                        Action(type=ActionType.UPDATE_STATE,
                               value={"keyword": KeywordId.MEMO_VOLTAGE, "state": KeywordState.DISCOVERED}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "workbench_inspected", "value": True}),
                    ]
                ),

                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="workbench_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="기름에 찌든 작업대입니다. 벽에는 고정된 **[멀티미터]**와 **[정비 메모]**가 붙어 있습니다."
                        ),
                    ]
                )
            ]
        ),
        KeywordId.MULTIMETER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="전압 측정기입니다. 건전지를 갖다 대면 전압을 알 수 있습니다."
        ),
        KeywordId.MEMO_VOLTAGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '"경고: 정격 전압 **19V**를 엄수할 것.\n\n'
                "회로 보호를 위해 전압은 반드시 **높은 곳에서 낮은 곳으로(High -> Low)** 흐르도록 배열할 것.\n\n"
                '순서가 틀리거나 전압이 맞지 않으면 역전류로 인해 감전될 수 있음."'
            ),
        ),

        # 3. 전자 금고 (키패드 + LED)
        KeywordId.ELECTRONIC_SAFE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="금고가 열려 있습니다.")]
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "전원이 켜지자 **4개의 LED**에 빨간 불이 들어왔습니다.\n"
                                "숫자 키패드가 활성화되었습니다. 어딘가에 비밀번호 힌트가 있을 것입니다."
                            )
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="`전자 금고 : [비밀번호]` 입력"),
                    ]
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="전원이 꺼져 있습니다. 4개의 LED가 모두 꺼져 있고 키패드도 반응하지 않습니다.")]
                )
            ]
        ),
        # 6. 소방 도끼 (오브젝트 - 벽에 붙어있는 상태)
        KeywordId.FIRE_AXE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="도끼를 꺼내려 했지만, **[녹슨 클램프]**가 꽉 물고 있어 꿈쩍도 하지 않습니다.",
                        ),
                        Action(
                            type=ActionType.DISCOVER_KEYWORD,
                            value=KeywordState.DISCOVERED,
                        ),
                    ]
                ),
            ],
        ),
        # 7. 녹슨 클램프 (초기 HIDDEN -> 도끼 조사 시 발견)
        KeywordId.RUSTY_CLAMP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "**[소방 도끼]**를 꽉 물고 있는 고정 장치입니다.\n\n"
                "붉은 녹이 슬어 꿈쩍도 안 합니다.\n\n"
                "화학적으로 녹을 제거해야 합니다."
            ),
        ),

    },
    combinations=[
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.SAUCE_BOTTLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value='녹슨 클램프에 산성 용액을 그대로 부었습니다.\n\n'
                          '용액은 주르륵 흘러내려 바닥으로 떨어졌고, 그중 일부가 당신의 손등에 튀었습니다!\n\n'
                          '"으악! 타는 것 같아!"',
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="[경고] 화상을 입어 체력이 감소했습니다. 용액이 흘러내리지 않게 점성을 높여야 합니다.",
                ),
            ],
        ),

        # 2. 도끼 획득
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_GEL],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="산성 젤을 발라 녹을 녹였습니다. 클램프가 풀리고 **[소방 도끼]**를 손에 넣었습니다!"),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_GEL),
                Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.FIRE_AXE_WALL),
                Action(type=ActionType.ADD_ITEM,
                       value={"name": KeywordId.FIRE_AXE, "description": "무엇이든 부술 수 있는 붉은 도끼."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "axe_obtained", "value": True}),
            ]
        ),

        # 3. 배터리 측정 및 조립 (기존 로직 유지)
        # --- [퍼즐 3] 배터리 전압 (멀티미터) ---
        # 1: 9V, 2: 6V, 3: 5V, 4: 4V, 5: 2V
        # 정답: 19V (9+6+4) -> ID 1, 2, 4
        # Action: UPDATE_ITEM_DATA 이름(extra_name)만 변경
        # 3-1. 측정 (속성 업데이트 로직)
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_1],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **9V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_1, "field": "extra_name", "value": "(9V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_1, "field": "description", "value": "측정된 전압은 9V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_2],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **6V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_2, "field": "extra_name", "value": "(6V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_2, "field": "description", "value": "측정된 전압은 6V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_3],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **5V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_3, "field": "extra_name", "value": "(5V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_3, "field": "description", "value": "측정된 전압은 5V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_4],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **4V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_4, "field": "extra_name", "value": "(4V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_4, "field": "description", "value": "측정된 전압은 4V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_5],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **2V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_5, "field": "extra_name", "value": "(2V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_5, "field": "description", "value": "측정된 전압은 2V입니다."},
                ),
            ],
        ),
        # 3-2. 조립 (정답: 19V, 순서 9->6->4 / ID 1, 2, 4)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "124"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="건전지를 순서대로(9V -> 6V -> 4V) 끼웠습니다.\n합계 19V. 완벽합니다! **[배터리 팩]**이 완성되었습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_CASE),
                # 건전지 아이템 소모 처리 (조립했으므로 제거)
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_1),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_2),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_3),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_4),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_5),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.BATTERY_PACK, "description": "안정적인 19V 전원."},
                ),
            ],
        ),
        # 3-3. 오답 (전압 틀림 예시: 9+6+5=20V -> ID 123)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "123"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="지지직! 전압 합계가 20V입니다. 19V를 맞춰야 합니다. 스파크가 튀어 손을 데었습니다.",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),
            ],
        ),
        # 3-4. 오답 (순서 틀림 예시: 4+6+9=19V -> ID 421)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "421"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="퍽! 합계는 19V지만, 낮은 전압을 먼저 연결하자 역전류가 발생했습니다. '높은 곳에서 낮은 곳으로' 연결해야 합니다.",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),
            ],
        ),
        # [신규] 빈 배터리 케이스 + 금고 (힌트)
        Combination(
            targets=[KeywordId.SAFE, KeywordId.BATTERY_CASE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="빈 케이스만 연결해서는 작동하지 않습니다. 건전지를 채워 넣어야 합니다.",
                )
            ],
        ),
        # 4. 금고 해제
        Combination(
            targets=[KeywordId.ELECTRONIC_SAFE, KeywordId.BATTERY_PACK],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="전원이 들어옵니다. LED가 깜빡입니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_PACK),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_powered", "value": True}),
            ]
        ),
        # C(6) Ca(20) Fe(26) -> 62026
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.ELECTRONIC_SAFE, "62026"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="철컥! 금고가 열리고 **[양자 가마솥]**을 발견했습니다! 이제 탈출뿐입니다!"),
                Action(type=ActionType.ADD_ITEM,
                       value={"name": KeywordId.QUANTUM_CAULDRON, "description": "전설의 조리 도구."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_opened", "value": True}),
            ]
        ),
    ]
)