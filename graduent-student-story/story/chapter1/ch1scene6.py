from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE6_DATA = SceneData(
    id=SceneID.CH1_SCENE6,
    name="석회 동굴 (수정 동굴)",
    initial_text=(
        "늪지대를 벗어나 바위 경사면을 따라 올라오자, 공기가 서늘하게 식어 간다.\n"
        "바위 틈 사이로 몸을 비집고 들어가자 곧 머리 위로 석회암 종유석이 빽빽이 매달린 동굴 홀이 펼쳐진다.\n\n"
        "입구 쪽에서 들어오는 희미한 빛이 동굴 바닥과 벽을 스치고 지나가며, 벽면에는 거대한 원형의 석회 문양이 어렴풋이 떠오른다.\n"
        "가까이 눈을 찌푸리고 바라보면, 그 중앙에 굳게 닫힌 둥근 석회문이 자리하고 있다.\n\n"
        "홀 한쪽 벽은 하얀 석회층으로 뒤덮여 있는데, 그 아래쪽에는 크고 작은 점무늬가 정갈하게 배열된 석회 패널이 희미하게 형체를 드러낸다.\n"
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
        "hall_inspected": False,  # 동굴 홀을 처음 조사했는지 여부
        "lime_btn_1": 0,
        "lime_btn_2": 0,
        "lime_btn_3": 0,
        "lime_btn_4": 0,
        "lime_btn_5": 0,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # 늪지대로 되돌아가는 길
        KeywordId.SWAMP_PATH_ALIAS: KeywordData(
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
        # 중앙 동굴 홀
        KeywordId.CAVE_HALL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "동굴 중앙은 둥근 홀처럼 트여 있다. 바닥에서 솟아오른 키가 서로 다른 세 개의 돌기둥이 빛을 받아 "
                "벽면에 서로 다른 방향의 그림자를 드리우고 있다.\n"
                "벽 한쪽에는 거대한 원형 석회 문양이 있고, 그 중앙에는 굳게 닫힌 석회문이 자리하고 있다."
            ),
            interactions=[
                # 첫 조사: 동굴 홀 DISCOVER + 짧은/중간/긴 돌을 노출
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="hall_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.CAVE_HALL, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동굴 중앙으로 조심스럽게 걸어 들어가자, 둥근 바닥 위에 서로 다른 높이의 돌기둥 세 개가 서 있는 것이 보인다.\n"
                                "각 돌기둥은 바깥에서 들어오는 희미한 빛을 받아 벽면의 석회문에 각기 다른 방향의 그림자를 드리우고 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.SHORT_STONE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MID_STONE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LONG_STONE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "hall_inspected", "value": True},
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="바닥의 **[짧은 돌]**, **[중간 돌]**, **[긴 돌]**이 눈에 들어오기 시작합니다.",
                        ),
                    ],
                ),
                # 이후 재조사
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="hall_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동굴 중앙에는 여전히 세 개의 돌기둥이 서 있고, "
                                "그 그림자들은 석회문 위에 멈춰 서 있는 것처럼 보인다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 짧은 돌
        KeywordId.SHORT_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "가장 키가 낮은 돌기둥이다. 입구 쪽에서 들어오는 빛을 받으면, "
                "그림자가 석회문의 오른쪽 부분으로 짧게 드리워진다.\n"
            ),
        ),
        # 중간 돌
        KeywordId.MID_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=("중간 높이의 돌기둥이다. 그림자를 자세히 따라가 보니, 석회문의 왼쪽 부분에 걸쳐 멈춰 있다.\n"),
        ),
        # 긴 돌
        KeywordId.LONG_STONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "가장 키가 큰 돌기둥이다. 그림자는 바닥을 따라 길게 뻗어 내려가더니, "
                "석회문의 아래쪽 가장 낮은 위치에 걸쳐 있다.\n"
            ),
        ),
        # 석회문
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
                                "벽면을 거의 가득 메운 거대한 원형 석회 문양이 서늘하게 돋보인다.\n"
                                "바깥쪽은 일정한 간격으로 조각된 홈들이 이어져 있고, 그 안쪽에는 더 촘촘한 자국들과 숫자 흔적들이 층처럼 남아 있다.\n"
                                "형태만 보면 그저 오래된 돌무늬 같지만, 바닥에서 솟은 서로 다른 높이의 세 돌기둥이 드리우는 그림자와 "
                                "아주 미세하게 부합하는 듯한 느낌이 든다.\n\n"
                                "석회문 아래쪽 모서리에는 거의 지워진 필치로 이런 문장이 남아 있다.\n"
                                "\"세 돌이 가리키는 흐름을 잇는 자만이, 문 너머로 나아갈 수 있으리라.\"\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`석회문 : [비밀번호 여섯자리]` 형태로 입력하세요.",
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
        # 절벽 통로(위)
        KeywordId.CLIFF_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.INACTIVE,
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
                                "석회문 가까이에서 위쪽 협곡 틈을 올려다보면, "
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
                                        value="당신은 석회문 옆 바위를 짚고 좁은 협곡 틈을 따라 위쪽 절벽으로 오르기 시작한다.",
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
        # 지하 호수 통로(아래)
        KeywordId.UNDERGROUND_LAKE_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.INACTIVE,
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
                "석회층 사이로 맑은 석영 결정들이 모여 자라고 있다. 겉보기엔 단단해서, 맨손으로는 깨내기 어려울 것 같다.\n"
                "무언가 묵직한 도구로 한 번 내려쳐야 조각을 떼어낼 수 있을 것 같다."
            ),
            interactions=[
                # 아직 석영을 안 땄을 때 → 힌트만
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quartz_discovered", value=True),
                        Condition(type=ConditionType.STATE_IS, target="quartz_collected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "석영 표면을 손가락으로 긁어 보았지만, 단단한 결정이어서 손으로는 아무 조각도 떨어지지 않는다.\n"
                                "충분히 무거운 도구로 한 번 내려쳐야 할 것 같다."
                            ),
                        )
                    ],
                ),
                # 이미 조각을 얻은 뒤
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quartz_collected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="석영 군집은 일부가 깨져 나간 채 남아 있다. 더 떼어낼 만한 조각은 없어 보인다.",
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
                # 처음 발견했을 때: 한 입 마시고 체력 +10, spring_collected 플래그만 세팅
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="spring_discovered", value=True),
                        Condition(type=ConditionType.STATE_IS, target="spring_collected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "목이 바싹 마른 김에 한 모금 떠서 조심스럽게 입에 머금었다.\n"
                                "입 안 가득 차가운 물이 퍼지자, 잠시 동안 머릿속까지 선명해지는 느낌이 든다."
                            ),
                        ),
                        Action(
                            type=ActionType.MODIFY_STAMINA,
                            value=10,
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "spring_collected", "value": True},
                        ),
                    ],
                ),
                # 이미 물을 마신 뒤
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="spring_collected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "웅덩이에서는 여전히 찬물이 조금씩 솟아나고 있지만, 방금 마신 한 모금만으로도 갈증은 충분히 가신 것 같다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # --- [석회암 패널 퍼즐: 5개 버튼 + 래버] ---
        KeywordId.LIME_PANEL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "벽 한쪽을 가득 메운 석회 패널 위에 크고 작은 둥근 버튼 다섯 개가 일렬로 박혀 있다.\n"
                "일부 버튼은 표면이 약간 더 반들거리고, 일부는 메마른 석회처럼 바래 있다."
            ),
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "버튼들을 하나하나 살펴보니, 어떤 것은 손가락을 대면 미세하게 움푹 들어가는 느낌이 들고, "
                                "어떤 것은 단단하게 굳어 아무 반응이 없다.\n"
                                "겉에 굳어 있는 석회층을 제거할 방법을 찾아보는 게 좋겠다."
                            ),
                        ),
                        # 버튼 존재만 알림 (실제 활성화는 식초 조합에서)
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_1, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_2, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_3, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_4, "state": KeywordState.INACTIVE},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LIME_DOT_5, "state": KeywordState.INACTIVE},
                        ),
                    ]
                )
            ],
        ),
        # 버튼 1~5 (0/1 토글)
        KeywordId.LIME_DOT_1: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 첫 번째 버튼이다. 표면이 약간 더 반들거리는 작은 둥근 버튼이다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_1", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="첫 번째 버튼을 누르자, 딸깍 하는 소리와 함께 안쪽으로 살짝 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_1", "value": 1},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_1", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="첫 번째 버튼이 다시 제자리로 튀어 올라온다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_1", "value": 0},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="첫 번째 버튼은 이미 고정된 상태다. 더 이상 누를 필요는 없어 보인다.",
                        )
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_2: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 두 번째 버튼이다. 살짝 옅은 흠집이 나 있어 다른 버튼과 구분된다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_2", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="두 번째 버튼을 누르자, 짧은 울림과 함께 안쪽으로 눌린다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_2", "value": 1},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_2", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="두 번째 버튼이 사르륵 소리를 내며 다시 튀어 오른다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_2", "value": 0},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="두 번째 버튼은 단단히 굳어 있다. 더 이상 움직이지 않는다.",
                        )
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_3: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 세 번째 버튼이다. 가장 평범해 보이지만, 미세하게 중앙이 파여 있다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_3", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 버튼이 또각 소리를 내며 안으로 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_3", "value": 1},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_3", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 버튼이 천천히 원래 자리로 밀려 올라온다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_3", "value": 0},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="세 번째 버튼 주변의 석회질이 단단하게 굳어, 아예 손을 댈 수 없을 것 같다.",
                        )
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_4: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 네 번째 버튼이다. 다른 버튼보다 살짝 기울어진 듯한 인상을 준다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_4", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 버튼을 누르자, 비뚤어진 느낌 그대로 안쪽으로 눌려 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_4", "value": 1},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_4", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 버튼이 약간의 마찰음을 남기며 다시 튀어 오른다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_4", "value": 0},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="네 번째 버튼은 이미 어떤 힘에 의해 고정된 듯 꿈쩍도 하지 않는다.",
                        )
                    ],
                ),
            ],
        ),
        KeywordId.LIME_DOT_5: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널의 다섯 번째 버튼이다. 가장 모서리 쪽에 있어 살짝 누르기 불편한 위치에 있다.",
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_5", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="손가락을 끝까지 뻗어 다섯 번째 버튼을 누르자, 미묘한 진동과 함께 쑥 들어간다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_5", "value": 1},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_5", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다섯 번째 버튼이 아슬아슬하게 밀려 나오며, 다시 원래 위치로 돌아온다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "lime_btn_5", "value": 0},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다섯 번째 버튼은 패널의 다른 부분과 함께 굳어, 손가락으로 눌러도 전혀 움직이지 않는다.",
                        )
                    ],
                ),
            ],
        ),
        # 확인 래버
        KeywordId.LIME_CONFIRM: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="석회 패널 오른쪽에 있는 래버다.",
            interactions=[
                # 정답 패턴일 때 (예: 1,0,0,0,1)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_1", value=1),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_2", value=0),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_3", value=0),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_4", value=0),
                        Condition(type=ConditionType.STATE_IS, target="lime_btn_5", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "래버를 당기자, 석회 패널 전체가 낮게 떨리며 버튼들이 한꺼번에 안쪽으로 잠긴다.\n"
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
                            value={"key": "lake_path_opened", "value": True},
                        ),
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
                            value={"keyword": KeywordId.UNDERGROUND_SPRING, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.QUARTZ_CLUSTER, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[지하 샘]**과 **[석영 군집]**이 시야에 드러났습니다.",
                        ),
                    ],
                ),
                # 오답 패턴일 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="래버를 당겨 보았지만, 패널 안쪽에서 잠깐 삐거덕거리는 소리만 날 뿐 아무 일도 일어나지 않는다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="버튼의 조합이 맞지 않는 것 같다. 패턴을 다시 조정해 보자.",
                        ),
                    ],
                ),
                # 이미 퍼즐을 푼 뒤
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="binary_panel_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="래버는 이미 한 역할을 끝낸 듯 묵묵히 잠겨 있다.",
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # 석회문 비밀번호: 034530
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.TIME_DOOR, "034530"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석회문 옆 작은 키패드에 034530을 입력하자, 한동안 조용하던 동굴이 낮게 울리기 시작한다.\n"
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
                    value="석회문이 열리며 위쪽 **[절벽 길]**과 아래쪽 **[지하 호수 통로]**가 드러났습니다.",
                ),
            ],
        ),
        # 석회 패널 + 반쯤 남은 식초 → 버튼 5개 + 래버 활성화
        Combination(
            targets=[KeywordId.LIME_PANEL, KeywordId.VINEGAR_HALF],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR_HALF),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "반쯤 남은 식초를 석회 패널 위에 조심스럽게 뿌렸다.\n"
                        "굳어 있던 석회층이 서서히 녹아내리자, 다섯 개의 둥근 버튼이 또렷하게 솟아오른다.\n"
                        "버튼 오른쪽에는 **[석회 패널 래버]**라고 적힌 래버도 하나 있다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_DOT_1, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_DOT_2, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_DOT_3, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_DOT_4, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_DOT_5, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LIME_CONFIRM, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 **[석회 패널 1번 점]**부터 **[석회 패널 5번 점]**, 그리고 **[석회 패널 래버]**를 사용하여 패턴을 맞출 수 있습니다.",
                ),
            ],
        ),
        # 소방 도끼 + 석영 군집 → 석영 조각 한 번만 획득
        Combination(
            targets=[KeywordId.FIRE_AXE, KeywordId.QUARTZ_CLUSTER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quartz_discovered", value=True),
                Condition(type=ConditionType.STATE_IS, target="quartz_collected", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼를 힘껏 휘둘러 석영 군집 한 귀퉁이를 내려쳤다.\n"
                        "맑은 파편들이 튀어 오르며, 그중 손바닥만 한 조각 하나가 바닥에 떨어진다."
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
    ],
)
