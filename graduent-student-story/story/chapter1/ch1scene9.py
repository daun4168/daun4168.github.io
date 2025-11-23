from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE9_DATA = SceneData(
    id=SceneID.CH1_SCENE9,
    name="산 정상 (번개의 제단)",
    initial_text=(
        "절벽 옆 좁은 길을 따라 한참을 오르자, 경사가 느려지고 시야가 한 번 더 트인다.\n"
        "당신은 숨을 몰아쉬며 평평한 암반 위에 올라선다.\n\n"
        "사방이 탁 트여 있다. 멀리 바다와 섬의 윤곽이 작게 보이고, 머리 위에는 먹구름이 거대한 돔처럼 하늘을 덮고 있다.\n"
        "귀에는 멀리서 울려오는 천둥소리와, 공기가 마찰하는 듯한 낮은 윙— 소리가 섞여 들려온다.\n\n"
        "이곳은 무선 안테나를 세우기에 최적의 장소이자, 번개를 맞기에도 최적의 장소다.\n"
        "당신은 베이스캠프에 둘 MK-II를 떠올린다. '여기서 설계를 끝내고, 저 아래로 가져가면 된다.'"
    ),
    initial_state={
        "antenna_assembled": False,
        "mast_fixed": False,
        "ground_rod_set": False,
        "grounding_done": False,
        "lightning_event_done": False,
        "coil_state": 0,
        "coil_tuned": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # --- ALIAS ---
        KeywordId.SUMMIT_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        KeywordId.STORM_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        KeywordId.ANTENNA_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.INACTIVE, description=None, interactions=[]
        ),
        KeywordId.TUNING_ALIAS: KeywordData(
            type=KeywordType.ALIAS, state=KeywordState.DISCOVERED, description=None, interactions=[]
        ),
        # --- 지형/환경 ---
        KeywordId.SUMMIT_ROCK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "넓은 암반 지대다. 중앙에는 자연적으로 패인 홈과 바위 틈이 있어 기둥을 세우기 좋게 생겼다.\n"
                "바닥에는 예전에 누군가 장비를 세웠던 듯한 자국이 희미하게 남아 있다."
            ),
        ),
        KeywordId.WET_SOIL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "암반 한쪽 끝에는 흙이 모여 있고, 안개비와 폭포수의 일부가 스며들어 촉촉하게 젖어 있다.\n"
                "접지 말뚝을 박기에 충분한 깊이로 보인다."
            ),
        ),
        KeywordId.STORM_SKY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "먹구름이 머리 위에서 천천히 소용돌이친다. 가끔 구름 사이에서 희미한 번개가 번쩍이고, "
                "바로 뒤이어 낮게 깔린 천둥소리가 들린다.\n"
                "조금만 더 기다리면 이 정상 위로도 본격적인 번개가 내리칠 것 같다."
            ),
        ),
        # --- 안테나, 접지 ---
        KeywordId.ANTENNA_MAST: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="아직 조립되지 않은 안테나 기둥이다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="금속 파이프들을 아직 서로 이어붙이지 않았다. 스패너를 써서 기둥처럼 조립해야 한다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                        Condition(type=ConditionType.STATE_IS, target="mast_fixed", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="금속 파이프를 이어 붙여 긴 기둥을 만들었다. 이제 암반에 제대로 고정해야 한다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                        Condition(type=ConditionType.STATE_IS, target="mast_fixed", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "금속 안테나 기둥이 암반 틈 사이에 안정적으로 서 있다.\n"
                                "꼭대기는 먹구름 속으로 곧게 뻗어 있어 번개를 유도하기에 딱 좋아 보인다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        KeywordId.GROUND_ROD_TOP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="젖은 흙에 박힌 접지 말뚝의 머리 부분이다.",
        ),
        # --- 휴대용 테스트 모듈 (작은 MK-II 뇌) ---
        KeywordId.MK_II_SUMMIT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "베이스캠프의 MK-II 본체에서 떼어온 통신·제어 모듈이다.\n"
                "이곳에서 회로와 코일을 시험한 뒤, 그대로 아래에 있는 본체에 옮겨 붙일 수 있다."
            ),
        ),
        # --- 튜닝 패널 ---
        KeywordId.TUNING_PANEL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "휴대용 모듈 옆에는 세 단계로 나뉜 작은 다이얼이 있다.\n"
                "메모에는 이렇게 적혀 있다.\n"
                '"1: 고주파 잡음 / 2: 구조 위성 대역 / 3: 저주파 간섭"'
            ),
        ),
    },
    combinations=[
        # --- 안테나 기둥 조립: METAL_PIPE_BUNDLE + SPANNER ---
        Combination(
            targets=[KeywordId.METAL_PIPE_BUNDLE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE_BUNDLE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "금속 파이프들을 하나씩 이어 붙이고, 스패너를 이용해 볼트를 단단히 조인다.\n"
                        "잠시 후, 사람 키 몇 배는 되는 길이의 안테나 기둥이 완성된다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_assembled", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_KEYWORD_DATA,
                    value={"keyword": KeywordId.ANTENNA_MAST, "field": "state", "value": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_KEYWORD_DATA,
                    value={"keyword": KeywordId.ANTENNA_ALIAS, "field": "state", "value": KeywordState.DISCOVERED},
                ),
            ],
        ),
        # --- 안테나 기둥 고정: ANTENNA_MAST + SUMMIT_ROCK ---
        Combination(
            targets=[KeywordId.ANTENNA_MAST, KeywordId.SUMMIT_ROCK],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                Condition(type=ConditionType.STATE_IS, target="mast_fixed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "암반의 자연스러운 홈과 틈을 이용해 안테나 기둥 아랫부분을 끼워 넣고, 주변 돌조각으로 틈을 메워 쐐기처럼 고정한다.\n"
                        "손으로 흔들어 보아도 웬만한 바람에는 끄덕없을 만큼 단단하다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mast_fixed", "value": True},
                ),
            ],
        ),
        # --- 접지 말뚝 박기: GROUND_ROD + WET_SOIL ---
        Combination(
            targets=[KeywordId.GROUND_ROD, KeywordId.WET_SOIL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.GROUND_ROD),
                Condition(type=ConditionType.STATE_IS, target="ground_rod_set", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "접지 말뚝 끝을 젖은 흙 위에 세우고, 돌과 스패너 손잡이로 여러 번 두드린다.\n"
                        "잠시 후, 말뚝 대부분이 흙 속으로 들어가고 윗부분만 살짝 남는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "ground_rod_set", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_KEYWORD_DATA,
                    value={"keyword": KeywordId.GROUND_ROD_TOP, "field": "state", "value": KeywordState.DISCOVERED},
                ),
            ],
        ),
        # --- 접지 케이블 연결: GROUND_CABLE + ANTENNA_MAST / GROUND_ROD_TOP ---
        Combination(
            targets=[KeywordId.GROUND_CABLE, KeywordId.ANTENNA_MAST],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.GROUND_CABLE),
                Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                Condition(type=ConditionType.STATE_IS, target="ground_rod_set", value=True),
                Condition(type=ConditionType.STATE_IS, target="grounding_done", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="접지 케이블 한쪽 끝을 안테나 기둥 아래쪽에 여러 번 감아 단단히 고정한다.",
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.GROUND_CABLE, KeywordId.GROUND_ROD_TOP],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.GROUND_CABLE),
                Condition(type=ConditionType.STATE_IS, target="ground_rod_set", value=True),
                Condition(type=ConditionType.STATE_IS, target="grounding_done", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "접지 케이블의 나머지 끝을 말뚝 머리에 감아 단단히 묶는다.\n"
                        "이제 번개가 기둥을 타고 내려오면 에너지 대부분은 이 케이블을 따라 젖은 흙으로 빠져나갈 것이다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "grounding_done", "value": True},
                ),
            ],
        ),
        # --- 튜닝 코일을 패널에 연결: TUNING_COIL + TUNING_PANEL ---
        Combination(
            targets=[KeywordId.TUNING_COIL, KeywordId.TUNING_PANEL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.TUNING_COIL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "튜닝 코일을 휴대용 모듈의 패널 단자에 연결한다.\n"
                        "다이얼을 돌리면 코일의 감은 수가 바뀌어 공진 주파수가 이동하도록 설계된 듯하다."
                    ),
                ),
            ],
        ),
        # --- 튜닝 패널 비밀번호 퍼즐 ---
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.TUNING_PANEL, "1"],
            conditions=[],
            actions=[
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "coil_state", "value": 0},
                ),
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "튜닝 패널을 1단으로 맞추고 테스트 모듈을 켠다.\n"
                        "귀를 찢는 듯한 고주파 잡음만 가득하다. 인간의 목소리는 전혀 들리지 않는다."
                    ),
                ),
            ],
        ),
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.TUNING_PANEL, "2"],
            conditions=[],
            actions=[
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "coil_state", "value": 1},
                ),
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "튜닝 패널을 2단으로 맞추고 테스트 모듈을 다시 켠다.\n"
                        "처음에는 바람 소리와 비슷한 잡음만 들리다가, 곧 잡음 사이로 또렷한 인간의 목소리가 섞여 들려온다.\n"
                        '"...여기는 구조 위성 중계기... 수신 상태 양호..."\n'
                        "구조 신호가 이 주파수 대역에 있는 것이 분명하다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "coil_tuned", "value": True},
                ),
            ],
        ),
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.TUNING_PANEL, "3"],
            conditions=[],
            actions=[
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "coil_state", "value": 2},
                ),
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "튜닝 패널을 3단으로 맞추자, 낮게 윙— 하는 저주파 소리와 전파 간섭만 가득하다.\n"
                        "유용한 통신은 전혀 잡히지 않는다."
                    ),
                ),
            ],
        ),
        # --- 번개 이벤트: STORM_SKY + ANTENNA_MAST ---
        Combination(
            targets=[KeywordId.STORM_SKY, KeywordId.ANTENNA_MAST],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                Condition(type=ConditionType.STATE_IS, target="mast_fixed", value=True),
                Condition(type=ConditionType.STATE_IS, target="grounding_done", value=True),
                Condition(type=ConditionType.STATE_IS, target="coil_tuned", value=True),
                Condition(type=ConditionType.STATE_IS, target="lightning_event_done", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "하늘이 잠시 새하얗게 밝아지더니, 귀가 먹먹해질 정도의 천둥과 함께 번개가 안테나 꼭대기를 강타한다.\n"
                        "섬광과 함께 에너지가 기둥과 접지 케이블을 타고 땅으로 빠르게 흘러내린다.\n\n"
                        "휴대용 테스트 모듈에서는 과부하 방지 회로가 작동하며 살짝 전압이 솟구쳤다가 곧 안정된다.\n"
                        "튜닝된 코일과 수력 발전 모듈은 번개 세례를 견뎌냈고, 앞으로 MK-II 본체에 연결할 준비가 된 것 같다.\n"
                        '당신은 노트를 꺼내 오늘의 결론을 적는다. "수력 + 번개 = 교수님이 좋아할 논문감".'
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "lightning_event_done", "value": True},
                ),
            ],
        ),
        # 접지 없이 시도할 경우 경고용
        Combination(
            targets=[KeywordId.STORM_SKY, KeywordId.ANTENNA_MAST],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_assembled", value=True),
                Condition(type=ConditionType.STATE_IS, target="mast_fixed", value=True),
                Condition(type=ConditionType.STATE_IS, target="grounding_done", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "먹구름 사이로 번개가 멀리 떨어지는 것을 바라본다.\n"
                        "이 상태에서 기둥이 직접 맞기라도 하면, 에너지가 어디로 흐를지 전혀 예측할 수 없다.\n"
                        "MK-II를 살리고 싶다면, 먼저 **접지**를 완성해야 한다."
                    ),
                )
            ],
        ),
        # 석영 조각을 테스트 모듈에 추가로 연결 (선택 퍼즐, 보너스 대사용)
        Combination(
            targets=[KeywordId.MK_II_SUMMIT, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "테스트 모듈의 발진기 소켓을 열고 석영 조각을 조심스럽게 끼워 넣는다.\n"
                        "주파수 드리프트가 눈에 띄게 줄어들고, 튜닝 패널을 돌릴 때마다 수신 대역이 또렷하게 움직인다.\n"
                        "실험이 끝나면 이 설정 그대로 MK-II 본체에 옮겨 달 수 있을 것이다."
                    ),
                ),
            ],
        ),
    ],
)
