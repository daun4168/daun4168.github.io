from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE7_DATA = SceneData(
    id=SceneID.CH1_SCENE7,
    name="지하 호수 (폭포 동굴)",
    initial_text=(
        "석회 동굴의 바닥 경사로를 따라 조심스레 내려가자, 공기가 점점 더 축축해진다.\n"
        "발밑 바위가 미끄러워질 즈음, 앞에서부터 거대한 물소리가 벽을 타고 울려 온다.\n\n"
        "좁은 틈을 빠져나오자 갑자기 시야가 열린다. 머리 위 동굴 천장에서 흰 물줄기가 폭포처럼 쏟아져 내려 "
        "넓은 지하 호수를 만들고 있다. 물안개가 허공에 뜨듯이 떠 있고, 바닥은 매끈한 바위와 젖은 자갈로 덮여 있다.\n\n"
        "호수 가장자리에는 물살에 깎인 둥근 바위 고리가 하나 놓여 있고, 한쪽 벽면에는 마치 쇳가루를 뿌린 듯 "
        "스패너가 살짝 달라붙는 검은 바위 덩어리가 박혀 있다.\n"
        "당신은 본능적으로 생각한다. '여기서 물을 전기로 바꿔 먹을 수만 있다면, MK-II에게 큰 도움이 될 텐데...'"
    ),
    initial_state={
        "magnetite_chipped": False,  # 자철석 조각을 떼어냈는지
        "rotor_built": False,  # 코코넛 수차 로터 제작 여부
        "dynamo_core_built": False,  # 자철석 + 구리선으로 코어 제작 여부
        "dynamo_module_built": False,  # 수력 발전 모듈 완성 여부
        "dynamo_tested": False,  # 폭포에서 한 번 돌려봤는지
        "back_path_inspected": False,  # 위로 되돌아가는 경로 설명 여부
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # --- ALIAS ---
        KeywordId.UNDERGROUND_LAKE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,  # ⬅️ 원래 DISCOVERED → HIDDEN
            description=None,
            interactions=[],
        ),
        KeywordId.WATERFALL_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,  # ⬅️ 마찬가지로 숨김
            description=None,
            interactions=[],
        ),
        # --- 포탈: 석회 동굴로 돌아가는 길 (이것만 초기에 DISCOVERED 유지) ---
        KeywordId.LAKE_BACK_TUNNEL: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,  # ⬅️ 요청대로 돌아가는 길만 DISCOVERED 유지
            description=None,
            interactions=[
                # 첫 조사: 설명
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="back_path_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "뒤를 돌아보면 방금 내려온 경사로가 어둠 속으로 이어져 있다.\n"
                                "손과 발을 모두 써서 기어 올라가야 할 만큼 가파르지만, "
                                "조심해서 가면 다시 석회 동굴로 돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "back_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 이후: 이동 여부 확인
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="back_path_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "경사로를 따라 석회 동굴로 되돌아가시겠습니까?\n올라가는 동안 체력이 2 소모됩니다.",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 젖은 바위를 짚으며 숨을 고르고, 조심스럽게 석회 동굴 쪽으로 기어 올라간다.",
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
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 이 지하 호수에서 더 해볼 수 있는 일이 남아 있는 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # --- 지형/환경 ---
        KeywordId.UNDERGROUND_LAKE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ 처음에는 안 보이게
            description=(
                "동굴 천장에서 떨어지는 폭포수가 동굴 바닥을 파고들어 넓은 호수를 만들고 있다.\n"
                "호수 한가운데는 깊이를 가늠하기 어렵고, 물 빛깔은 푸르스름하게 어둡다.\n"
                "호수 주변에는 물살에 깎인 자갈과 둥근 바위들이 어지럽게 흩어져 있다."
            ),
        ),
        KeywordId.WATERFALL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ HIDDEN으로 변경
            description=(
                "동굴 천장 갈라진 틈에서 흰 물줄기가 쏟아져 내린다.\n"
                "폭포 아래쪽에는 물살이 세게 부딪히는 자리와, 옆으로 튀어나와 물이 측면으로 흘러내리는 자리, "
                "그리고 조금 더 아래쪽에 물살이 한 번 꺾여 적당한 속도로 흐르는 지점이 있다.\n"
                "이쯤 되면, 공대생의 뇌가 자동으로 떠올린다. '이건... 수차 자리다.'"
            ),
        ),
        KeywordId.LAKE_SHORE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ HIDDEN으로 변경
            description=(
                "호수 가장자리는 간신히 사람이 설 수 있을 정도의 좁은 자갈 턱으로 이어져 있다.\n"
                "발밑 자갈은 젖어서 미끄럽지만, 조심해서 움직이면 수면 가까이 손을 뻗을 수 있다."
            ),
        ),
        KeywordId.STONE_RING: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ HIDDEN으로 변경
            description=(
                "물살에 깎여 테두리가 둥글게 패인 바위 고리가 바닥에 놓여 있다.\n"
                "가운데 구멍은 둥글고 매끈해서, 축을 꽂으면 베어링처럼 쓸 수 있을 것 같다."
            ),
        ),
        KeywordId.MAGNETIC_ROCK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ HIDDEN으로 변경
            description=(
                "동굴 벽 한쪽에 검은 바위 덩어리가 튀어나와 있다.\n"
                "가까이 다가가 스패너를 대 보니, 금속이 살짝 끌리는 느낌이 든다.\n"
                "표면에 달라붙은 작은 쇳가루도 보인다. 거의 확실히 자철석이다."
            ),
        ),
        KeywordId.RESIN_POOL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ HIDDEN으로 변경
            description=(
                "벽 틈 사이에서 흘러나온 끈적한 수지가 작은 웅덩이를 이루고 있다.\n"
                "공기 중의 먼지와 모래가 붙어 표면은 살짝 지저분하지만, 안쪽은 여전히 투명한 수지 덩어리다.\n"
                "코일을 방수 처리하는 데 안성맞춤일 것 같다."
            ),
        ),
        # --- 장비/인벤토리 관련 ---
        KeywordId.TOOL_POUCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # ⬅️ 처음엔 숨겨 두고, 유저가 입력해서 발견하게
            description=("허리춤에 찬 작은 공구 파우치다. MK-II 정비용으로 챙겨온 자잘한 부품들이 들어 있다."),
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="dynamo_core_built",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "파우치를 열어 보니, 자잘한 나사들과 절연 테이프 몇 조각, "
                                "그리고 꽤 길이가 되는 얇은 구리선 뭉치가 하나 들어 있다.\n"
                                "기본적인 발전 코일 정도는 감을 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.COPPER_WIRE,
                                "description": "MK-II 정비 키트에서 꺼낸 얇은 구리선 뭉치다. 코일을 감기에 충분한 길이다.",
                            },
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="dynamo_core_built",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="공구 파우치에는 이제 눈에 띄는 부품이 남아 있지 않다.",
                        )
                    ],
                ),
            ],
        ),
        # --- Scene7에서 새로 얻는 아이템들 ---
        KeywordId.MAGNETITE_CHUNK: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="검은 바위에서 떼어낸 자철석 조각이다. 철 성분이 많아 자성이 강하다.",
        ),
        KeywordId.COPPER_WIRE: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="MK-II 정비용으로 챙겨온 얇은 구리선 뭉치다.",
        ),
        KeywordId.MAKESHIFT_ROTOR: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="코코넛 껍질과 덩굴로 만든 임시 수차 로터다. 물살을 받으면 빙글빙글 잘 돌아갈 것 같다.",
        ),
        KeywordId.DYNAMO_CORE: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="자철석 조각에 구리선을 여러 번 감아 만든 작은 발전 코어다.",
        ),
        KeywordId.HYDRO_DYNAMO_MODULE: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="폭포수만 있어도 돌아가는 소형 수력 발전 모듈이다. MK-II를 위한 임시 발전소로 쓸 수 있다.",
        ),
        KeywordId.RESIN_GLOB: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="동굴 벽 틈에서 긁어낸 끈적한 수지 덩어리다. 굳으면 훌륭한 방수 코팅이 된다.",
        ),
    },
    combinations=[
        # --- 자철석 조각 얻기: MAGNETIC_ROCK + SPANNER ---
        Combination(
            targets=[KeywordId.MAGNETIC_ROCK, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="magnetite_chipped", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너로 검은 바위 덩어리를 몇 번 두드려 보니, 가장자리가 조금씩 부서져 나간다.\n"
                        "그중 자성이 가장 강한 조각 몇 개를 골라 주머니에 챙겨 넣는다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MAGNETITE_CHUNK,
                        "description": "검은 자철석 조각이다. 가까이 대면 금속이 살짝 끌리는 느낌이 난다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "magnetite_chipped", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MAGNETIC_ROCK, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="magnetite_chipped", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="더 이상 쓸 만한 자철석 조각은 잘 떨어지지 않는다.",
                )
            ],
        ),
        # --- 코코넛 껍질 가공: COCONUT + SPANNER ---
        Combination(
            targets=[KeywordId.COCONUT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="rotor_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛을 바위 위에 고정하고 스패너의 모서리로 힘껏 내려친다.\n"
                        "몇 번의 시도 끝에 코코넛이 비교적 깔끔하게 반으로 갈라진다. "
                        "단단한 껍질은 물살을 받는 날개로 쓰기 딱 좋아 보인다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.COCONUT,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "반으로 갈라진 코코넛 껍질이다. 수차 날개로 개조할 수 있을 것 같다.",
                    },
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.COCONUT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="rotor_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이미 코코넛 껍질을 가공해 수차에 쓸 준비를 마쳤다.",
                )
            ],
        ),
        # --- 코코넛 껍질 + 덩굴 → 임시 로터 ---
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.VINES],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINES),
                Condition(type=ConditionType.STATE_IS, target="rotor_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛 껍질을 십자 모양으로 엇갈려 덩굴로 단단히 묶는다.\n"
                        "중앙에 막대를 꽂을 수 있는 작은 구멍을 뚫어 두자, 제법 그럴듯한 수차 로터가 완성된다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.COCONUT_SHELL,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MAKESHIFT_ROTOR,
                        "description": "코코넛 껍질과 덩굴로 만든 임시 수차 로터다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "rotor_built", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.VINES],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="rotor_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이미 코코넛 껍질과 덩굴로 수차 로터를 만들어 두었다.",
                )
            ],
        ),
        # --- 자철석 + 구리선 → 발전 코어 ---
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COPPER_WIRE),
                Condition(type=ConditionType.STATE_IS, target="dynamo_core_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석 조각에 구리선을 빽빽하게 감아 나간다.\n"
                        "몇 겹을 감고 난 뒤, 양 끝 전선을 조금 남겨 단자처럼 꺾어 두자, "
                        "어디서 많이 본 모양의 작은 발전 코어가 손에 들어온다.\n"
                        '"교과서에서 보던 바로 그 그림이네..."'
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.COPPER_WIRE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.DYNAMO_CORE,
                        "description": "자철석에 구리선을 감아 만든 소형 발전 코어다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "dynamo_core_built", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="dynamo_core_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이미 자철석 코어에 구리선을 감아 두었다.",
                )
            ],
        ),
        # --- 발전 코어 + 수차 로터 → 수력 발전 모듈 ---
        Combination(
            targets=[KeywordId.DYNAMO_CORE, KeywordId.MAKESHIFT_ROTOR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DYNAMO_CORE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAKESHIFT_ROTOR),
                Condition(type=ConditionType.STATE_IS, target="dynamo_module_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석 코어를 수차 로터 중앙에 맞춰 끼우고, 덩굴과 남은 끈으로 단단히 고정한다.\n"
                        "구리선 단자는 바깥쪽으로 살짝 빼서 나중에 배선을 연결할 수 있게 해 둔다.\n"
                        "이제 물살만 있으면 전기를 뽑아낼 수 있는 **소형 수력 발전 모듈**이 완성됐다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.DYNAMO_CORE,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.MAKESHIFT_ROTOR,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.HYDRO_DYNAMO_MODULE,
                        "description": "폭포수만 있으면 전기를 만들어내는 소형 수력 발전 모듈이다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "dynamo_module_built", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.DYNAMO_CORE, KeywordId.MAKESHIFT_ROTOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="dynamo_module_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이미 수력 발전 모듈을 조립해 두었다.",
                )
            ],
        ),
        # --- 수지로 방수 코팅: 모듈 + RESIN_POOL ---
        Combination(
            targets=[KeywordId.HYDRO_DYNAMO_MODULE, KeywordId.RESIN_POOL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HYDRO_DYNAMO_MODULE),
                Condition(type=ConditionType.STATE_IS, target="dynamo_tested", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "수력 모듈을 조심히 수지 웅덩이에 담갔다 빼내어, 코일과 금속 부분에 얇게 코팅을 입힌다.\n"
                        "겉면을 한 번 훑자 끈적한 막이 형성되고, 안쪽은 서서히 단단해질 기세다.\n"
                        "이 정도면 물 튀김 정도는 충분히 버틸 수 있을 것이다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.RESIN_GLOB,
                        "description": "남은 수지 조각이다. 나중에 다른 부품을 코팅하는 데도 쓸 수 있을 것 같다.",
                    },
                ),
            ],
        ),
        # --- 폭포에 걸어 테스트: WATERFALL + HYDRO_DYNAMO_MODULE ---
        Combination(
            targets=[KeywordId.WATERFALL, KeywordId.HYDRO_DYNAMO_MODULE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HYDRO_DYNAMO_MODULE),
                Condition(type=ConditionType.STATE_IS, target="dynamo_module_built", value=True),
                Condition(type=ConditionType.STATE_IS, target="dynamo_tested", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "수력 모듈을 폭포 옆, 물살이 적당히 꺾여 내려오는 지점에 걸어 본다.\n"
                        "코코넛 수차가 물살을 받아 돌기 시작하고, 곧 손에 쥔 두 가닥 전선이 따끔하게 저려 온다.\n"
                        "멀리 베이스캠프의 MK-II가 떠오른다. '좋아, 이 녀석만 있으면 한 번 더 살아볼 수 있겠다.'"
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "dynamo_tested", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="**[소형 수력 발전 모듈]**을 확보했습니다. 나중에 MK-II 수리에 활용할 수 있을 것 같습니다.",
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.WATERFALL, KeywordId.HYDRO_DYNAMO_MODULE],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="dynamo_tested", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="수력 모듈은 이미 충분히 테스트를 마쳤다. 이제는 베이스캠프로 가져가면 된다.",
                )
            ],
        ),
    ],
)
