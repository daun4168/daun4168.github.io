from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_7_DATA = SceneData(
    id=SceneID.CH1_SCENE2_7,
    name="지하 연구실",
    body=(
        '"으스스하네... 여긴 냉동 창고를 개조한 건가?"\n\n'
        "서늘한 냉기가 감도는 은밀한 연구실입니다. 벽면은 방음재로 덮여 있고, 알 수 없는 기계 장치들이 웅웅거립니다.\n"
        "중앙에는 연구용 책상이 있고, 그 위에는 약품 트레이가 놓여 있습니다. 벽 쪽에는 기름때 묻은 작업대가 있습니다.\n\n"
        "가장 안쪽 구석에는 육중한 전자 금고가 보이고, 반대편 벽에는 소방 도끼가 단단히 고정되어 있습니다.\n"
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
        KeywordId.AXE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.FIRE_AXE),
        KeywordId.SAFE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.ELECTRONIC_SAFE),
        KeywordId.DESK: KeywordData(type=KeywordType.ALIAS, target=KeywordId.LAB_DESK),
        KeywordId.TRAY: KeywordData(type=KeywordType.ALIAS, target=KeywordId.MEDICINE_TRAY),
        # 0. 나가는 길 (지하 복도)
        KeywordId.TOXIC_CORRIDOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                # Case 1: 첫 조사 (설명 출력)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="corridor_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="복도로 나가는 문입니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "corridor_inspected", "value": True}),
                    ],
                    continue_matching=True,  # 설명 후 바로 이동 조건 체크로 넘어감
                ),
                # Case 2: 금고를 아직 안 열었을 때 (이동 차단)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_opened", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "아직 나갈 수 없습니다. 여기까지 와서 빈손으로 돌아갈 순 없습니다.\n\n"
                                "반드시 금고를 열어보아야 합니다."
                            ),
                        )
                    ],
                ),
                # Case 3: 금고를 열었을 때 (이동 허용)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "산업용 배터리를 챙겼습니다. **[지하 복도]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="연구실을 빠져나갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_5),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE, value="아직 더 살펴볼 게 남았는지 확인합니다."
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
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
                            value="책상 서랍을 열자 **[건전지] 5개**와 **[배터리 케이스]**가 굴러다닙니다. 실험용으로 쓰던 것 같습니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.BATTERY_CASE,
                                "description": "3구 직렬 배터리 홀더. `배터리 케이스 : 123` 처럼 건전지 번호를 입력해 조립한다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_1, "description": "낡은 건전지."}
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_2, "description": "낡은 건전지.", "silent": True},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_3, "description": "낡은 건전지.", "silent": True},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_4, "description": "낡은 건전지.", "silent": True},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_5, "description": "낡은 건전지.", "silent": True},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "batteries_found", "value": True}),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[건전지 2], [건전지 3], [건전지 4], [건전지 5]**를 **주머니**에 넣었습니다.",
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="이미 다 챙겼습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LAB_DESK, "state": KeywordState.UNSEEN},
                        ),
                    ]
                ),
            ],
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
                                '<img src="assets/chapter1/pills2.png" alt="약" width="520">\n\n'
                                "책상 위에 놓인 스테인리스 트레이입니다.\n\n"
                                "옆에 [실험 노트]가 놓여 있습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.DISCOVER_KEYWORD,
                            value=KeywordId.LAB_NOTE,
                        ),
                    ]
                )
            ],
        ),
        KeywordId.LAB_NOTE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "노트에는 비커 그림과 함께 실험 결과가 적혀 있습니다. \n\n"
                                "**<침전 반응 테스트>**\n\n"
                                "알약 하나는 가벼워 표면에 뜬다.\n\n"
                                "알약 둘은 결합하여 그 아래에 부유한다.\n\n"
                                "일곱개 이상의 알약을 투입하면 무거워 바닥에 가라앉는다.\n\n"
                            ),
                        ),
                    ]
                )
            ],
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
                            value="기름에 찌든 작업대입니다. 벽에는 고정된 **[멀티미터]**와 **[정비 메모]**가 붙어 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MULTIMETER, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MEMO_VOLTAGE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "workbench_inspected", "value": True}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="workbench_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="기름에 찌든 작업대입니다. 벽에는 고정된 **[멀티미터]**와 **[정비 메모]**가 붙어 있습니다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.MULTIMETER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="전압 측정기입니다. 건전지를 갖다 대면 전압을 알 수 있습니다.",
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
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="금고가 열려 있습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.ELECTRONIC_SAFE, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/led_keypad.png" alt="키패드" width="220">\n\n'
                                "전원이 켜지자 4개의 LED에 빨간 불이 들어왔습니다.\n"
                                "숫자 키패드가 활성화되었습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.ELECTRONIC_SAFE} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="전원이 꺼져 있습니다. 4개의 LED가 모두 꺼져 있고 키패드도 반응하지 않습니다.",
                        )
                    ]
                ),
            ],
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
                            value=KeywordId.RUSTY_CLAMP,
                        ),
                    ]
                ),
            ],
        ),
        # 7. 녹슨 클램프 (초기 HIDDEN -> 도끼 조사 시 발견)
        KeywordId.RUSTY_CLAMP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                # Case 1: 녹 제거 후 (도끼 획득 상태)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="axe_obtained", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산성 젤이 닿은 부분이 하얗게 부식되어 녹아내렸습니다. 클램프는 힘없이 입을 벌리고 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RUSTY_CLAMP, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # Case 2: 녹 제거 전 (기본 상태)
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[소방 도끼]**를 꽉 물고 있는 고정 장치입니다.\n\n"
                                "붉은 녹이 슬어 꿈쩍도 안 합니다.\n\n"
                                "화학적으로 녹을 제거해야 합니다."
                            ),
                        )
                    ]
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (지하 연구실) ---
        "냉동 창고": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="개조 전에는 여기서 참치를 얼렸을까? 지금은 내 몸이 얼고 있다.",
        ),
        "서늘한 냉기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="에어컨 18도 설정해놓고 이불 덮고 있는 느낌이다. 단지 이불이 없을 뿐.",
        ),
        "방음재": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="소리를 먹어치우는 스펀지 같다. 여기서 비명을 질러도 아무도 모를 것이다. 소름 돋는다.",
        ),
        "기계 장치": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="복잡한 전선과 램프가 뒤엉켜 있다. 공대생의 악몽을 시각화하면 이런 모습일 것이다.",
        ),
        "기름때": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="오래된 엔진 오일 냄새가 난다. 작업복에 묻으면 절대 안 지워질 것 같은 강력한 얼룩이다.",
        ),
        "반대편 벽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="도끼가 걸려 있어 살벌하다. 인테리어 점수는 0점, 생존 점수는 100점이다.",
        ),
        "개조": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="불법 개조의 냄새가 난다. 건축법과 소방법을 가볍게 무시한 설계다. 구청에 신고하면 포상금을 받을 수 있을까?",
        ),
        "천장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="낮고 압박감이 든다. 정체불명의 액체가 결로현상처럼 맺혀 뚝뚝 떨어진다. 맞으면 머리가 벗겨질까 봐 피하고 싶다.",
        ),
        "바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="차가운 금속 타일이다. 냉기가 신발 밑창을 뚫고 올라와 척추를 얼리고 있다. 수면 양말이 간절하다.",
        ),
        "소리": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="웅웅거리는 저주파 소음이 이명처럼 들린다. 계속 듣고 있으면 정신이 피폐해질 것 같은 '공대 기숙사 냉장고' 소리다.",
        ),
        "조명": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="창백한 형광등 불빛이다. 안 그래도 안 좋은 내 안색을 더욱 시체처럼 보이게 만든다.",
        ),
        "전선": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="기계 뒤편에 스파게티 면처럼 엉켜 있다. 선정리를 해주고 싶은 강박이 들지만, 건드리면 100% 감전될 것이다.",
        ),
        "은밀": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="지하 깊은 곳에 숨겨진 연구실이라니. 여기서 무슨 불법 실험을 자행했을지 상상조차 하기 싫다.",
        ),
    },
    combinations=[
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_SOURCE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="녹슨 클램프에 산성 용액을 그대로 부었습니다.\n\n"
                    "용액은 주르륵 흘러내려 바닥으로 떨어졌고, 그중 일부가 당신의 손등에 튀었습니다!\n\n"
                    '"으악! 타는 것 같아!"',
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-2),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="[경고] 화상을 입어 체력이 감소했습니다. 용액이 흘러내리지 않게 점성을 높여야 합니다.",
                ),
            ],
        ),
        # 2. 도끼 획득
        Combination(
            conditions=[Condition(type=ConditionType.STATE_IS, target="axe_obtained", value=False)],
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_GEL],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="산성 젤을 발라 녹을 녹였습니다. 클램프가 풀리고 **[소방 도끼]**를 손에 넣었습니다!",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_GEL),
                Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.FIRE_AXE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.FIRE_AXE, "description": "무엇이든 부술 수 있는 붉은 도끼."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "axe_obtained", "value": True}),
            ],
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
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.WORKBENCH, "state": KeywordState.UNSEEN},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.MEMO_VOLTAGE, "state": KeywordState.UNSEEN},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.MULTIMETER, "state": KeywordState.UNSEEN},
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
            ],
        ),
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.ELECTRONIC_SAFE, "10878538"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="*띠리릭- 철컥!* 정답입니다.\n\n"
                    "금고 문이 열렸습니다.\n\n"
                    "안에서 묵직한 **[산업용 배터리]**를 발견했습니다!\n\n"
                    "이제 탈출뿐입니다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.HEAVY_BATTERY, "description": "양자 가마솥을 위한 대용량 배터리."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_opened", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.PERIODIC_TABLE),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.LAB_NOTE, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.MEDICINE_TRAY, "state": KeywordState.UNSEEN},
                ),
                Action(type=ActionType.UPDATE_CHAPTER_STATE, value={"key": "distiller_state", "value": 1}),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="시간이 꽤나 지난 것 같네요. 도끼를 얻었다면 베이스캠프로 돌아가보는 것이 좋겠습니다.",
                ),
            ],
        ),
    ],
)
