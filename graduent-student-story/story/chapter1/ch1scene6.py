from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE6_DATA = SceneData(
    id=SceneID.CH1_SCENE6,
    name="석회 동굴 (수정 동굴)",
    initial_text=(
        "늪지대를 벗어나 바위 경사면을 따라 올라오자, 공기가 서늘하게 식어 간다.\n"
        "바위 틈 사이로 몸을 비집고 들어가자 곧 머리 위로 석회암 종유석이 빽빽이 매달린 동굴 홀이 펼쳐진다.\n\n"
        "입구 쪽에서 들어오는 희미한 빛이 바닥의 짧은 돌, 중간 돌, 긴 돌 세 개를 스치고 지나가며, 동굴 벽면에 어딘가 시계처럼 보이는 원형 그림자를 만든다.\n"
        "각 돌기둥의 그림자는 서로 다른 방향을 가리키고 있어, 마치 멈춰버린 시계 바늘처럼 보인다.\n\n"
        "홀 한쪽 벽은 하얀 석회층으로 뒤덮여 있는데, 가까이 다가가면 크고 작은 점무늬가 정갈하게 배열된 패널이 눈에 띈다.\n"
        "반대편에는 바닥으로 내려가는 낮은 경사로와, 위쪽 협곡으로 이어지는 듯한 좁은 바람길이 어둠 속으로 이어져 있다."
    ),
    initial_state={
        "shadow_door_unlocked": False,
        "binary_panel_step": 0,
        "binary_panel_solved": False,
        "cliff_path_opened": False,
        "lake_path_opened": False,
        "spring_discovered": False,
        "spring_collected": False,
        "quartz_discovered": False,
        "quartz_collected": False,
        "swamp_path_inspected": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # 늪지대로 되돌아가는 길
        KeywordId.SWAMP_PATH_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SWAMP_PATH),
        KeywordId.SWAMP_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 처음 확인
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="swamp_path_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "들어왔던 바위 틈을 다시 돌아보면, 아래쪽으로 이어지는 경사로 끝에 "
                                "독특한 냄새가 풍기는 늪지대의 어둠이 희미하게 보인다.\n"
                                "조심해서 내려가면 다시 맹독 늪지대로 되돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한 번 늪지대를 입력하면 늪으로 되돌아갈지 물어봅니다. 내려갔다가 다시 올라오면 체력이 꽤 소모될 것 같습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "swamp_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 이후에는 확인 프롬프트
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="swamp_path_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "경사로를 따라 다시 늪지대로 내려가시겠습니까?\n"
                                    "미끄러운 경사로를 오르내리느라 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 깊은 숨을 한 번 내쉰 뒤, 조심스럽게 경사로를 따라 맹독 늪지대로 내려가기 시작한다.",
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE5,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 동굴 안에서 더 살펴볼 곳이 남아 있는 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),

        # --- [그림자 시계 퍼즐 관련 오브젝트] ---
        # 중앙 동굴 홀 설명
        KeywordId.CAVE_HALL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "동굴 중앙은 둥근 홀처럼 트여 있다. 바닥에서 솟아오른 키가 서로 다른 세 개의 돌기둥(짧은 돌, 중간 돌, 긴 돌)이 빛을 받아 "
                "벽면에 서로 다른 방향의 그림자를 드리우고 있다.\n"
                "벽 한쪽에는 시계판처럼 보이는 원형 석회 문양이 있고, 그 중앙에는 바닥으로 내려가는 문처럼 보이는 경계선이 보인다."
            ),
        ),
        # 짧은 돌
        KeywordId.SHORT_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "가장 키가 낮은 돌기둥이다. 입구 쪽에서 들어오는 빛을 받으면, "
                "그림자가 동굴 벽면 시계판의 오른쪽 부분으로 짧게 드리워진다.\n"
                "그림자가 닿는 자리에는 희미하게 '06'이라는 숫자가 새겨져 있는 것이 보인다."
            ),
        ),
        # 중간 돌
        KeywordId.MID_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "중간 높이의 돌기둥이다. 그림자를 자세히 따라가 보니, 시계판의 왼쪽 부분에 걸쳐 멈춰 있다.\n"
                "그 지점의 돌기 표면에는 '45'라는 두 자리 숫자가 희미하게 남아 있다."
            ),
        ),
        # 긴 돌
        KeywordId.LONG_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "가장 키가 큰 돌기둥이다. 그림자는 바닥을 따라 길게 뻗어 내려가더니, "
                "시계판 아래쪽 가장 낮은 위치에 걸쳐 있다.\n"
                "그 부분에는 '30'이라는 숫자가 다른 곳보다 조금 더 깊게 새겨져 있다."
            ),
        ),
        # 시계 문양 / 석회문
        KeywordId.TIME_DOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 아직 잠겨 있을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="shadow_door_unlocked",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "거대한 원형 석회 문양이 벽면을 거의 가득 메우고 있다. 바깥쪽은 12등분된 시계처럼, "
                                "안쪽에는 더 촘촘한 눈금과 숫자들이 원형으로 줄지어 있다.\n"
                                "중앙 아래쪽에는 아주 작은 글씨로 '짧은 돌은 시, 중간 돌은 분, 긴 돌은 초. "
                                "세 수를 잇고 문을 두드려라.' 라고 적혀 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="석회문 : [6자리 시간 코드] 형식으로 숫자를 입력할 수 있을 것 같다.",
                        ),
                    ],
                ),
                # 이미 열렸을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="shadow_door_unlocked",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="석회문은 이미 옆으로 밀려 열린 상태다. 틈 사이로 차가운 공기가 계속 새어 나온다.",
                        )
                    ],
                ),
            ],
        ),

        # 석회문 안쪽으로 이어지는 절벽 통로(위쪽)
        KeywordId.CLIFF_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 아직 길이 완전히 열리지 않았을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="cliff_path_opened",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "시계 모양 석회문 가까이에서 위쪽 협곡 틈을 올려다보면, "
                                "낡은 석회 조각들이 아직 길을 반쯤 막고 있다.\n"
                                "문을 완전히 열어야만 위쪽 절벽으로 이어지는 바람길이 안전해질 것 같다."
                            ),
                        )
                    ],
                ),
                # 길이 열린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="cliff_path_opened",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "위쪽 협곡을 따라 가파른 절벽으로 올라가시겠습니까?\n"
                                    "바위를 붙잡고 오르느라 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 시계문 옆 바위를 짚고 좁은 협곡 틈을 따라 위쪽 절벽으로 오르기 시작한다.",
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE8,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 석회 동굴 안에서 더 살펴볼 곳이 남아 있는 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),

        # 석회문 안쪽 아래로 이어지는 지하 호수 통로(아래쪽)
        KeywordId.UNDERGROUND_LAKE_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 아직 길이 열리지 않았을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="lake_path_opened",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "석회문 아래쪽 틈 사이로는 어딘가에서 울려오는 물소리만 희미하게 들린다.\n"
                                "아직은 석회층이 두껍게 남아 있어, 몸을 낮추고 지나갈 수 있을 정도로 뚫려 있지는 않다."
                            ),
                        )
                    ],
                ),
                # 길이 열린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="lake_path_opened",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "석회문 아래쪽 틈을 통해 지하 호수 쪽으로 내려가시겠습니까?\n"
                                    "미끄러운 경사면을 따라 내려가느라 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 벽을 짚고 몸을 낮춘 채, 물소리가 울려오는 아래쪽 지하 호수 방향으로 천천히 내려간다.",
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE7,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 동굴 홀 주변의 다른 것들을 더 살펴보기로 한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),

        # --- [석영 / 지하수 자원] ---
        KeywordId.QUARTZ_CLUSTER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "석회층 사이로 맑은 석영 결정들이 모여 자라고 있다. 빛을 받으면 동굴 안쪽으로 은은하게 퍼뜨릴 것 같다."
            ),
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="quartz_discovered",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="quartz_collected",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "손에 쥘 수 있을 만큼 적당한 크기의 석영 조각을 몇 개 조심스럽게 떼어냈다.\n"
                                "진동을 잘 전달할 것 같은 맑은 덩어리라, 나중에 발진기나 시계 회로에 쓸 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.QUARTZ_SHARD,
                                "description": "맑은 석영 조각이다. 전자 장비의 기준 발진기로 쓰기에 적당해 보인다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "quartz_collected", "value": True},
                        ),
                    ],
                ),
                # 이미 채취한 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="quartz_collected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="석영 군집에서 더 떼어낼 만한 조각은 남지 않았다.",
                        )
                    ],
                ),
            ],
        ),

        KeywordId.UNDERGROUND_SPRING: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "석회층 사이 좁은 틈에서 맑은 물줄기가 솟아 나와 작은 웅덩이를 만들고 있다. 물을 만져보니 손이 얼얼할 만큼 차갑다."
            ),
            interactions=[
                # 처음 발견하고 물을 뜰 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="spring_discovered",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="spring_collected",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "손을 웅덩이에 넣어 물을 떠보니, 피부가 금방 얼얼해질 정도로 차갑다.\n"
                                "이 정도 온도라면 열 식히는 용도로 쓰기에 안성맞춤이다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.COLD_GROUNDWATER,
                                "description": "석회 동굴에서 떠온 차갑고 맑은 지하수다. MK-II 냉각수로 쓰기 좋을 것 같다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "spring_collected", "value": True},
                        ),
                    ],
                ),
                # 이미 물을 떠간 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="spring_collected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="웅덩이에서는 여전히 찬물이 조금씩 솟아나고 있지만, 지금은 더 떠갈 필요는 없어 보인다.",
                        )
                    ],
                ),
            ],
        ),

        # --- [석회암 2진수 패널 퍼즐] ---
        KeywordId.LIME_PANEL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "벽 한쪽을 가득 메운 석회 패널 위에 크고 작은 둥근 점 일곱 개가 일렬로 박혀 있다.\n"
                "일부 점은 표면이 약간 더 반들거리고, 일부는 메마른 석회처럼 바래 있다."
            ),
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "점들을 하나하나 살펴보니, 어떤 점은 손가락을 대면 미세하게 움푹 들어가는 느낌이 들고, "
                                "어떤 점은 단단하게 굳어 아무 반응이 없다.\n"
                                "조금 떨어진 지하수 소리가 규칙적인 리듬으로 떨어지는 것이, 어쩐지 이 점들의 배열과 닮아 보인다."
                            ),
                        ),
                        # 점 키워드들을 활성화
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_1, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_2, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_3, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_4, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_5, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_6, "state": KeywordState.HIDDEN},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_7, "state": KeywordState.HIDDEN},
                        ),
                    ]
                )
            ],
        ),

        # 일곱 개의 점 – 순서 누르기 퍼즐 (● ○ ● ● ○ ○ ●)
        KeywordId.LIME_DOT_1: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 첫 번째 점이다. 가까이서 보면 다른 점보다 표면이 약간 더 반들거린다.",
            interactions=[
                # 정답 시퀀스의 1단계 (step == 0)
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_step",
                            value=0,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="첫 번째 점을 누르자 미세한 클릭 소리와 함께 점이 안쪽으로 조금 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 1},
                        ),
                    ],
                ),
                # 이미 풀린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="첫 번째 점은 이미 안쪽으로 들어가 고정된 상태다.",
                        )
                    ],
                ),
                # 그 외 잘못된 타이밍에 눌렀을 때 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="점이 잠깐 흔들렸지만, 다시 원래 자리로 돌아가 버린다. 패턴이 어긋난 것 같다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 0},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_2: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 두 번째 점이다. 딱딱하게 굳어 있어 눌러도 움직일 것 같지 않다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="두 번째 점을 눌러 보지만, 단단하게 굳어 있어 아무 반응이 없다.",
                        )
                    ]
                )
            ],
        ),
        KeywordId.LIME_DOT_3: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 세 번째 점이다. 표면에 작은 균열이 가 있어 누르면 안으로 들어갈 것 같다.",
            interactions=[
                # 정답 시퀀스의 2단계 (step == 1)
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_step",
                            value=1,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 점을 누르자 첫 번째 점과 마찬가지로 안쪽으로 살짝 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 2},
                        ),
                    ],
                ),
                # 이미 풀린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 점은 이미 안쪽으로 들어가 고정된 상태다.",
                        )
                    ],
                ),
                # 그 외 잘못된 타이밍 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 점을 눌러 보았지만, 패턴이 어긋났는지 다시 모두 원위치로 튕겨 나온다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 0},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_4: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 네 번째 점이다. 다른 반응하는 점들과 비슷하게 표면이 유난히 매끈하다.",
            interactions=[
                # 정답 시퀀스의 3단계 (step == 2)
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_step",
                            value=2,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 점을 누르자 안쪽에서 금속 장치가 한 번 더 '딸깍' 하고 움직인다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 3},
                        ),
                    ],
                ),
                # 이미 풀린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 점은 이미 안쪽으로 들어가 고정된 상태다.",
                        )
                    ],
                ),
                # 그 외 잘못된 타이밍 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 점을 누르자 한동안 침묵이 흐르더니, 모든 점이 다시 원위치로 튕겨 오른다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 0},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_5: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 다섯 번째 점이다. 메마른 석회처럼 바래 있어, 눌러도 미동조차 없다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다섯 번째 점은 아무리 눌러도 미동도 하지 않는다.",
                        )
                    ]
                )
            ],
        ),
        KeywordId.LIME_DOT_6: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 여섯 번째 점이다. 다른 굳어 있는 점들과 마찬가지로 전혀 반응을 보이지 않는다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="여섯 번째 점도 굳어 있어, 누르면 손가락만 아플 뿐이다.",
                        )
                    ]
                )
            ],
        ),
        KeywordId.LIME_DOT_7: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 일곱 번째 점이다. 표면이 반들반들해 다른 반응 점들과 비슷해 보인다.",
            interactions=[
                # 정답 시퀀스의 마지막 단계 (step == 3)
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_step",
                            value=3,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "일곱 번째 점을 누르자, 지금까지 눌러 온 점들이 모두 안쪽으로 완전히 잠기며 "
                                "석회 패널 전체가 낮게 떨리기 시작한다.\n"
                                "잠시 뒤 패널 아래쪽 석회층이 갈라지며, 지하에서 올라오는 차가운 공기와 함께 "
                                "멀리서 물 떨어지는 소리가 또렷하게 들려온다.\n"
                                "갈라진 틈 사이로는 작은 지하 샘과, 그 옆 벽면에 박힌 석영 군집이 모습을 드러낸다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_solved", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 0},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lake_path_opened", "value": True},
                        ),
                        # 지하 샘과 석영 군집도 이때 함께 드러나도록 처리
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "spring_discovered", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "quartz_discovered", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={
                                "keyword": KeywordId.UNDERGROUND_SPRING,
                                "state": KeywordState.DISCOVERED,
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={
                                "keyword": KeywordId.QUARTZ_CLUSTER,
                                "state": KeywordState.DISCOVERED,
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[지하 샘]**과 **[석영 군집]**이 시야에 드러났습니다.",
                        ),
                    ],
                ),
                # 이미 풀린 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="일곱 번째 점은 이미 완전히 안쪽으로 잠겨 고정되어 있다.",
                        )
                    ],
                ),
                # 그 외 잘못된 타이밍 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="binary_panel_solved",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="일곱 번째 점을 누르자마자 패널이 잠깐 진동하다가, 모든 점이 다시 원래 자리로 튕겨 나온다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "binary_panel_step", "value": 0},
                        ),
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # 시계문 비밀번호: 064530 (짧은 돌: 06, 중간 돌: 45, 긴 돌: 30)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.TIME_DOOR, "064530"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석회문 옆 작은 키패드에 064530을 입력하자, 한동안 조용하던 동굴이 낮게 울리기 시작한다.\n"
                        "곧이어 원형 석회문이 바닥을 긁는 소리를 내며 옆으로 천천히 밀려난다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "shadow_door_unlocked", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "cliff_path_opened", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.CLIFF_PATH,
                        "state": KeywordState.DISCOVERED,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.UNDERGROUND_LAKE_PATH,
                        "state": KeywordState.DISCOVERED,
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="석회문이 열리며 위쪽 절벽과 아래쪽 지하 호수로 이어지는 통로가 드러났습니다.",
                ),
            ],
        ),
        # 석회 패널에 식초를 뿌려 보는 조합 – 반응하는 점과 안 하는 점 힌트
        Combination(
            targets=[KeywordId.LIME_PANEL, KeywordId.VINEGAR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "식초를 석회 패널 위에 조금 뿌려 보았다.\n"
                        "일부 점에서는 조그만 기포가 피어오르며 색이 더 짙어지지만, "
                        "다른 점들은 축축해졌을 뿐 아무 변화도 없다.\n"
                        "마치 어떤 점은 살아 있고, 어떤 점은 이미 돌처럼 굳어 버린 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="반응하는 점과 전혀 반응하지 않는 점이 명확히 나뉩니다. 순서와 패턴을 잘 관찰해 두는 편이 좋겠습니다.",
                ),
            ],
        ),
    ],
)
