from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE8_DATA = SceneData(
    id=SceneID.CH1_SCENE8,
    name="가파른 절벽 (바람의 언덕)",
    initial_text=(
        "석회 동굴 벽을 짚고 좁은 협곡을 비집고 나오자, 갑자기 하늘이 쫙 열리며 바람이 얼굴을 후려친다.\n"
        "발밑은 절벽 가장자리, 아래로는 지나온 숲과 늪, 해변이 한눈에 내려다보인다.\n"
        "위쪽으로는 바람에 휘날리는 잔디와 바위가 이어진 완만한 언덕이 펼쳐져 있고, 그 끝에는 산 정상의 평평한 능선이 보인다.\n\n"
        '절벽 바로 옆에는 난파선에서 끌어올린 장비 상자가 무심하게 놓여 있다. 옆면에는 희미하게 "DECK WINCH KIT"라는 글자가 보인다.\n'
        "당신은 직감한다. '저걸 안 쓰고 여기서 장비를 직접 들고 올라가면, 내가 먼저 사라질 것이다.'"
    ),
    initial_state={
        "bundle_opened": False,
        "pulley_installed": False,
        "rope_threaded": False,
        "basket_attached": False,
        "equipment_loaded": False,
        "counterweight_ready": False,
        "equipment_up": False,
        "barometer_built": False,
        "storm_coming": True,
        "storm_alerted": False,
        "safety_line_set": False,
        "cliff_path_inspected": False,
        "back_path_inspected": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # --- ALIAS ---
        KeywordId.CLIFF_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        KeywordId.CLIFF_UP_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        KeywordId.CLIFF_BACK_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        KeywordId.BAROMETER_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.INACTIVE, description=None, interactions=[]
        ),
        # --- 지형/환경 ---
        KeywordId.CLIFF_FACE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "눈앞의 절벽은 거의 수직에 가깝다. 군데군데 튀어나온 바위 턱이 손잡이 역할을 해 줄 것 같지만, "
                "무거운 장비까지 짊어지고 오르기에는 무리다.\n"
                "잘못 미끄러지면 밑의 숲과 늪을 한 번에 관통하는 체험을 하게 될 것이다."
            ),
        ),
        KeywordId.PULLEY_ANCHOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "절벽 상단 가까이에 튀어나온 단단한 바위 턱이 보인다.\n"
                "로프나 도르래를 걸기에는 딱 좋은 모양이다. "
                "이미 누군가 여기서 비슷한 짓을 해 본 흔적(닳은 자국)도 보인다."
            ),
        ),
        KeywordId.STONE_PILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "절벽 아래에는 주먹에서 머리통 크기까지 다양한 돌들이 쌓여 있다.\n"
                "몇 개만 골라 묶으면 그럴듯한 평형추가 될 것 같다."
            ),
        ),
        KeywordId.CLIFF_SPRING: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "절벽 아래 바위 틈에서 맑은 물이 조금씩 스며 나와 작은 샘을 이루고 있다.\n"
                "기압계에 쓸 물을 채우기에 딱 좋다."
            ),
        ),
        # --- 장비 상자 ---
        KeywordId.EQUIPMENT_BUNDLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description="덮개가 반쯤 열린 장비 상자다. 안에 무엇이 들어 있는지 아직 제대로 살펴보지 않았다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bundle_opened", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "상자를 열어 보니, 선박 갑판에서 짐을 올리고 내릴 때 쓰던 장비들이 잔뜩 들어 있다.\n"
                                "**[등반용 로프]**, 낡았지만 쓸 만한 **[도르래 바퀴]**, 큼직한 **[그물 바구니]**, "
                                "그리고 서로 이어 붙일 수 있는 **[금속 파이프 묶음]**이 눈에 띈다.\n"
                                "한쪽에는 **[접지 말뚝]**, **[접지 케이블]**, **[안테나 케이블]**, 그리고 "
                                "수상한 메모가 붙은 **[튜닝 코일]**도 있다.\n"
                                "이 키트 하나로 절벽 위에 안테나와 접지를 세팅하라는 뜻인 것 같다. 담당 교수의 악의가 느껴진다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.CLIMBING_ROPE,
                                "description": "선박에서 쓰던 튼튼한 등반용 로프다. 사람과 장비를 동시에 지탱할 정도다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.PULLEY_WHEEL,
                                "description": "무거운 짐을 들어 올릴 때 사용하는 금속 도르래 바퀴다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.CARGO_NET,
                                "description": "부피 큰 장비를 한 번에 담을 수 있는 그물 바구니다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.METAL_PIPE_BUNDLE,
                                "description": "서로 이어 붙이면 높은 안테나 기둥이 될 수 있는 금속 파이프 묶음이다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.GROUND_ROD,
                                "description": "뾰족한 끝을 가진 긴 금속 말뚝이다. 젖은 흙에 박아 접지용으로 쓰기 좋다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.GROUND_CABLE,
                                "description": "굵은 피복으로 감싼 구리 케이블이다. 안테나와 접지를 연결하는 데 사용한다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.ANTENNA_CABLE,
                                "description": "MK-II 통신 모듈과 고지대 안테나를 연결할 긴 케이블이다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.TUNING_COIL,
                                "description": '메모가 붙어 있다. "코일 감은 수 조절용. 나중에 꼭 필요함(중요)."',
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "bundle_opened", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bundle_opened", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="상자에서 쓸 만한 장비는 이미 모두 꺼내 두었다.",
                        )
                    ],
                ),
            ],
        ),
        # --- 기압계용 상자 ---
        KeywordId.WEATHER_CRATE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description="절벽 옆에 반쯤 묻힌 작은 관측 장비 상자가 보인다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="barometer_built", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "상자를 비틀어 열어 보니, 깨진 온도계와 녹슨 삼각대, 그리고 멀쩡한 **작은 플라스틱 병**과 "
                                "**플라스틱 빨대 조각**이 나온다.\n"
                                "공기에 민감한 간이 기압계를 만들 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.SMALL_BOTTLE,
                                "description": "투명한 작은 플라스틱 병이다. 뚜껑은 없지만 입구가 단단하다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.PLASTIC_STRAW,
                                "description": "잘려 나간 플라스틱 빨대 조각이다.",
                            },
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="barometer_built", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="상자 안에는 이제 쓸 만한 것이 남아 있지 않다.",
                        )
                    ],
                ),
            ],
        ),
        # --- 간이 기압계 ---
        KeywordId.IMPROVISED_BAROMETER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="플라스틱 병과 빨대를 이용해 만든 간이 기압계다. 물기둥 높이로 기압 변화를 볼 수 있다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="barometer_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="storm_alerted", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기압계를 눈높이에 맞춰 바라본다.\n"
                                "빨대 안 물기둥이 처음보다 확실히 더 올라가 있다. 내부 공기가 팽창하면서 물을 밀어 올리는 모양이다.\n\n"
                                "— 기압이 빠르게 떨어지고 있다. 곧 이쪽으로 폭풍이 몰려올 것이다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.WEATHER_LOG,
                                "description": '기압 변화를 간단히 적어 둔 메모다. "수십 분 내 강한 돌풍 예상"이라고 쓰여 있다.',
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "storm_alerted", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="barometer_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="storm_alerted", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "물기둥은 이미 한계치에 가까운 높이를 유지하고 있다.\n"
                                "폭풍은 언제 들이닥쳐도 이상하지 않은 상태다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # --- 이동 포탈: 위 / 아래 ---
        KeywordId.CLIFF_TOP_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 첫 조사
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "절벽 옆으로 사람 한 명 겨우 지나갈 수 있는 좁은 바위 길이 위쪽으로 이어져 있다.\n"
                                "옆은 그대로 낭떠러지라, 바람이 강하게 불 때마다 몸이 한쪽으로 휘청인다.\n"
                                "이 길을 따라 올라가면 산 정상의 평평한 능선으로 이어질 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "cliff_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 장비를 아직 올리지 못했을 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="equipment_up", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "지금 혼자 올라가면 절벽 위에는 몸밖에 없고, 중요한 장비는 전부 아래에 남게 된다.\n"
                                "MK-II 수리를 위해서는 안테나와 접지 재료를 위로 먼저 올려야 할 것 같다."
                            ),
                        )
                    ],
                ),
                # 장비는 위로 올렸지만 안전 로프가 없을 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="equipment_up", value=True),
                        Condition(type=ConditionType.STATE_IS, target="safety_line_set", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "장비는 이미 절벽 위로 올려 두었다.\n"
                                    "하지만 이 좁은 길을 **안전 로프 없이** 올라가려면 꽤 위험하다.\n"
                                    "조심스럽게 절벽 위로 올라가시겠습니까?\n"
                                    "오르내리는 동안 **체력이 2 소모**됩니다."
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 바위에 몸을 최대한 붙이고, 강풍의 간격을 계산해 한 걸음씩 앞으로 나아간다.\n"
                                            "두 번쯤 심장이 멎는 줄 알았지만, 결국 산 정상의 능선에 올라서는 데 성공한다."
                                        ),
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE9,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_SYSTEM,
                                        value="일단은 안전 로프를 설치하는 방법이 없는지 더 고민해 보기로 한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
                # 장비도 올렸고 안전 로프도 있는 경우
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="equipment_up", value=True),
                        Condition(type=ConditionType.STATE_IS, target="safety_line_set", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "장비는 이미 절벽 위에 있고, 안전 로프도 설치되어 있다.\n"
                                    "로프에 몸을 연결하고 산 정상 능선으로 올라가시겠습니까?\n"
                                    "오르내리는 동안 **체력이 1 소모**됩니다."
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 하네스를 한 번 더 확인한 뒤, 절벽 옆 좁은 길을 따라 위로 올라간다.\n"
                                            "바람이 불 때마다 로프가 몸을 잡아 주어, 몇 번의 위기 끝에 안전하게 능선에 도달한다."
                                        ),
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-1,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE9,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_SYSTEM,
                                        value="아직은 마음의 준비가 덜 된 것 같다. 매듭을 한 번 더 확인한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        KeywordId.CLIFF_BACK_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="back_path_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "뒤쪽 협곡 틈으로는 석회 동굴로 내려가는 가파른 경사로가 이어져 있다.\n"
                                "바닥이 미끄러워 보이지만, 조심해서 내려가면 다시 동굴 홀로 돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "back_path_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="back_path_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "석회 동굴로 되돌아가시겠습니까?\n내려가고 올라오는 동안 **체력이 2 소모**됩니다.",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 바위를 짚으며 조심스럽게 협곡을 따라 석회 동굴 쪽으로 내려간다.",
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE6,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_SYSTEM,
                                        value="일단은 절벽 위 작업을 더 진행해 보기로 한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # --- 도르래 설치 ---
        Combination(
            targets=[KeywordId.PULLEY_WHEEL, KeywordId.PULLEY_ANCHOR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PULLEY_WHEEL),
                Condition(type=ConditionType.STATE_IS, target="pulley_installed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "도르래 바퀴를 바위 턱에 대고 볼트와 너트로 단단히 고정한다.\n"
                        "이제 로프를 걸면 제대로 된 승강 장치를 만들 수 있을 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_installed", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PULLEY_WHEEL, KeywordId.PULLEY_ANCHOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="pulley_installed", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="도르래는 이미 바위 턱에 단단히 고정되어 있다.",
                )
            ],
        ),
        # --- 로프를 도르래에 걸기 ---
        Combination(
            targets=[KeywordId.CLIMBING_ROPE, KeywordId.PULLEY_WHEEL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="pulley_installed", value=True),
                Condition(type=ConditionType.STATE_IS, target="rope_threaded", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="등반용 로프를 도르래 바퀴에 통과시켰다. 양쪽 끝이 절벽 위아래로 자연스럽게 늘어진다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "rope_threaded", "value": True},
                ),
            ],
        ),
        # --- 그물 바구니를 로프 끝에 연결 ---
        Combination(
            targets=[KeywordId.CARGO_NET, KeywordId.CLIMBING_ROPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CARGO_NET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="rope_threaded", value=True),
                Condition(type=ConditionType.STATE_IS, target="basket_attached", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="로프의 아래쪽 끝에 그물 바구니를 단단히 묶었다. 이제 장비를 실어 올릴 수 있다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "basket_attached", "value": True},
                ),
            ],
        ),
        # --- 장비 상자를 그물에 싣기 ---
        Combination(
            targets=[KeywordId.EQUIPMENT_BUNDLE, KeywordId.CARGO_NET],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="basket_attached", value=True),
                Condition(type=ConditionType.STATE_IS, target="equipment_loaded", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "금속 파이프와 각종 장비를 그물 바구니 안으로 밀어 넣는다.\n"
                        "그물 줄이 팽팽해지며 무게를 받아낸다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "equipment_loaded", "value": True},
                ),
            ],
        ),
        # --- 평형추 만들기 ---
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.CLIMBING_ROPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="rope_threaded", value=True),
                Condition(type=ConditionType.STATE_IS, target="counterweight_ready", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "로프의 반대쪽 끝에 적당한 크기의 돌들을 여러 개 묶어 매단다.\n"
                        "평형추가 생기자, 장비 쪽 로프의 장력이 눈에 띄게 줄어든다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "counterweight_ready", "value": True},
                ),
            ],
        ),
        # --- 장비 끌어올리기 ---
        Combination(
            targets=[KeywordId.CLIMBING_ROPE, KeywordId.EQUIPMENT_BUNDLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="equipment_loaded", value=True),
                Condition(type=ConditionType.STATE_IS, target="counterweight_ready", value=True),
                Condition(type=ConditionType.STATE_IS, target="equipment_up", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "로프를 서서히 당기자 그물 바구니가 끌려 올라간다.\n"
                        "평형추가 대부분의 무게를 떠받쳐 주어, 당신은 방향만 잡아 주듯 로프를 조절하기만 하면 된다.\n"
                        "잠시 후, 절벽 위에서 금속이 부딪히는 소리가 나며 장비가 안전하게 능선 위에 안착한다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "equipment_up", "value": True},
                ),
            ],
        ),
        # --- 안전 로프 설치 ---
        Combination(
            targets=[KeywordId.CLIMBING_ROPE, KeywordId.CLIFF_TOP_PATH],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="rope_threaded", value=True),
                Condition(type=ConditionType.STATE_IS, target="safety_line_set", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "로프의 한쪽 끝을 절벽 아래쪽 굵은 바위에, 다른 쪽 끝을 절벽 위쪽 바위에 고정한다.\n"
                        "중간에는 하네스를 연결할 수 있는 고리를 하나 만들어 두었다.\n"
                        "이제 이 길을 오르내릴 때, 로프가 마지막 안전장치가 되어 줄 것이다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "safety_line_set", "value": True},
                ),
            ],
        ),
        # --- 기압계 제작 ---
        Combination(
            targets=[KeywordId.SMALL_BOTTLE, KeywordId.CLIFF_SPRING],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SMALL_BOTTLE),
                Condition(type=ConditionType.STATE_IS, target="barometer_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="작은 플라스틱 병을 샘물에 담가 절반 정도까지 물을 채운다.",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.SMALL_BOTTLE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WATER_FILLED_BOTTLE,
                        "description": "맑은 물이 절반쯤 채워진 작은 플라스틱 병이다.",
                    },
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.WATER_FILLED_BOTTLE, KeywordId.PLASTIC_STRAW],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATER_FILLED_BOTTLE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_STRAW),
                Condition(type=ConditionType.STATE_IS, target="barometer_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "플라스틱 빨대를 병 입구에 꽂고, 주변을 천 조각과 테이프로 임시로 막는다.\n"
                        "병을 세워 두자 빨대 안으로 물이 일정 높이까지 올라온다.\n"
                        "기압이 떨어지면 공기가 팽창하면서 물기둥 높이가 변할 것이다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.WATER_FILLED_BOTTLE,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.PLASTIC_STRAW,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.IMPROVISED_BAROMETER,
                        "description": "플라스틱 병과 빨대로 만든 간이 기압계다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "barometer_built", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_KEYWORD_DATA,
                    value={
                        "keyword": KeywordId.IMPROVISED_BAROMETER,
                        "field": "state",
                        "value": KeywordState.DISCOVERED,
                    },
                ),
            ],
        ),
    ],
)
