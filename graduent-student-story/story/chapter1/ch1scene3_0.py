from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

# [챕터 1-3: 생태 관측소 외부]
# 수정: 화단 -> 텃밭, 단계별 물 주기(3회), 소금빵 팻말 힌트

CH1_SCENE3_0_DATA = SceneData(
    id=SceneID.CH1_SCENE3_0,
    name="생태 관측소 외부",
    body=(
        '"이런 깊은 숲 속에 연구소라니..."\n\n'
        '<img src="assets/chapter1/observatory_0.png" alt="생태 관측소" width="600">\n\n'
        "거대한 원통형 목조 건물이 숲과 하나가 된 듯 서 있습니다.\n\n"
        "지붕과 벽면은 온통 푸른 이끼와 덩굴로 뒤덮여 있고, 입구의 낡은 나무 문은 쇠사슬로 칭칭 감겨 있습니다.\n\n"
        "계단 옆 덤불 속에는 배전함이 숨겨져 있고, 길가에는 관리가 안 된 텃밭이 덩그러니 놓여 있습니다."
    ),
    initial_state={
        "garden_step": 0,  # 텃밭 상태 (0: 메마름, 1: 촉촉, 2: 새싹, 3: 꽃)
        "box_opened": False,  # 배전함 열림 여부
        "door_step": 0,
        "beach_path_inspected": False,  # 베이스캠프 경로 확인
        "panel_inspected": False,
        "puzzle_solved": False,
        # 스위치 상태 (True: ON/초록불, False: OFF/빨간불)
        "sw1": False,
        "sw2": False,
        "sw3": False,
        "sw4": False,
        "sw5": False,
    },
    on_enter_actions=[],
    keywords={
        # 0. 베이스캠프 (이동)
        KeywordId.BASECAMP: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "숲 가장자리, 나뭇가지 사이로 해변 쪽 하얀 모래와 야자수 그늘이 멀리 보입니다.\n"
                                "그쪽으로 한참 내려가면 다시 베이스캠프로 돌아갈 수 있을 것 같습니다."
                            ),
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
                                "prompt": "숲 입구 쪽으로 되돌아가 해변 베이스캠프로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="숲의 그늘을 벗어나 다시 뜨거운 모래사장으로 내려갑니다.",
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE1,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 이 숲에서 할 일이 남은 것 같습니다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 1. 텃밭 (단계별 상호작용)
        # 기존 KeywordId.FLOWERBED를 사용하되 이름을 '텃밭'으로 표시
        KeywordId.GARDEN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            name=KeywordId.GARDEN,  # 표시 이름 변경
            interactions=[
                # Step 0: 메마름 + 소금빵 팻말
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/before_flower_1.png" alt="텃밭" width="540">\n\n'
                                "바짝 마른 흙먼지만 날리는 텃밭입니다. 식물은커녕 잡초도 말라 죽었습니다.\n\n"
                                "텃밭 한가운데 팻말이 꽂혀 있습니다. 글씨 대신 그림이 그려져 있네요.\n\n"
                                "물을 주면 빵이라도 열리는 걸까요? 배가 고프니 별생각이 다 듭니다."
                            ),
                        ),
                    ],
                ),
                # Step 1: 촉촉해짐
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/before_flower_2.png" alt="텃밭" width="540">\n\n'
                                "물을 머금어 흙색이 진해졌습니다. 아주 약간 생기가 도는 것 같습니다.\n\n"
                                "하지만 아직 부족해 보입니다."
                            ),
                        ),
                    ],
                ),
                # Step 2: 새싹
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/before_flower_3.png" alt="텃밭" width="540">\n\n'
                                "놀랍게도 흙을 뚫고 작은 연두색 새싹들이 올라왔습니다!\n\n"
                                "조금만 더 있으면 꽃이 필 것 같습니다."
                            ),
                        ),
                    ],
                ),
                # Step 3: 꽃 만개 (힌트)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=3)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/flower.png" alt="텃밭" width="540">\n\n'
                                "바닷물을 듬뿍 머금은 식물들이 순식간에 자라나 꽃을 피웠습니다.\n\n"
                                "소금빵 그림이 거짓말은 아니었나 봅니다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # 2. 배전함
        KeywordId.DISTRIBUTION_BOX: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="box_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=f"배전함이 열려 있습니다. 복잡한 전선과 **[{KeywordId.CIRCUIT_PANEL}]**가 보입니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.DISTRIBUTION_BOX, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="box_opened", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "덤불 속에 회색 철제 박스가 숨겨져 있습니다. 4자리 번호 자물쇠로 잠겨 있습니다.\n\n"
                                "겉면에 귀여운 과일 스티커가 순서대로 붙어 있습니다.\n\n"
                                "🍎(사과) - 🫐(블루베리) - 🍓(딸기) - 🍈(메론)"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어  `{KeywordId.DISTRIBUTION_BOX} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
            ],
        ),
        # 3. 전선 스위치 (퍼즐 2단계 - 스위치 토글)
        KeywordId.CIRCUIT_PANEL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="panel_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_1),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_2),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_3),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_4),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SWITCH_5),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.MAIN_LEVER),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "panel_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # 성공 상태
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="power_restored", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="모든 표시등에 녹색 불이 들어왔습니다. 자물쇠에 전력이 공급되고 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.CIRCUIT_PANEL, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # 진행 중 상태 (이미지 노출)
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/panel_wire2.png" alt="배전반" width="500">\n\n'
                                "전력 공급 장치입니다. 5개의 토글 스위치가 있습니다.\n\n"
                                "초록색으로 연결되는 스위치만 켜고 **[메인 레버]**를 당겨야 전력이 복구될 것 같습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SWITCH,
                            value=["sw1", "sw2", "sw3", "sw4", "sw5"],
                        ),
                    ]
                ),
            ],
        ),
        # --- [스위치 개별 동작] (본인만 토글) ---
        KeywordId.SWITCH_1: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="딸깍! 1번 스위치를 눌렀습니다."),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw1"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"스위치 상태가 변경되었습니다. **[{KeywordId.CIRCUIT_PANEL}]**를 확인하세요.",
                        ),
                    ]
                )
            ],
        ),
        KeywordId.SWITCH_2: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="딸깍! 2번 스위치를 눌렀습니다."),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw2"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"스위치 상태가 변경되었습니다. **[{KeywordId.CIRCUIT_PANEL}]**를 확인하세요.",
                        ),
                    ]
                )
            ],
        ),
        KeywordId.SWITCH_3: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="딸깍! 3번 스위치를 눌렀습니다."),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw3"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"스위치 상태가 변경되었습니다. **[{KeywordId.CIRCUIT_PANEL}]**를 확인하세요.",
                        ),
                    ]
                )
            ],
        ),
        KeywordId.SWITCH_4: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="딸깍! 4번 스위치를 눌렀습니다."),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw4"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"스위치 상태가 변경되었습니다. **[{KeywordId.CIRCUIT_PANEL}]**를 확인하세요.",
                        ),
                    ]
                )
            ],
        ),
        KeywordId.SWITCH_5: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="딸깍! 5번 스위치를 눌렀습니다."),
                        Action(type=ActionType.TOGGLE_SWITCH, value="sw5"),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"스위치 상태가 변경되었습니다. **[{KeywordId.CIRCUIT_PANEL}]**를 확인하세요.",
                        ),
                    ]
                )
            ],
        ),
        # [메인 레버] - 정답 확인
        KeywordId.MAIN_LEVER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                # 성공
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="sw1", value=False),
                        Condition(type=ConditionType.STATE_IS, target="sw2", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw3", value=False),
                        Condition(type=ConditionType.STATE_IS, target="sw4", value=True),
                        Condition(type=ConditionType.STATE_IS, target="sw5", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "우웅- 쾅!!\n\n"
                                "레버를 올리자 5개의 전구에서 눈부신 녹색 빛이 뿜어져 나옵니다.\n\n"
                                "어딘가에 전기가 들어왔습니다!"
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "puzzle_solved", "value": True}),
                        # 스위치 상호작용 비활성화 (깔끔하게)
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_1, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_2, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_3, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_4, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SWITCH_5, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MAIN_LEVER, "state": KeywordState.INACTIVE},
                        ),
                    ],
                ),
                # 이미 성공한 후
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="puzzle_solved", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="전력이 정상적으로 공급되고 있습니다.")],
                ),
                # 실패: 하나라도 꺼져있으면 초기화
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "틱. 레버가 힘없이 다시 내려갑니다.\n\n"
                                "스파크가 살짝 튀었는지 손이 따끔하네요.\n\n"
                                "안전 장치가 작동하여 스위치가 초기화됩니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw1", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw2", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw3", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw4", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sw5", "value": False}),
                        Action(type=ActionType.MODIFY_STAMINA, value=-1),
                    ]
                ),
            ],
        ),

        # 5. 나무 문
        KeywordId.WOODEN_DOOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="door_step", value=0),
                        Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.OBSERVATORY_KEY),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/observatory_2.png" alt="문" width="520">\n\n'
                                "쇠사슬과 자물쇠로 단단히 잠겨 있습니다."
                            ),
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
Condition(type=ConditionType.STATE_IS, target="door_step", value=0),
                        Condition(type=ConditionType.HAS_ITEM, target=KeywordId.OBSERVATORY_KEY),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/observatory_2.png" alt="문" width="520">\n\n'
                                "쇠사슬과 자물쇠로 단단히 잠겨 있습니다.\n\n"
                                "배전함에서 열쇠를 찾았지만, 열쇠가 들어가기에는 구멍이 너무 작아 보입니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어  `{KeywordId.WOODEN_DOOR} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
Condition(type=ConditionType.STATE_IS, target="door_step", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/observatory_3.png" alt="문" width="520">\n\n'
                                "자물쇠는 땅바닥에 떨어졌지만, 여전히 문은 열리지 않네요.\n\n"
                                "어떻게 들어갈 방법이 없을까요?"
                            ),
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "문이 열려 있습니다. **[관측소 내부]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE, value="끼이익... 낡은 문을 열고 들어갑니다."
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="잠시 밖을 더 둘러봅니다.")
                                ],
                            },
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_unlocked", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="자물쇠는 풀렸지만 나무 문은 꿈쩍도 하지 않습니다. 들어갈 방법을 찾아야 합니다.",
                        ),
                    ],
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (생태 관측소 외부) ---
        "깊은 숲": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="피톤치드가 과하다. 건강해지기 전에 곰이랑 마주쳐서 명을 달리할 것 같은 깊이다.",
        ),
        "건물": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="거대한 참치 캔처럼 생겼다. 숲속의 은둔자가 사는 곳일까? 아니면 매드 사이언티스트의 비밀 기지? 어느 쪽이든 환영받긴 글렀다.",
        ),
        "이끼": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="건물 전체를 녹색 털옷처럼 감싸고 있다. 만지면 미끈거리는 게 기분 나쁘다. 내 졸업 논문도 이렇게 이끼가 낄 때까지 통과가 안 되고 있는데...",
        ),
        "덩굴": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="식물이 건물을 교살하고 있는 현장이다. 이어폰 줄 꼬인 것처럼 복잡하게 얽혀 있어 풀 엄두가 안 난다.",
        ),
        "쇠사슬": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="나무 문에 강철 쇠사슬이라니, 과잉 대응이다. 안에 쥬라기 공원 공룡이라도 가둬놨나? 틈새로 보이는 어둠이 심상치 않다.",
        ),
        "자물쇠": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="녹물로 코팅되어 있다. 열쇠 구멍이 있긴 한데, 맞는 열쇠를 넣어도 안 돌아갈 것 같은 '고집불통'의 관상이 보인다.",
        ),
        "계단": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="밟을 때마다 '끼익' 비명을 지른다. 공포 영화였다면 이 계단을 밟는 순간 킬러가 튀어 나왔을 것이다. 체중 감량이 시급하다.",
        ),
        "덤불": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="바스락거리는 소리가 났다. 다람쥐면 다행이고, 뱀이면 낭패다. 제발 내 발목을 노리지 말아 줘.",
        ),
        "길가": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="잡초가 무성해서 길인지 아닌지 구분이 안 간다. 여기서 길을 잃으면 헨젤과 그레텔 찍는 거다. 물론 과자 집은 없겠지만.",
        ),
        "지붕": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="나뭇가지와 이끼 덩어리에 가려 형체도 안 보인다. 비가 오면 천장 누수가 100% 확실시되는 부실 공사의 현장이다.",
        ),
        "적막": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="새소리조차 들리지 않는다. 너무 조용해서 내 심장 소리가 돌비 서라운드로 들린다. 뭔가 튀어나오기 딱 좋은 타이밍이다.",
        ),
        "공기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="축축하고 묵직하다. 곰팡이 포자가 폐 속으로 침투해 버섯 농장을 차릴 것 같은 기분이다.",
        ),
    },
    combinations=[
        # [물 주기 1단계]: 0 -> 1 (촉촉해짐)
        Combination(
            targets=[KeywordId.SEAWATER_FILLED_COCONUT, KeywordId.GARDEN],  # FILLED_COCONUT: 바닷물이 담긴 코코넛 껍질
            conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=0)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/before_flower_2.png" alt="텃밭" width="540">\n\n'
                        "코코넛 껍질에 담긴 바닷물을 메마른 흙에 부었습니다.\n\n"
                        "치이익 소리와 함께 흙이 물을 빨아들입니다.\n\n"
                        "흙이 조금 촉촉해졌습니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "garden_step", "value": 1}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SEAWATER_FILLED_COCONUT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "속을 다 비운 코코넛 껍질이다. 잘 말리면 그릇이나 수차 날개로 쓸 수 있을 것 같다.",
                    },
                ),
            ],
        ),
        # [물 주기 2단계]: 1 -> 2 (새싹)
        Combination(
            targets=[KeywordId.SEAWATER_FILLED_COCONUT, KeywordId.GARDEN],
            conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=1)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/before_flower_3.png" alt="텃밭" width="540">\n\n'
                        "한 번 더 바닷물을 붓자, 흙 속에서 무언가 꿈틀거립니다.\n\n"
                        "뿅! 귀여운 연두색 새싹들이 고개를 내밀었습니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "garden_step", "value": 2}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SEAWATER_FILLED_COCONUT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "속을 다 비운 코코넛 껍질이다. 잘 말리면 그릇이나 수차 날개로 쓸 수 있을 것 같다.",
                    },
                ),
            ],
        ),
        # [물 주기 3단계]: 2 -> 3 (개화)
        Combination(
            targets=[KeywordId.SEAWATER_FILLED_COCONUT, KeywordId.GARDEN],
            conditions=[Condition(type=ConditionType.STATE_IS, target="garden_step", value=2)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "마지막 한 방울까지 탈탈 털어 넣었습니다.\n\n"
                        "새싹들이 무럭무럭 자라나더니 순식간에 꽃망울을 터뜨립니다!\n\n"
                        "소금빵 그림이 거짓말은 아니었나 봅니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "garden_step", "value": 3}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SEAWATER_FILLED_COCONUT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "속을 다 비운 코코넛 껍질이다. 잘 말리면 그릇이나 수차 날개로 쓸 수 있을 것 같다.",
                    },
                ),
            ],
        ),
        # [배전함 암호]
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.DISTRIBUTION_BOX, "2728"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=f"달칵! 배전함이 열리고 안에서 **[관측소 열쇠]**가 보입니다.\n\n**[{KeywordId.CIRCUIT_PANEL}]**이 드러났습니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "box_opened", "value": True}),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.OBSERVATORY_KEY,
                        "description": '\n\n<img src="assets/chapter1/7324_key_2.png" alt="관측소 열쇠" width="520">\n\n'
                        "특이한 모양의 열쇠.",
                    },
                ),
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.CIRCUIT_PANEL),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.GARDEN, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # [자물쇠 해제]
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.WOODEN_DOOR, "7324"],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="door_step", value=0),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.OBSERVATORY_KEY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="쿠웅! 자물쇠가 풀려 바닥으로 떨어집니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_step", "value": 1}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.OBSERVATORY_KEY),
            ],
        ),
        # [도끼로 쇠사슬 절단]
        Combination(
            targets=[KeywordId.WOODEN_DOOR, KeywordId.FIRE_AXE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_step", value=1)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/observatory_4.png" alt="문" width="520">\n\n'
                        "좋은 말로 해서 안 듣는다면 물리 치료가 답이죠. \n\n"
                        "도끼날이 문에 박히자 묵은 체증이 내려가는 듯한 '콰직' 소리가 울려 퍼집니다.\n\n"
                        "문은 처참하게 박살 났고, 자물쇠는 바닥에 힘없이 나뒹굽니다.\n\n"
                        "진작 이렇게 할 걸 그랬네요."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_step", "value": 2}),
            ],
        ),
    ],
)
