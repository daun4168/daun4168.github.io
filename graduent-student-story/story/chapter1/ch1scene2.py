from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_DATA = SceneData(
    id=SceneID.CH1_SCENE2,
    name="난파선 잔해 (화물칸 통로)",
    body=(
        "반쯤 모래에 파묻힌 거대한 난파선 잔해 안쪽입니다. 썩은 바닷물 냄새와 쇳가루 냄새가 진동합니다.\n"
        "발밑에는 정체모를 파이프와 전선들이 뱀처럼 얽혀 있고, 벽면에는 'DANGER'라고 적힌 붉은 경고문이 희미하게 보입니다.\n\n"
        "벽 한쪽에는 먼지 쌓인 비상 캐비닛이 위태롭게 매달려 있고, "
        "복도 끝에는 육중한 강화 격벽이 굳게 닫혀 있어 더 이상 진입할 수 없습니다. "
        "저 너머가 기관실이나 하층 화물칸으로 내려가는 길인 것 같습니다.\n\n"
        "서쪽으로 돌아가면 안전한 해변 베이스캠프입니다."
    ),
    initial_state={
        "beach_path_inspected": False,
        "cabinet_searched": False,
        "door_heated": False,
        "door_frozen": False,
        "door_opened": False,
        "underground_inspected": False,
        "bucket_found": False,  # [신규] 양동이 발견 여부
        "floor_wires_collected": False,  # 바닥 전선에서 구리선을 이미 챙겼는지 여부
    },
    on_enter_actions=[
        Action(
            type=ActionType.ADD_ITEM,
            value={
                "name": "주기율표",
                "description": '<img src="assets/chapter1/periodic_table.png" alt="주기율표" width="540">',
            },
        ),
    ],
    keywords={
        KeywordId.BASECAMP: KeywordData(type=KeywordType.ALIAS, target=KeywordId.BEACH),
        KeywordId.CABINET: KeywordData(type=KeywordType.ALIAS, target=KeywordId.EMERGENCY_CABINET),
        KeywordId.BULKHEAD: KeywordData(type=KeywordType.ALIAS, target=KeywordId.IRON_DOOR),
        # 1. 해변 (돌아가는 길)
        KeywordId.BEACH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="서쪽을 보니 베이스캠프가 아지랑이 속에 보인다. 돌아가는 길도 험난해 보인다. (체력 소모 예상)",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "beach_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": ("**[해변]**으로 돌아가시겠습니까?\n\n체력이 2 소모됩니다."),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="뜨거운 모래사장을 가로질러 베이스캠프로 복귀합니다.",
                                    ),
                                    Action(type=ActionType.MODIFY_STAMINA, value=-2),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="조금 더 조사가 필요합니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 2. 비상 캐비닛 (조명탄 파밍 - 동적 생성)
        KeywordId.EMERGENCY_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cabinet_searched", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="녹슨 캐비닛을 억지로 열었습니다. 구급약품은 모두 썩었지만, 방수 포장된 **[조명탄]** 하나가 구석에 남아있습니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.FLARE,
                                "description": "선박 구조 신호용 붉은 조명탄. 마그네슘이 포함되어 점화 시 2,000도 이상의 고열을 낸다.",
                            },
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "cabinet_searched", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="텅 비어있습니다. 더 가져갈 것은 없습니다.")]
                ),
            ],
        ),
        # 4. 강화 격벽 (메인 퍼즐)
        KeywordId.IRON_DOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="군용 수송선급의 두꺼운 격벽입니다. 잠금 휠은 녹슬어 본체와 한 몸이 되었습니다. 물리적인 힘으로 여는 건 불가능해 보입니다. 재질은 고장력강(High Tensile Steel). 열역학적으로 접근해야 할 것 같습니다.",
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="잠금장치가 산산조각 나 문이 열려 있습니다. 어두운 **[지하 통로]**가 보입니다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_frozen", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="하얗게 성에가 낀 문에서 '쩡, 쩡' 하는 금속 비명 소리가 들립니다. 미세한 균열이 보입니다. 지금이라면 충격을 주어 깰 수 있을 것 같습니다.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="시뻘겋게 달아올라 엄청난 열기를 내뿜고 있습니다. 금속이 팽창해 터질 듯합니다. 지금 식혀야 합니다... 아주 급격하게.",
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="급속 냉각 수단이 필요합니다."),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="꿈쩍도 안 합니다. 틈새가 없어 지렛대도 들어가지 않습니다. 금속의 성질을 변화시켜야 합니다.",
                        ),
                    ]
                ),
            ],
        ),
        # 5. 지하 통로 (초기엔 INACTIVE, 문 열면 등장)
        KeywordId.UNDERGROUND_PASSAGE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.INACTIVE,  # 처음엔 안 보임
            description="난파선 가장 깊은 곳으로 이어지는 어둡고 축축한 계단입니다. 썩은 기름 냄새가 올라옵니다.",
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="underground_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="계단 아래는 칠흑 같은 어둠입니다. 무엇이 기다리고 있을지 모릅니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한번 **[지하 통로]**를 입력하면 이동 여부를 결정합니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "underground_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="underground_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "어두운 **[지하 통로]**로 내려가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 심호흡을 하고 어둡고 축축한 계단을 따라 내려갑니다...",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 이곳에서 할 일이 남은 것 같습니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # --- [단순 상호작용 요소 추가] ---
        # 3. 경고문 (단순 조사)
        KeywordId.WARNING_SIGN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="붉은 페인트로 칠해진 'DANGER' 문구 아래에, 부식되어 잘 안 보이지만 'High Voltage(고전압)'이라는 작은 글씨가 남아있다.\n전기가 끊긴 지 오래되어 보이지만, 본능적으로 만지고 싶지 않다.",
        ),
        # 4. 파이프 (양동이 획득)
        KeywordId.PIPE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bucket_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="발에 걸리적거리는 파이프 더미를 들춰보았습니다. 구석에 찌그러진 **[녹슨 양동이]**가 끼어 있습니다.\n힘을 주어 빼냈습니다. 구멍은 없어 보입니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.RUSTY_BUCKET,
                                "description": "바닥이 찌그러졌지만 물을 담을 수 있는 튼튼한 양동이.",
                            },
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "bucket_found", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="차가운 금속 파이프들입니다. 더 이상 쓸만한 건 없습니다.",
                        )
                    ]
                ),
            ],
        ),
        # 5. 바닥 전선 (단순 조사)
        KeywordId.FLOOR_WIRES: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "바닥에 뱀처럼 얽혀있는 전선들이다. 피복이 벗겨져 구리가 드러나 있어 밟으면 감전될지도 모른다."
            ),
            interactions=[
                # 첫 조사: 구리 전선 챙기기
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="floor_wires_collected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "살펴보니 완전히 썩어빠진 부분을 제외하면, 아직 쓸 만한 구리선이 조금 남아 있다.\n"
                                "가장 멀쩡해 보이는 구간만 골라 조심스럽게 잘라서 말아 챙겨 둔다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.COPPER_WIRE,
                                "description": (
                                    "피복이 거의 다 벗겨진 구리 전선 조각이다. 구리 자체는 멀쩡하지만, "
                                    "이 상태로 그대로 쓰면 감전 위험이 크다. 절연 처리가 필요해 보인다."
                                ),
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "floor_wires_collected", "value": True},
                        ),
                    ],
                ),
                # 이후 재조사: 이미 챙긴 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="floor_wires_collected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="쓸 만한 구리 전선은 이미 모두 걷어냈다. 남은 건 부서진 피복과 녹슨 구리 찌꺼기뿐이다.",
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # 1. 가열: 조명탄 + 격벽
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.FLARE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="치익! 조명탄을 터뜨려 문 손잡이 틈새에 꽂아 넣었습니다.\n눈부신 백색 섬광과 함께 강철이 시뻘겋게 달아오르며 팽창하기 시작합니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FLARE),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_heated", "value": True}),
            ],
        ),
        # 2. 급랭: 먼지제거제 + 격벽
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="먼지제거제를 거꾸로 뒤집어 잡고, 달궈진 문고리를 향해 액체 냉매를 발사했습니다.\n\n**콰아아-!**\n\n2,000도의 열기와 영하 50도의 냉기가 충돌했습니다. 엄청난 수증기와 함께 금속 표면에 거미줄 같은 균열이 발생합니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.AIR_DUSTER),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_frozen", "value": True}),
            ],
        ),
        # 2-1. 힌트 제공
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="차가운 강철에 냉매를 뿌려봐야 소용없습니다. '열충격'을 주려면 먼저 금속을 뜨겁게 달궈야 합니다.",
                )
            ],
        ),
        # 3. 파괴: 스패너 + 격벽 (지하 통로 등장)
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_frozen", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="스패너로 하얗게 얼어붙은 잠금장치를 가볍게 내리쳤습니다.\n\n**채앵-그랑!**\n\n유리가 깨지듯 잠금장치가 산산조각 나 바닥으로 쏟아집니다. 육중한 격벽이 끼이익 소리를 내며 열립니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_opened", "value": True}),
                # [핵심] 지하 통로 키워드 활성화 (INACTIVE -> DISCOVERED)
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.UNDERGROUND_PASSAGE, "state": KeywordState.DISCOVERED},
                ),
                Action(type=ActionType.PRINT_SYSTEM, value="**[지하 통로]**가 시야에 드러났습니다."),
            ],
        ),
    ],
)
