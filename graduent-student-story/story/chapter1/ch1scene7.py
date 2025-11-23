from const import (
    ActionType,
    CombinationType,
    ConditionType,
    KeywordId,
    KeywordState,
    KeywordType,
    SceneID,
)
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE7_DATA = SceneData(
    id=SceneID.CH1_SCENE7,
    name="지하 호수 (폭포 동굴)",
    initial_text=(
        "석회 동굴의 바닥 경사로를 따라 조심스레 내려가자, 공기가 점점 더 축축해진다.\n"
        "발밑 바위가 미끄러워질 즈음, 앞에서부터 거대한 물소리가 벽을 타고 울려 온다.\n\n"
        "좁은 틈을 빠져나오자 갑자기 시야가 열린다. 머리 위 동굴 천장에서 흰 물줄기가 폭포처럼 쏟아져 내려 "
        "넓은 지하 호수를 만들고 있다. 물안개가 허공에 떠 있고, 바닥은 매끈한 바위와 젖은 자갈들로 덮여 있다.\n\n"
        "호숫가에는 물살에 깎인 둥근 바위 고리가 하나 놓여 있고, 한쪽 벽면에는 마치 쇳가루를 뿌린 듯 "
        "스패너가 살짝 달라붙는 검은 바위 덩어리가 박혀 있다.\n"
        "당신은 본능적으로 생각한다. '여기서 물을 전기로 바꿔 먹을 수만 있다면, MK-II에게 큰 도움이 될 텐데...'"
    ),
    initial_state={
        "magnetite_chipped": False,
        "rotor_built": False,
        "dynamo_core_built": False,
        "generator_installed": False,
        "generator_unlocked": False,
        "battery_charged": False,
        "back_path_inspected": False,
        # ⬇️ 새로 추가
        "stone_ring_collected": False,
        "wooden_shaft_collected": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # --- ALIAS ---
        KeywordId.UNDERGROUND_LAKE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[],
        ),
        KeywordId.WATERFALL_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[],
        ),
        # --- 돌아가는 길 포탈만 DISCOVERED ---
        KeywordId.LAKE_BACK_TUNNEL: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
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
            state=KeywordState.HIDDEN,
            description=(
                "동굴 천장에서 떨어지는 폭포수가 바닥을 파고들어 넓은 호수를 만들고 있다.\n"
                "호수 한가운데는 깊이를 가늠하기 어렵고, 물빛은 푸른빛이 도는 검은색에 가깝다."
            ),
        ),
        KeywordId.WATERFALL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "동굴 천장 갈라진 틈에서 흰 물줄기가 쏟아져 내린다.\n"
                "폭포 아래쪽에는 물살이 세게 부딪히는 자리와, 옆으로 튀어나와 물이 측면으로 흘러내리는 자리, "
                "조금 더 아래에는 물살이 한 번 꺾여 적당한 속도로 흘러가는 지점이 보인다."
            ),
        ),
        KeywordId.LAKE_SHORE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "호수 가장자리는 간신히 사람이 설 수 있을 정도의 좁은 자갈 턱으로 이어져 있다.\n"
                "발밑 자갈은 젖어서 미끄럽지만, 조심해서 움직이면 수면 가까이 손을 뻗을 수 있다."
            ),
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="stone_ring_collected",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="wooden_shaft_collected",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "호숫가를 자세히 살펴보니, 물살에 깎여 매끈한 둥근 바위 고리와 "
                                "물에 떠내려온 긴 나무 막대 하나가 눈에 띈다.\n"
                                "둘 다 수차를 만들 때 써먹기 좋아 보인다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_RING,
                                "description": "물살에 깎여 테두리가 둥글게 패인 바위 고리다. 축을 끼워 베어링처럼 쓸 수 있다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.WOODEN_SHAFT,
                                "description": "적당한 길이와 굵기를 가진 나무 막대다. 수차의 회전축으로 쓰기 좋다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "stone_ring_collected", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "wooden_shaft_collected", "value": True},
                        ),
                    ],
                ),
                # 이미 둘 다 줍고 난 뒤 다시 조사
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="stone_ring_collected",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="wooden_shaft_collected",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="호숫가에는 잘게 부서진 자갈과 젖은 돌들만 남아 있다. 쓸 만한 건 이미 챙긴 것 같다.",
                        )
                    ],
                ),
            ],
        ),
        KeywordId.MAGNETIC_ROCK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "동굴 벽 한쪽에 검은 바위 덩어리가 튀어나와 있다.\n"
                "스패너를 가까이 가져가자 금속이 살짝 끌리는 느낌이 든다. 표면에 쇳가루도 붙어 있는 걸 보니, "
                "제법 강한 자성을 띠는 자철석인 듯하다."
            ),
        ),
        # --- 설치형 수력 발전기 (처음에는 비활성) ---
        KeywordId.HYDRO_GENERATOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # 모듈 설치 전에는 등장하지 않음
            description="폭포 옆 바위 고리에 수차 모듈을 걸어 만든 임시 수력 발전기다.",
            interactions=[
                # 설치만 되어 있고 아직 잠금(비밀번호) 안 풀린 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="generator_installed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="generator_unlocked",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "폭포 옆 바위 고리에 수차 모듈을 단단히 고정해 두었다.\n"
                                "물살을 받아 코코넛 날개가 일정한 속도로 돌아가고, 연결된 자철석 코어 주변에 미세한 전류가 흐르는 것이 느껴진다.\n"
                                "발전기 옆 조그마한 금속 패널에는 이렇게 적혀 있다.\n"
                                '"원 둘레 / 지름 ≈ 3.14  → 소수점 없이 세 자리 입력"\n'
                                "아무래도 시동을 걸기 전에 비밀번호를 먼저 입력해야 하는 모양이다."
                            ),
                        )
                    ],
                ),
                # 잠금 해제 후 단순 관찰
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="generator_installed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="generator_unlocked",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "폭포 옆 수력 발전기가 일정한 속도로 돌아가고 있다.\n"
                                "코일에서 나온 전기는 외부 단자에 안정적으로 출력되는 중이다."
                            ),
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # --- 1) 자철석 + 소방 도끼 → 자철석 조각 ---
        Combination(
            targets=[KeywordId.MAGNETIC_ROCK, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="magnetite_chipped", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼로 자성을 띤 검은 바위 가장자리를 조심스럽게 내리친다.\n"
                        "몇 번의 타격 끝에 손바닥만 한 자철석 조각 하나가 바닥으로 떨어진다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MAGNETITE_CHUNK,
                        "description": "자철석 덩어리에서 떼어낸 조각이다. 발전기의 자석 코어로 쓰기 좋다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "magnetite_chipped", "value": True},
                ),
            ],
        ),
        # 임시 수차 로터 + 폭포 (축 없이 사용 시 부정 피드백)
        Combination(
            targets=[KeywordId.MAKESHIFT_ROTOR, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAKESHIFT_ROTOR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "임시 수차 로터를 그냥 물살에 던져 보았지만, 축이 없어 이리저리 휩쓸려 다니기만 한다.\n"
                        "먼저 튼튼한 축을 끼우는 편이 좋겠다."
                    ),
                )
            ],
        ),
        # 이미 자철석 조각 획득 후
        Combination(
            targets=[KeywordId.MAGNETIC_ROCK, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="magnetite_chipped", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="더 쳐 봐야 잘게 부서질 뿐, 쓸 만한 자철석 조각은 더 이상 나오지 않을 것 같다.",
                )
            ],
        ),
        # --- 6) 수력 발전 모듈 + 폭포 → 수력 발전기 설치(오브젝트 활성화) ---
        Combination(
            targets=[KeywordId.HYDRO_DYNAMO_MODULE, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HYDRO_DYNAMO_MODULE),
                Condition(type=ConditionType.STATE_IS, target="generator_installed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "수력 발전 모듈을 폭포 옆, 물살이 적당히 꺾여 내려오는 지점에 설치한다.\n"
                        "코코넛 수차가 물을 받아 돌기 시작하고, 자철석 코어 주변에서는 미묘한 전류가 흐르는 느낌이 전해진다.\n"
                        "옆의 바위에 임시로 단자와 스위치를 고정해 두자, 그럴듯한 수력 발전기가 완성된다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.HYDRO_DYNAMO_MODULE),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "generator_installed", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.HYDRO_GENERATOR,
                        "state": KeywordState.DISCOVERED,
                    },
                ),
            ],
        ),
        # --- 7) 수력 발전기 비밀번호 퍼즐: HYDRO_GENERATOR + "314" ---
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.HYDRO_GENERATOR, "314"],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="generator_installed", value=True),
                Condition(type=ConditionType.STATE_IS, target="generator_unlocked", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "발전기 옆 금속 패널에 3-1-4를 차례대로 눌러 본다.\n"
                        "잠시 후 작게 딸깍 하는 소리와 함께 내부에서 계기들이 정렬되는 느낌이 전해진다.\n"
                        "수차의 회전 속도가 안정되고, 출력 단자에 일정한 전압이 걸린다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "generator_unlocked", "value": True},
                ),
            ],
        ),
        # 잠금이 안 풀린 상태에서 배터리 연결을 시도할 때 (힌트)
        Combination(
            targets=[KeywordId.HYDRO_GENERATOR, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
                Condition(type=ConditionType.STATE_IS, target="generator_installed", value=True),
                Condition(type=ConditionType.STATE_IS, target="generator_unlocked", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "산업용 배터리를 단자에 연결해 보았지만, 발전기 측 안전장치가 여전히 잠겨 있어 전류가 흐르지 않는다.\n"
                        "옆 패널의 비밀번호를 먼저 해제해야 할 것 같다."
                    ),
                )
            ],
        ),
        # --- 8) 수력 발전기 + 산업용 배터리 → 충전된 배터리 ---
        Combination(
            targets=[KeywordId.HYDRO_GENERATOR, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
                Condition(type=ConditionType.STATE_IS, target="generator_installed", value=True),
                Condition(type=ConditionType.STATE_IS, target="generator_unlocked", value=True),
                Condition(type=ConditionType.STATE_IS, target="battery_charged", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "산업용 배터리를 발전기 출력 단자에 연결한다.\n"
                        "폭포수에 맞춰 수차가 일정한 속도로 돌면서, 배터리 측 표시등이 천천히 깜빡이기 시작한다.\n"
                        "잠시 후, 깜빡이던 불빛이 안정된 색으로 바뀐다. 충분히 충전된 듯하다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.HEAVY_BATTERY),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.CHARGED_HEAVY_BATTERY,
                        "description": "수력 발전기로 완전히 충전된 산업용 배터리다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "battery_charged", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="충전된 산업용 배터리를 획득했습니다. 이제 MK-II에게 세컨드 찬스를 줄 수 있을 것 같습니다.",
                ),
            ],
        ),
        # 이미 배터리를 충전한 뒤 또 연결하려 할 때
        Combination(
            targets=[KeywordId.HYDRO_GENERATOR, KeywordId.CHARGED_HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
                Condition(type=ConditionType.STATE_IS, target="battery_charged", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="배터리는 이미 충분히 충전되어 있다. 더 돌리면 발전기 쪽이 먼저 탈지도 모른다.",
                )
            ],
        ),
        # ------------------------------------------------------------------
        # [추가됨] 폭포(WATERFALL)와의 부정 피드백 모음
        # ------------------------------------------------------------------
        # [부정] 자철석 조각 + 폭포
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석 조각을 흐르는 물에 씻어 보았다. 반짝거려서 예쁘긴 하지만, 젖은 자석이 전기를 뱉어내진 않는다.\n"
                        "전자기 유도를 일으키려면 코일과 함께 '회전'시켜야 한다."
                    ),
                )
            ],
        ),
        # [부정] 구리선 + 폭포
        Combination(
            targets=[KeywordId.COPPER_WIRE, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COPPER_WIRE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "구리선을 폭포수에 담가 본다. 시원한 물줄기가 전선을 타고 흐르지만, 전자가 흐르는 것은 아니다.\n"
                        "이걸 발전기로 만들려면 자석 주위에서 끊임없이 움직이게 해 줄 장치가 필요하다."
                    ),
                )
            ],
        ),
        # [부정] 코코넛 껍질 + 폭포
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛 껍질로 떨어지는 폭포수를 받아 마셨다. 갈증은 해소되지만 탈출에는 진전이 없다.\n"
                        "수력 발전을 하려면 이 껍질들을 엮어서 물살을 받아낼 '날개'를 만들어야 한다."
                    ),
                )
            ],
        ),
        Combination(
            targets=[KeywordId.SHAFTED_ROTOR, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SHAFTED_ROTOR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("축 달린 수차를 폭포 옆 바위에 기대어 보지만, 축이 흔들려 금방 한쪽으로 기울어 버린다.\n"),
                )
            ],
        ),
        # [부정] 발전 코어 + 폭포
        Combination(
            targets=[KeywordId.DYNAMO_CORE, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DYNAMO_CORE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "발전 코어를 손에 쥐고 물살 속에 넣어 보았다. 묵직한 수압이 느껴지지만 손목만 아플 뿐이다.\n"
                    ),
                )
            ],
        ),
        # [부정] 나무 축 + 폭포
        Combination(
            targets=[KeywordId.WOODEN_SHAFT, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WOODEN_SHAFT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "나무 축을 흐르는 물에 꽂아 보았다. 유속을 측정하는 척해 보지만, 막대기 하나로는 아무런 동력도 얻을 수 없다.\n"
                    ),
                )
            ],
        ),
        # [부정] 고리에 끼운 수차 + 폭포 (발전 코어 누락)
        Combination(
            targets=[KeywordId.MOUNTED_ROTOR, KeywordId.WATERFALL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MOUNTED_ROTOR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "고리에 끼운 수차를 폭포 옆에 설치해 보았다. 베어링 덕분에 수차는 신나게 돌아가지만, 전기는 1볼트도 나오지 않는다.\n"
                        "회전 에너지를 전기 에너지로 바꿔 주어야 한다."
                    ),
                )
            ],
        ),
    ],
)
