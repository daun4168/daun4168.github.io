from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

# [퍼즐 초기 상태]
# 난이도: 1, 3, 5번이 꺼져 있음 (F, T, F, T, F) -> 2번, 4번, 3번 순서 등으로 눌러서 해결
INITIAL_DECK_STATE = {
    "hallway_inspected": False,
    "lion_opened": False,  # 사자 금고 개방 여부
    "puzzle_solved": False,  # 배전함 퍼즐 해결 여부
    "panel_inspected": False,
    "bear_inspected": False,  # 곰 캐비닛 최초 조사 여부
    # 스위치 상태 (True: ON/초록불, False: OFF/빨간불)
    "sw1": False,
    "sw2": False,
    "sw3": False,
    "sw4": False,
    "sw5": False,
}

CH1_SCENE2_4_DATA = SceneData(
    id=SceneID.CH1_SCENE2_4,
    name="갑판 뒷편",
    initial_text="---\n## 갑판 뒷편\n---\n\n",
    body=(
        '"으아악! 내 머리! 미역 줄기 되는 줄 알았네!"\n\n'
        "문을 열자마자 소금기 머금은 강풍이 따귀를 때립니다. 난간은 엿가락처럼 휘어져 있고, "
        "갑판 중앙에는 녹슨 철제 캐비닛 두 개가 덩그러니 놓여 있습니다.\n\n"
        '<img src="assets/chapter1/bear_lion2.png" alt="철제 캐비닛" width="540">\n\n'
        "왼쪽에는 사자 캐비닛이 굳게 닫혀 있고, 오른쪽 곰 캐비닛은 문이 활짝 열려 있습니다.\n\n"
        "누군가 곰은 꺼내갔나 봅니다. 사자도 탈출하기 전에 우리가 먼저 선수를 쳐야겠습니다."
    ),
    initial_state=INITIAL_DECK_STATE,
    on_enter_actions=[],
    keywords={
        # 0. 나가기
        KeywordId.HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="바람이 너무 셉니다. 안쪽 복도로 대피해야 할 것 같습니다. 이대로 있다간 뼈가 시리겠습니다.",
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
                                "prompt": "거친 갑판을 떠나 **[복도]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="바람을 등지고 서둘러 복도로 대피합니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_0),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 갑판에 할 일이 남았습니다. 좀 더 둘러봅니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 곰 캐비닛 (열려 있음 - 힌트/맥거핀)
        # [수정] 1. 곰 캐비닛 (자물쇠 발견 로직 분리)
        KeywordId.BEAR_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                # Case 1: 처음 조사할 때 (자물쇠 발견)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bear_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "오른쪽 곰 캐비닛을 살펴봅니다.\n\n"
                                "문이 덜컹거리며 열려 있고, 안은 텅 비었습니다.\n\n"
                                "바닥을 자세히 보니 누군가 부수고 간 **[부서진 자물쇠]**가 굴러다닙니다."
                            ),
                        ),
                        Action(
                            type=ActionType.DISCOVER_KEYWORD,
                            value=KeywordId.BROKEN_LOCK,
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "bear_inspected", "value": True},
                        ),
                    ],
                ),
                # Case 2: 이미 조사한 후
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bear_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="이미 텅 빈 캐비닛입니다. 곰은 떠났고, 남은 건 바닥의 먼지뿐입니다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.BROKEN_LOCK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="이미 망가진 자물쇠. 다이얼의 첫 번째 숫자는 보이지 않고, 나머지 두 개는 '18'에 멈춰 있습니다.",
        ),
        # 2. 사자 캐비닛 (잠김 -> 배전함)
        KeywordId.LION_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                # 열린 후 (배전함 노출)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="lion_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="문이 열려 있습니다. 안에 **[배전함]**이 매립되어 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LION_CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # 닫힌 상태
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "녹슨 철문에 사자 그림이 그려져 있습니다. 입을 크게 벌리고 포효하는 모습입니다.\n"
                                "3자리 숫자를 입력하는 자물쇠가 채워져 있습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.LION_CABINET} : [비밀번호 3자리]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # 3. 배전함 (퍼즐 본체)
        KeywordId.DISTRIBUTION_PANEL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # LION_CABINET이 열릴 때 DISCOVERED로 변경됨
            interactions=[
                # Case 1: 이미 해결된 경우
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="puzzle_solved", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="모든 전구에 초록불이 들어와 있습니다. 어딘가에 전력이 공급 중입니다.",
                        )
                    ],
                ),
                # Case 2: 초기 조사 (스위치 및 레버 발견)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="panel_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="사자 뱃속에 내장이 아니라 복잡한 전선이 가득합니다. 5개의 **[스위치]**와 **[메인 레버]**가 작동을 기다리고 있습니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "panel_inspected", "value": True}),
                        # --- 요청하신 DISCOVERY ACTIONS ---
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_1),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_2),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_3),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_4),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_5),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.MAIN_LEVER),
                    ],
                    continue_matching=False,
                ),
                # Case 3: 퍼즐 진행 중 (상태 표시) - Fallback
                # [상태 안내 시작]
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("5개의 스위치 상태를 확인합니다."),
                        ),
                        Action(
                            type=ActionType.PRINT_SWITCH,
                            value=["sw1", "sw2", "sw3", "sw4", "sw5"],
                        ),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("모든 스위치를 켜고 **[메인 레버]**를 당겨야 할 것 같습니다."),
                        ),
                    ],
                ),
            ],
        ),
        # --- [청개구리 스위치] ---
        # 1번 (1, 2 토글)
        KeywordId.SWITCH_1: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="딸깍! 1번을 눌렀더니 옆에 있는 2번도 같이 깜빡거립니다.",
                        ),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw1"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw2"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="전구 배열이 바뀌었습니다. **[배전함]**을 확인해 보세요.",
                        ),
                    ]
                )
            ],
        ),
        # 2번 (1, 2, 3 토글)
        KeywordId.SWITCH_2: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE, value="딸깍! 2번을 누르자 1번과 4번도 같이 춤을 춥니다."
                        ),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw1"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw2"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw4"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="전구 배열이 바뀌었습니다. **[배전함]**을 확인해 보세요.",
                        ),
                    ]
                )
            ],
        ),
        # 3번 (2, 3, 4 토글)
        KeywordId.SWITCH_3: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="딸깍! 가운데 3번을 눌렀습니다. 1, 3, 5번이 반대로 바뀝니다.",
                        ),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw1"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw3"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw5"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="전구 배열이 바뀌었습니다. **[배전함]**을 확인해 보세요.",
                        ),
                    ]
                )
            ],
        ),
        # 4번 (3, 4, 5 토글)
        KeywordId.SWITCH_4: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="딸깍! 4번을 눌렀습니다. 2, 3, 5번도 같이 영향을 받습니다.",
                        ),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw2"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw3"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw4"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw5"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="전구 배열이 바뀌었습니다. **[배전함]**을 확인해 보세요.",
                        ),
                    ]
                )
            ],
        ),
        # 5번 (4, 5 토글)
        KeywordId.SWITCH_5: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="딸깍! 끝에 있는 5번을 눌렀습니다. 4번과 1번이 움직이네요.",
                        ),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw1"),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw4"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="전구 배열이 바뀌었습니다. **[배전함]**을 확인해 보세요.",
                        ),
                    ]
                )
            ],
        ),
        # 메인 레버 (정답 확인)
        KeywordId.MAIN_LEVER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                # 성공: 모두 True (기존 유지)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="puzzle_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("레버가 잠금장치에 '철컥' 소리와 함께 고정됩니다. 더 이상 움직이지 않습니다."),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MAIN_LEVER, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="sw1", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw2", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw3", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw4", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw5", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "우웅- 쾅!!\n\n"
                                "레버를 올리자 5개의 전구에서 눈부신 녹색 빛이 뿜어져 나옵니다.\n\n"
                                "배 전체에 웅장한 진동이 울립니다. 어딘가에 전기가 들어온 것 같습니다!"
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "puzzle_solved", "value": True}),
                        Action(
                            type=ActionType.UPDATE_CHAPTER_STATE,
                            value={"key": "basement_power_restored", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_1, "state": KeywordState.UNSEEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_2, "state": KeywordState.UNSEEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_3, "state": KeywordState.UNSEEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_4, "state": KeywordState.UNSEEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_5, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # 실패: 모든 전구 초기화 액션 추가
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "틱. 레버가 힘없이 다시 내려갑니다.\n\n"
                                "합선 방지 시스템이 작동합니다. 처음 상태로 되돌아갑니다."
                            ),
                        ),
                        # --- 초기화 액션 ---
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw1", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw2", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw3", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw4", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw5", "value": False}),
                    ]
                ),
            ],
        ),
        "미역 줄기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="머리카락이 미역 줄기처럼 엉켜서 떼어낼 수가 없다. 자연산 헤어스타일이 완성되는 중이다.",
        ),
        "소금기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="입안과 피부에 짠 기운이 가득하다. 공짜로 소금물 사우나를 즐기는 기분이지만, 목마름은 더 심해진다.",
        ),
        "따귀": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="바람이 너무 세서 진짜로 누가 때리는 것 같다. 이렇게 모래로 얻어맞으면 피부 각질 제거는 확실히 될 것이다.",
        ),
        "철제 캐비닛": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="차가운 철제 덩어리가 두개 있다. 녹슨 채로 옮기려면 용역 인력 3명이 필요할 것이다.",
        ),
        "강풍": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="선풍기 바람의 100배쯤 된다. 이걸 맞으면서 균형을 잡는 게 이 시대 최고의 코어 운동이 아닐까?",
        ),
        "난간": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="엿가락처럼 휘어져 있다. 저걸 믿고 기댈 바에야 차라리 맨손으로 벽을 짚는 게 안전하다.",
        ),
        "파도": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="철썩거리는 소리가 굉음과 같다. 바다가 우리에게 화내는 것처럼 느껴져서 괜히 죄지은 기분이다.",
        ),
        "엿가락": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="단단한 강철이 엿가락처럼 휘었다니, 대체 얼마나 강한 폭풍우가 몰아쳤던 걸까? 상상조차 하기 싫다.",
        ),
        "머리": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이미 미역 줄기 꼴이다. 탈모가 올 것 같다. 안 그래도 스트레스 때문에 많이 빠졌는데...",
        ),
        "중앙": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="태풍의 눈처럼 캐비닛 두 개가 떡하니 버티고 있다. 왜 하필 중앙일까? 풍수지리설이라도 따랐나.",
        ),
        "왼쪽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="굳게 닫힌 사자 캐비닛이 있다. 안에 사자가 들어있진 않겠지? 슈뢰딩거의 사자인가?",
        ),
        "오른쪽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="활짝 열린 곰 캐비닛이 있다. 곰이 탈출했다면 지금쯤 어디에 있을까? 제발 바다로 수영하러 갔길 바란다.",
        ),
        "선수": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="사자가 나오기 전에 내가 먼저 선수를 친다? 말은 쉽지. 물리면 파상풍 주사도 못 맞는데.",
        ),
        "곰": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="곰은 이미 탈출했다. 녀석이 남긴 흔적은 '열려 있는 캐비닛' 안에 있을 것이다. 거기서 단서를 찾아야 한다.",
        ),
        "사자": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="굳게 닫힌 캐비닛 문에 사자가 그려져 있다. 열린 캐비닛을 먼저 뒤져서 힌트를 얻지 못하면, 이 사자는 영원히 입을 다물고 있을 것이다.",
        ),
        "캐비닛": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="두 개의 캐비닛이 있다. 하나는 열렸고, 하나는 잠겼다. 열린 곳을 먼저 조사하는게 좋겠다.",
        ),
    },
    combinations=[
        # 사자 캐비닛 잠금 해제 (Li=3, O=8, N=7 -> 387)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.LION_CABINET, "387"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "철컥! 덜컹!\n"
                        "자물쇠가 풀리고 사자 캐비닛이 열립니다. 안에는 맹수 대신 복잡한 **[배전함]**과 스위치들이 들어있습니다.\n"
                        "선장이 숨기고 싶었던 건 사자가 아니라 전기였나 봅니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "lion_opened", "value": True}),
                # 배전함 및 스위치 발견 처리
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.DISTRIBUTION_PANEL),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.BEAR_CABINET, "state": KeywordState.UNSEEN},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.BROKEN_LOCK, "state": KeywordState.UNSEEN},
                ),
            ],
        )
    ],
)
