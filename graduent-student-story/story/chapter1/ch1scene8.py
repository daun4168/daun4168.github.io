import json

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

CH1_SCENE8_DATA = SceneData(
    id=SceneID.CH1_SCENE8,
    name="가파른 절벽 (바람의 언덕)",
    body=(
        "석회 동굴 벽을 짚고 좁은 협곡을 비집고 나오자, 갑자기 하늘이 쫙 열리며 바람이 얼굴을 후려친다.\n"
        "발밑은 절벽 가장자리, 아래로는 지나온 숲과 늪, 해변이 한눈에 내려다보인다.\n\n"
        "옆에는 거칠게 긁힌 장비 상자가 놓여 있고, 위쪽에는 바람을 정면으로 맞받는 바위 턱이 어둡게 솟아 있다.\n"
        "바닥 가까이에는 크기가 제각각인 돌무더기가 쌓여 있어 발걸음을 더욱 조심하게 만든다.\n\n"
        "절벽을 따라 불어오는 바람은 일정하지 않아, 이곳에서 무언가 작업했던 흔적들이 더 선명하게 느껴진다."
    ),
    initial_state={
        # 상자들 상태
        "gear_crate_opened": False,  # 장비 상자 열렸는지
        "gear_nameplate_detached": False,  # 장비 상자에서 금속 명판을 떼어냈는지
        "obs_crate_opened": False,  # 관측 장비 상자(풍향계 재료)
        "ascent_crate_opened": False,  # 등반 장비 상자(도르래 재료)
        "stone_pick_count": 0,  # 돌을 몇 개 쪼아냈는지 (0~5)
        # 도르래 제작/설치 상태
        "rope_prepared": False,  # 정리된 로프 끝 제작 여부
        "harness_set_built": False,  # 하네스 세트 제작 여부
        "main_pulley_prepared": False,  # 설치용 큰 도르래 제작 여부
        "pulley_progress": 0,  # 바위 턱 위 도르래 설치 단계 (0~5)
        "climb_ready": False,  # 절벽 등반 준비 완료 여부
        # 경로 설명 여부
        "cliff_path_inspected": False,  # 위로 가는 길 설명 했는지
        "back_path_inspected": False,  # 석회 동굴로 내려가는 길 설명 했는지
        "wind_log_step": 0,
        "weight_puzzle_solved": False,  # 돌 무게 평형추 퍼즐 해결 여부
        "stone_1_used": False,
        "stone_2_used": False,
        "stone_3_used": False,
        "stone_4_used": False,
        "stone_5_used": False,
    },
    keywords={
        KeywordId.CLIFF_BACK_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,  # 이거만 처음부터 보이도록
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
        KeywordId.PULLEY_ANCHOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "절벽 상단 가까이에 튀어나온 단단한 바위 턱이 보인다.\n"
                "거칠게 닳은 표면이, 여기서 무언가를 여러 번 걸었다 뗐다 한 흔적을 말해 준다."
            ),
            interactions=[
                # progress 0: 아직 아무것도 안 설치된 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "바위 턱 위에는 지금 아무것도 걸려 있지 않다.\n"
                                "손으로 잡아 보니 충분히 단단해서, 무거운 것 하나 정도 매달려도 끄떡없을 것 같다."
                            ),
                        )
                    ],
                ),
                # progress 1: 설치용 큰 도르래까지 단 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=1),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "바위 턱에는 이제 큰 도르래가 달려 있다.\n"
                                "바람에 따라 천천히 흔들리는 모습만 보면, 아직 이 장치가 무엇을 끌어올려야 하는지 정해지지 않은 것처럼 보인다."
                            ),
                        )
                    ],
                ),
                # progress 2: 도르래 + 정리된 로프 끝까지 통과된 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=2),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "도르래를 통과한 로프가 바위 턱 위아래로 늘어져 있다.\n"
                                "줄만 늘어진 모양새라 그런지, 아직은 이 줄에 무엇을 연결해야 할지가 조금 비어 보인다."
                            ),
                        )
                    ],
                ),
                # progress 3: 하네스 세트까지 연결된 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=3),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "로프 한쪽에 하네스 세트가 매달려 있다.\n"
                                "구조는 갖춰졌지만, 볼트와 연결부 여기저기가 손에 힘을 주면 미세하게 움직이는 느낌이 남아 있다."
                            ),
                        )
                    ],
                ),
                # progress 4: 스패너로 조임까지 끝난 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=4),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "볼트와 연결부를 한 번씩 잡아당겨 보아도 쉽게 움직일 기미는 보이지 않는다.\n"
                                "다만 로프의 남은 부분이 다소 느슨하게 늘어져 있어, 마지막 손질이 조금 남은 듯한 인상을 준다."
                            ),
                        )
                    ],
                ),
                # progress 5 이상: 완성된 상태 (climb_ready == True일 것)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
                        Condition(type=ConditionType.STATE_IS, target="stone_1_used", value=False),
                        Condition(type=ConditionType.STATE_IS, target="stone_2_used", value=False),
                        Condition(type=ConditionType.STATE_IS, target="stone_3_used", value=False),
                        Condition(type=ConditionType.STATE_IS, target="stone_4_used", value=False),
                        Condition(type=ConditionType.STATE_IS, target="stone_5_used", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "바위 턱 위에는 도르래와 로프, 하네스가 하나의 장치처럼 자연스럽게 이어져 있다.\n"
                                "도르래 옆으로는 작은 금속 접시가 하나 매달려 있는데, 평형추를 올려둘 자리인 듯 허공에서 가볍게 흔들린다.\n"
                                "지금 상태라면, 여기에 적당한 무게를 맞춰 걸기만 하면 장치 전체의 균형이 잡힐 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="이제 평형추로 쓸 돌을 모두 선택해 바위 턱에 걸어두고, 다시 돌어와서 무게가 적절한지 확인해 보세요.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
                        Condition(
                            type=ConditionType.STONE_PUZZLE,
                            target=json.dumps(
                                {
                                    "keys": [
                                        "stone_1_used",
                                        "stone_2_used",
                                        "stone_3_used",
                                        "stone_4_used",
                                        "stone_5_used",
                                    ],
                                    "weights": [1, 4, 7, 8, 11],
                                    "target_weight": 18,
                                }
                            ),
                            value="gt",
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("너무 무거운 것 같다. 처음부터 다시 해 보자."),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_1_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_2_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_3_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_4_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_5_used", "value": False}),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_1),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_2),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_3),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_4),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_5),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_1,
                                "description": "손 안에 쏙 들어오는 작은 돌이다. 흔히 볼 수 있는 자갈처럼 보이지만 제법 단단하다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_2,
                                "description": "손에 쥐면 조금 묵직하게 느껴지는 돌이다. 표면이 단단해서 평형추로 쓰기 좋다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_3,
                                "description": "표면이 매끈한 돌이다. 크기에 비해 묵직한 편이라 감이 독특하다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_4,
                                "description": "손바닥을 가득 채우는 크기의 돌이다. 모서리가 적당히 둥글다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_5,
                                "description": "다섯 개 중 가장 큰 돌이다. 평형추로 쓰기 딱 좋아 보인다.",
                                "silent": True,
                            },
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
                        Condition(
                            type=ConditionType.STONE_PUZZLE,
                            target=json.dumps(
                                {
                                    "keys": [
                                        "stone_1_used",
                                        "stone_2_used",
                                        "stone_3_used",
                                        "stone_4_used",
                                        "stone_5_used",
                                    ],
                                    "weights": [1, 4, 7, 8, 11],
                                    "target_weight": 18,
                                }
                            ),
                            value="lt",
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("너무 가벼운 것 같다. 처음부터 다시 해 보자."),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_1_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_2_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_3_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_4_used", "value": False}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "stone_5_used", "value": False}),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_1),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_2),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_3),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_4),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_5),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_1,
                                "description": "손 안에 쏙 들어오는 작은 돌이다. 흔히 볼 수 있는 자갈처럼 보이지만 제법 단단하다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_2,
                                "description": "손에 쥐면 조금 묵직하게 느껴지는 돌이다. 표면이 단단해서 평형추로 쓰기 좋다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_3,
                                "description": "표면이 매끈한 돌이다. 크기에 비해 묵직한 편이라 감이 독특하다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_4,
                                "description": "손바닥을 가득 채우는 크기의 돌이다. 모서리가 적당히 둥글다.",
                                "silent": True,
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STONE_5,
                                "description": "다섯 개 중 가장 큰 돌이다. 평형추로 쓰기 딱 좋아 보인다.",
                                "silent": True,
                            },
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
                        Condition(
                            type=ConditionType.STONE_PUZZLE,
                            target=json.dumps(
                                {
                                    "keys": [
                                        "stone_1_used",
                                        "stone_2_used",
                                        "stone_3_used",
                                        "stone_4_used",
                                        "stone_5_used",
                                    ],
                                    "weights": [1, 4, 7, 8, 11],
                                    "target_weight": 18,
                                }
                            ),
                            value="eq",
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "이제 완벽하게 평형을 이루었다. 장치가 안정적으로 작동하는 느낌이다.\n"
                                "더 이상 돌은 필요 없을 것 같다. 이제 절벽으로 가 보자."
                            ),
                        ),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_1),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_2),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_3),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_4),
                        Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_5),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "weight_puzzle_solved", "value": True},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.STONE_PILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="절벽 아래에는 크기가 다른 돌들이 잔뜩 쌓여 있다.",
            interactions=[
                # 처음 보는 경우 (돌도 안 쪼았고, 피쳐폰도 아직 못 본 상태)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=0),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "돌무더기를 살펴보니, 겉에 쌓인 자잘한 돌들은 손으로 집어 들기엔 너무 가볍고 부서지기 쉽다.\n"
                                "속에 박힌 덩어리를 소방 도끼로 쪼아 내면, 평형추로 쓰기 좋은 돌들을 뽑아낼 수 있을 것 같다.\n\n"
                                "돌무더기 가장자리에는 먼지와 모래에 파묻힌 고장난 피쳐폰 하나가 나뒹굴고 있다.\n"
                                "별 모양 스티커가 붙어 있는 걸 보니, 이 섬 어디선가 쓰이던 장비였던 것 같다."
                            ),
                        ),
                        # 고장난 피쳐폰 오브젝트를 발견 상태로 전환
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={
                                "keyword": KeywordId.BROKEN_FEATURE_PHONE,
                                "state": KeywordState.DISCOVERED,
                            },
                        ),
                    ],
                ),
                # 돌을 다섯 개 다 쪼아낸 뒤
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=5),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="돌무더기 표면에는 이미 도끼 자국이 여러 개 남아 있다. 더 쓸만한 돌이 있을지 모르겠다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.CLIFF_WIND: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "절벽 위쪽에서 거센 바람이 불어온다. 방향이 일정하지 않고, 때때로 방향을 바꾸며 불고 멈추기를 반복한다."
            ),
        ),
        # --- 상자들 ---
        KeywordId.EQUIPMENT_BUNDLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="덮개가 반쯤 열린 장비 상자다. 하지만 안쪽은 별도의 잠금 장치로 막혀 있는 것 같다.",
            interactions=[
                # 아직 안 열었고, 명판도 안 뜯었을 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=False),
                        Condition(type=ConditionType.STATE_IS, target="gear_nameplate_detached", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "장비 상자 안쪽에는 네 자리 숫자를 맞추는 자물쇠와, 그 옆에 얇은 금속판이 나사로 붙어 있다.\n"
                                "나사를 풀어 보면 금속판을 떼어낼 수 있을지도 모르겠다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`장비 상자 : [비밀번호 네자리]` 형태로 입력하세요.",
                        ),
                    ],
                ),
                # 아직 안 열었지만, 명판은 이미 떼어낸 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=False),
                        Condition(type=ConditionType.STATE_IS, target="gear_nameplate_detached", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "장비 상자 안쪽 자물쇠 아래에는 금속 명판을 떼어낸 자국이 남아 있다.\n"
                                "나사 자국 모양을 보니, 명판이 처음에는 거꾸로 달려 있었던 것 같다.\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`장비 상자 : [비밀번호 네자리]` 형태로 입력하세요.",
                        ),
                    ],
                ),
                # 이미 상자를 연 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "장비 상자 안은 이미 한 번 뒤졌기 때문에, 이제는 텅 비어 있다.\n"
                                "관측 장비 상자와 등반 장비 상자, 그리고 로프는 이미 밖으로 꺼내 둔 상태다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="장비 상자는 이미 열려 있다. 필요한 것들은 모두 꺼냈다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.WEATHER_CRATE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                # 아직 안 연 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="obs_crate_opened", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "철제 관측 장비 상자 앞에는 네 자리 숫자를 맞추는 자물쇠가 달려 있다.\n"
                                "상자 뚜껑 안쪽에는 연필로 끄적인 문장이 하나 보인다.\n\n"
                                "\n\n"
                                "**별에서 시작해서, 바람이 가리키는 대로 움직인다.**\n\n"
                                "**위로 한 칸, 오른쪽으로 한 칸, 다시 위로 한 칸, 다시 오른쪽으로 한 칸.**\n\n"
                                "**길을 네 번 따라가면, 네 자리 숫자가 남는다.**\n\n"
                                "\n\n"
                                "별이라는 말과 바람이라는 말이 유난히 진하게 눌려 적혀 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`관측 장비 상자 : [비밀번호 네자리]` 형태로 입력하세요.",
                        ),
                    ],
                ),
                # 이미 연 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="obs_crate_opened", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "관측 장비 상자 안에는 이미 필요한 부품들을 모두 꺼낸 뒤라, "
                                "자잘한 포장재와 녹슨 나사 몇 개만 굴러다니고 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="관측 장비 상자는 이미 열려 있다. 안은 비어 있다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.ASCENT_CRATE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="등반 장비가 들어 있을 법한 길쭉한 상자다. 잠금 장치는 바람 방향 모양의 아이콘으로 꾸며져 있다.",
            interactions=[
                # 아직 안 연 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ascent_crate_opened", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "길쭉한 등반 장비 상자 앞에는 작은 다이얼 자물쇠가 달려 있다.\n"
                                "자물쇠 주변에는 동, 서, 남, 북을 가리키는 작은 화살표와, "
                                "그 아래로 이어진 곡선이 마치 바람의 흐름을 그려 둔 것처럼 새겨져 있다.\n"
                                "W는, 서쪽에서 불어오는 바람, NE는 북동쪽에서 불어오는 바람을 뜻하는 것 같다.\n\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`등반 장비 상자 : [비밀번호 네자리]` 형태로 입력하세요.",
                        ),
                    ],
                ),
                # 이미 연 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="ascent_crate_opened", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "등반 장비 상자 안에는 비어 있는 받침대와 얇은 포장재만 남아 있다.\n"
                                "도르래와 하네스는 이미 밖으로 꺼내 놓은 상태다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="등반 장비 상자는 이미 열려 있다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.BROKEN_FEATURE_PHONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="바람 모양 스티커가 붙어 있던 오래된 피쳐폰이다. 화면은 깨져 있고 전원은 들어오지 않는다.",
            interactions=[
                Interaction(
                    conditions=[],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "고장난 피쳐폰을 집어 들어 뒤집어 본다.\n\n"
                                "앞면의 화면은 금이 가서 아무것도 보이지 않지만, 아래쪽 숫자 키패드는 아직 형태를 유지하고 있다.\n\n"
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # --- 이동 포탈: 위 / 아래 ---
        KeywordId.CLIFF_FACE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 첫 조사: 절벽 구조 설명 + 바위 턱/도르래 힌트
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "눈앞의 절벽은 거의 수직에 가깝다. 군데군데 튀어나온 바위 턱이 손잡이 역할을 해 줄 것 같지만, "
                                "맨몸으로 기어오르기에는 무리다.\n"
                                "절벽 위로 올라가려면, 저 바위 턱에 도르래를 걸어 놓고 그 힘을 빌려 올라가는 수밖에 없어 보인다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "cliff_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 도르래도 아직 완성 전: 그냥 못 올라감
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="climb_ready", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "절벽은 여전히 수직으로 서 있고, 바위 턱은 손에 잡힐 듯 먼 곳에 있다.\n"
                                "지금 상태로는 올라갈 수 없다. 도르래 장치를 완성해, 바위 턱에 제대로 걸어야만 이 절벽을 오를 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # 도르래는 완성됐지만, 평형추 퍼즐이 아직: 올라가면 위험해 보임
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="climb_ready", value=True),
                        Condition(type=ConditionType.STATE_IS, target="weight_puzzle_solved", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "도르래와 로프, 하네스는 하나의 장치처럼 이어져 있지만, 바위 턱 옆에 달린 빈 접시가 눈에 들어온다.\n"
                                "평형추가 걸려야 할 자리인 듯한 그 접시는, 지금은 텅 비어 덜컹거리며 흔들릴 뿐이다.\n"
                                "이대로 몸을 맡겼다가는, 무게가 맞지 않아 도르래가 제멋대로 튕겨 나갈지도 모른다.\n"
                                "절벽 아래 돌무더기에서 고른 돌들을 이용해, 적당한 무게를 맞추어야 할 것 같다."
                            ),
                        )
                    ],
                ),
                # 도르래 완성 + 평형추 퍼즐 해결 후: 절벽을 타고 올라갈지 선택
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="climb_ready", value=True),
                        Condition(type=ConditionType.STATE_IS, target="weight_puzzle_solved", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "바위 턱에 걸린 도르래 장치는 균형추까지 맞춰져, 더 이상 덜컹거리는 느낌이 없다.\n"
                                    "하네스를 확인하고 절벽을 타고 위 능선으로 올라가시겠습니까?\n"
                                    "올라가는 동안 **체력이 2 소모**됩니다."
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 하네스를 조이고, 로프를 잡아당기며 절벽 옆으로 천천히 몸을 끌어올린다.\n"
                                            "몇 번의 숨 고르기 끝에, 드디어 산 정상의 능선 위에 발을 딛는다."
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
                                        value="아직은 준비가 덜 된 것 같다. 장비 상태를 한 번 더 점검한다.",
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
        # ================================
        # 1) 장비 상자 퍼즐: 1699 -> 6691
        # ================================
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.EQUIPMENT_BUNDLE, "6691"],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "상자 옆 금속 패널에 6-6-9-1을 차례대로 눌러 본다.\n"
                        "잠시 후 안쪽에서 '투벅' 하는 무거운 소리와 함께 잠금 장치가 풀리는 느낌이 전해진다.\n"
                        "덮개를 들어 올리자, 안쪽에서 두 개의 작은 상자와 튼튼한 로프 한 뭉치가 모습을 드러낸다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gear_crate_opened", "value": True},
                ),
                # 명판은 더 이상 필요 없으니 인벤토리에서 제거 (있을 경우에만)
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.EQUIPMENT_NAMEPLATE,
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="장비 상자 명판은 더 이상 필요 없을 것 같다. 조심스레 배낭 한쪽에 밀어 넣었다.",
                ),
                # 관측/등반 상자 활성화(상태만)
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.WEATHER_CRATE, "state": KeywordState.DISCOVERED},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.ASCENT_CRATE, "state": KeywordState.DISCOVERED},
                ),
                # 로프 지급
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.CLIMBING_ROPE,
                        "description": "등반용 로프다. 사람 한 명쯤 매달려도 버틸 만큼 튼튼해 보이지만, 끝부분이 해져 있어 그대로는 도르래에 통과시키기 어렵다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="관측 장비 상자와 등반 장비 상자가 눈에 들어오기 시작합니다.",
                ),
            ],
        ),
        # =========================================
        # 2) 관측 장비 상자: 별 핸드폰 퍼즐
        # =========================================
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.WEATHER_CRATE, "7856"],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=True),
                Condition(type=ConditionType.STATE_IS, target="obs_crate_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "별 모양 아이콘이 그려진 잠금 장치에 코드를 입력하자, 상자에서 짧은 전자음이 들린다.\n"
                        "덮개를 열어 보니, 관측 장비와 각종 금속 부품, 그리고 별 모양 스티커가 붙은 작은 휴대폰 하나가 들어 있다."
                    ),
                ),
                # 풍향계 재료 지급
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.METAL_PIPE,
                        "description": "속이 빈 금속 파이프다. 세워 두면 기둥처럼 쓸 수 있지만, 바람이 강한 곳에서는 바닥 고정이 필요해 보인다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ROTATION_BRACKET,
                        "description": "회전축으로 쓸 수 있는 작은 브래킷이다. 헐거워 약간의 조임이 필요해 보인다.”",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ALUMINUM_PLATE,
                        "description": "얇은 알루미늄 판이다. 가공해서 꼬리 역할을 하게 만들 수 있다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.PLASTIC_ROD,
                        "description": "가벼운 플라스틱 막대다. 끝부분이 약간 비어 있어 작은 조각을 끼우면 앞쪽에 무게를 줄 수도 있을 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.BOLT_SET,
                        "description": "여러 개의 볼트와 너트가 들어 있는 작은 상자다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "obs_crate_opened", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 풍향계를 만들 수 있을 것 같습니다.",
                ),
            ],
        ),
        # ===========================================================
        # 3) 등반 장비 상자: 풍향계 + 바람 퍼즐 (코드는 나중에 교체)
        # ===========================================================
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.ASCENT_CRATE, "7421"],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="obs_crate_opened", value=True),
                Condition(type=ConditionType.STATE_IS, target="ascent_crate_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "풍향계를 통해 기록한 바람 패턴을 상자 옆 패널에 입력하자, "
                        "내부에서 하중이 풀리는 소리가 나며 잠금 장치가 열린다.\n"
                        "상자 안에는 등반용 도르래와 하네스가 가지런히 놓여 있다.\n"
                        "풍향계는 제 역할을 다 한 것 같다. 이제는 도르래를 조립하는 데 집중해야 한다."
                    ),
                ),
                # 풍향계 제거
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.WIND_VANE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.LARGE_PULLEY,
                        "description": "큰 도르래다. 바위 턱 같은 곳에 걸어 메인 도르래로 쓰기 좋지만, 제대로 쓰려면 단단히 고정할 필요가 있어 보인다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SMALL_PULLEY,
                        "description": "작은 보조 도르래다. 하네스 같은 장비에 달아 로프를 한 번 더 꺾어 주면, 몸을 끌어올릴 때 힘을 적게 쓸 수 있다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.HARNESS,
                        "description": "허리와 다리를 감싸는 등반용 하네스다. 로프만 매달면 몸이 한쪽으로 쏠리기 쉬워, 어딘가에 도르래 같은 보조 장치를 달아 주는 게 좋아 보인다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "ascent_crate_opened", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 도르래를 조립해 절벽을 올라갈 수 있을 것 같습니다.",
                ),
            ],
        ),
        # ==========================
        # 4) 풍향계 제작 (아이템 ↔ 아이템)
        # ==========================
        Combination(
            targets=[KeywordId.ALUMINUM_PLATE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ALUMINUM_PLATE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="알루미늄 판 가장자리를 소방 도끼로 잘라 깃 모양으로 다듬는다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.TRIMMED_TAIL_PLATE,
                        "description": "얇은 알루미늄 판을 깃 모양으로 다듬어 놓았다. 넓은 면적 덕분에 바람이 불면 뒤쪽에서 안정적으로 방향을 잡아 줄 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.ALUMINUM_PLATE,
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PLASTIC_ROD, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_ROD),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="플라스틱 막대 끝에 석영 조각을 달아 화살촉처럼 만든다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ARROW_HEAD,
                        "description": "플라스틱 막대 끝에 석영을 달아 만든 작은 화살 모양 조각이다. 바람을 받으면 앞쪽이 민감하게 돌아가도록 되어 있다.",
                    },
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.PLASTIC_ROD,
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.TRIMMED_TAIL_PLATE, KeywordId.ARROW_HEAD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.TRIMMED_TAIL_PLATE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ARROW_HEAD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="다듬은 꼬리판과 화살 헤드를 한 축에 맞춰 연결해 하나의 날개로 조립한다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WIND_VANE_WINGS,
                        "description": "앞쪽은 화살처럼 무게가 실려 있고, 뒤쪽은 넓은 꼬리판이 받쳐 주는 구조다. 바람을 받으면 자연스럽게 한쪽이 먼저 돌고, 다른 쪽이 뒤를 잡아준다.",
                    },
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.TRIMMED_TAIL_PLATE),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ARROW_HEAD),
            ],
        ),
        Combination(
            targets=[KeywordId.METAL_PIPE, KeywordId.BOLT_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BOLT_SET),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="금속 파이프를 단단히 고정할 수 있도록 볼트 위치를 맞춰 본다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WIND_VANE_POLE,
                        "description": "풍향계를 세우기 위한 기둥이다. 위에 무언가 회전하는 구조물을 올려두면 흔들리지 않을 것 같다.",
                    },
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ROTATION_BRACKET, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ROTATION_BRACKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="회전 브래킷의 볼트를 스패너로 조여, 헐거운 부분이 없도록 정리한다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.TIGHTENED_PIVOT,
                        "description": "헐거웠던 브래킷을 스패너로 조여 둔 회전축이다. 기둥 위에 올리면 바람에 흔들려도 매끄럽게 돌아갈 것 같다.",
                    },
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ROTATION_BRACKET),
            ],
        ),
        # =======================================
        # 5) 풍향계 설치 (아이템 ↔ 바위 턱, progress 0→3)
        # =======================================
        # 풍향계 기둥 + 회전축 → 회전 기둥 세트
        Combination(
            targets=[KeywordId.WIND_VANE_POLE, KeywordId.TIGHTENED_PIVOT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE_POLE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.TIGHTENED_PIVOT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "풍향계 기둥 상단에 조여진 회전축을 끼워 맞춘다.\n"
                        "몇 번 돌려 보니, 바람을 받아도 부드럽게 돌아갈 만큼 적당한 마찰만 남아 있다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.PIVOT_POLE_SET,
                        "description": "기둥 위에 회전축을 단단히 끼워 만든 구조물이다. 위에 날개를 꽂기만 하면 바람 방향을 읽을 수 있는 형태가 갖춰진다.",
                    },
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.WIND_VANE_POLE,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.TIGHTENED_PIVOT,
                ),
            ],
        ),
        # 회전 기둥 세트 + 풍향계 날개 → 풍향계 완성
        Combination(
            targets=[KeywordId.PIVOT_POLE_SET, KeywordId.WIND_VANE_WINGS],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PIVOT_POLE_SET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE_WINGS),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "조립해 둔 풍향계 날개를 회전축 끝에 끼워 넣는다.\n"
                        "숨을 들이쉬어 가볍게 내뱉자, 화살 부분이 바람을 따라 방향을 틀며 잔잔히 돌아간다.\n"
                        "이제 어디서든 세워 두기만 하면, 바람이 불어오는 방향을 바로 읽을 수 있을 것이다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WIND_VANE,
                        "description": "앞이 민감하고 뒤가 안정적인 날개가 회전축에 연결되어 있다. 바람이 부는 쪽을 향해 자연스럽게 돌아가는 완성된 풍향계다.",
                    },
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.PIVOT_POLE_SET,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.WIND_VANE_WINGS,
                ),
            ],
        ),
        # ====================================
        # 6) 도르래 제작 (아이템 ↔ 아이템)
        # ====================================
        Combination(
            targets=[KeywordId.CLIMBING_ROPE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="로프 끝을 도끼로 잘라 지저분한 부분을 정리하고, 단단한 매듭을 지을 수 있도록 만든다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ROPE_TIP_CUT,
                        "description": "끝이 깔끔하게 정리된 로프 쪽 부분이다. 도르래에 통과시키거나 바위 턱에 한 번 더 걸어 매기에 알맞다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={
                        "keyword": KeywordId.CLIMBING_ROPE,
                        "field": "description",
                        "value": "등반용 로프다. 사람 한 명쯤 매달려도 버틸 만큼 튼튼해 보인다. "
                                 "한쪽 끝은 도르래를 통과시키고, 나머지 부분은 몸과 바위에 고정해야 제대로 힘을 쓸 수 있다.",
                    },
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.HARNESS, KeywordId.SMALL_PULLEY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HARNESS),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SMALL_PULLEY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="하네스의 허리 부분에 작은 도르래를 달아, 몸쪽에 걸리는 보조 도르래 세트를 만든다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.HARNESS_SET,
                        "description": "작은 도르래가 달린 하네스 세트다. 로프를 통과시키기만 하면, 바위 턱에 걸어 둔 도르래와 연결되어 몸이 함께 끌려 올라갈 수 있다.",
                    },
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SMALL_PULLEY),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.HARNESS),
            ],
        ),
        Combination(
            targets=[KeywordId.LARGE_PULLEY, KeywordId.BOLT_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LARGE_PULLEY),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BOLT_SET),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="큰 도르래에 볼트를 끼워, 바위 턱에 걸어 고정할 수 있는 형태로 만든다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MOUNTABLE_PULLEY,
                        "description": "바위 턱에 바로 고정할 수 있도록 볼트까지 세팅해 둔 큰 도르래다. 이제 위치만 잡고 바위 턱에 걸어 주면 된다.",
                    },
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.LARGE_PULLEY),
            ],
        ),
        # ===========================================
        # 7) 도르래 설치 (아이템 ↔ 바위 턱, progress 0→5)
        # ===========================================
        # progress 0 → 1: 메인 도르래 설치
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.MOUNTABLE_PULLEY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MOUNTABLE_PULLEY),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="바위 턱 위에 큰 도르래를 올리고, 틈새에 볼트를 끼워 단단히 고정한다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_progress", "value": 1},
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.MOUNTABLE_PULLEY),
            ],
        ),
        # progress 1 → 2: 로프 통과
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.ROPE_TIP_CUT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ROPE_TIP_CUT),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="정리된 로프 끝을 도르래에 통과시켜, 위아래로 자유롭게 움직일 수 있도록 만든다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_progress", "value": 2},
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ROPE_TIP_CUT),
            ],
        ),
        # progress 2 → 3: 하네스 세트 설치
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.HARNESS_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HARNESS_SET),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="하네스 세트를 로프의 한쪽에 연결해, 몸을 매달 수 있는 구조를 만든다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_progress", "value": 3},
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.HARNESS_SET),
            ],
        ),
        # progress 3 → 4: 스패너로 전체 점검/조임
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=3),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="스패너로 각 연결부의 볼트를 다시 한 번 조여, 도르래와 로프가 흔들리지 않도록 고정한다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_progress", "value": 4},
                ),
            ],
        ),
        # progress 4 → 5: 로프 본체 연결 (완성)
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.CLIMBING_ROPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CLIMBING_ROPE),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=4),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "남은 로프 부분을 바위 아래쪽 고리에 한 번 더 감아 매고, "
                        "느슨함을 조절해 몸을 끌어올리기 좋은 장력으로 맞춘다.\n"
                        "이제 도르래를 이용해 절벽을 오를 준비가 끝났다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "pulley_progress", "value": 5},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "climb_ready", "value": True},
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CLIMBING_ROPE),
            ],
        ),
        # ===============================
        # 8) 무게추(돌 1~5) 퍼즐 (틀만)
        # ===============================
        # 예시: 바위 턱 + 돌 N → 가볍다/무겁다/딱 맞다 피드백 (정답 로직은 나중에 구현)
        # 여기서는 틀만 하나 넣어두고, 실제 조건/정답 조합은 나중에 네가 채우면 됨.
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.STONE_1],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_1),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="돌 1을 시험 삼아 평형추 접시 위에 매달아 본다. 아직은 어떤 느낌인지 가늠하기 어렵다.",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.STONE_1,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_1_used", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.STONE_2],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_2),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="돌 2를 접시에 걸어 본다. 도르래가 천천히 움직이긴 하지만, 아직은 어딘가 가볍게 느껴진다.",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.STONE_2,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_2_used", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.STONE_3],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_3),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="돌 3을 올려 두자, 도르래가 짧게 삐걱인 뒤 조용해진다.",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.STONE_3,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_3_used", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.STONE_4],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_4),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="돌 4를 매달자, 도르래가 조금 과하게 돌아가며 금속 마찰음이 길게 이어진다. ",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.STONE_4,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_4_used", "value": True},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PULLEY_ANCHOR, KeywordId.STONE_5],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_5),
                Condition(type=ConditionType.STATE_IS, target="pulley_progress", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="돌 5를 걸어 보자, 도르래가 크게 움직이는 것 처럼 보인다.",
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.STONE_5,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_5_used", "value": True},
                ),
            ],
        ),
        # ===========================
        # 돌무더기 + 소방 도끼 → 돌 1~5
        # ===========================
        # 1번째 타격 → 돌 1
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼로 돌무더기 옆을 세게 내려친다.\n"
                        "겉돌이 부서지며 안쪽에서 단단한 조각 하나가 굴러 나온다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.STONE_1,
                        "description": "손 안에 쏙 들어오는 작은 돌이다. 흔히 볼 수 있는 자갈처럼 보이지만 제법 단단하다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_pick_count", "value": 1},
                ),
            ],
        ),
        # 2번째 타격 → 돌 2
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("한 번 더 내려치자, 갈라진 틈 사이로 조금 더 묵직한 돌 조각이 떨어져 나온다."),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.STONE_2,
                        "description": "손에 쥐면 조금 묵직하게 느껴지는 돌이다. 표면이 단단해서 평형추로 쓰기 좋다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_pick_count", "value": 2},
                ),
            ],
        ),
        # 3번째 타격 → 돌 3
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("도끼날이 깊숙이 파고들면서, 매끈한 표면을 가진 중간 크기의 돌이 하나 튀어나온다."),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.STONE_3,
                        "description": "표면이 매끈한 돌이다. 크기에 비해 묵직한 편이라 감이 독특하다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_pick_count", "value": 3},
                ),
            ],
        ),
        # 4번째 타격 → 돌 4
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=3),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("이번에는 도끼로 가장자리 부분을 잘라내자, 손바닥만 한 크기의 돌이 통째로 떨어져 나온다."),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.STONE_4,
                        "description": "손바닥을 가득 채우는 크기의 돌이다. 모서리가 적당히 둥글다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_pick_count", "value": 4},
                ),
            ],
        ),
        # 5번째 타격 → 돌 5
        Combination(
            targets=[KeywordId.STONE_PILE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="stone_pick_count", value=4),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("마지막으로 깊게 찍어내자, 다른 것들보다 더 크고 묵직한 돌 조각이 느리게 굴러 나온다."),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.STONE_5,
                        "description": "다섯 개 중 가장 큰 돌이다. 평형추로 쓰기 딱 좋아 보인다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "stone_pick_count", "value": 5},
                ),
            ],
        ),
        # 장비 상자 + 스패너 → 금속 명판 떼어내기
        Combination(
            targets=[KeywordId.EQUIPMENT_BUNDLE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="gear_crate_opened", value=False),
                Condition(type=ConditionType.STATE_IS, target="gear_nameplate_detached", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너로 장비 상자 안쪽 금속판을 고정하고 있던 나사를 하나씩 풀어낸다.\n"
                        "마지막 나사를 빼자, 금속판이 '톡' 하고 떨어져 손바닥 위에 내려앉는다.\n"
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.EQUIPMENT_NAMEPLATE,
                        "description": "장비 상자 안쪽에 붙어 있던 금속 명판이다. 한쪽 면에 '1699'라는 숫자가 적혀 있었다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gear_nameplate_detached", "value": True},
                ),
            ],
        ),
        # ============================================
        # 풍향계 + 바람 관측 로그 (wind_log_step 0 → 1 → 2 → 3 → 4 → 1 …)
        # ============================================
        # 0단계: 서풍(W) → 북동풍(NE)
        Combination(
            targets=[KeywordId.CLIFF_WIND, KeywordId.WIND_VANE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE),
                Condition(type=ConditionType.STATE_IS, target="wind_log_step", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "풍향계 화살이 먼저 서쪽에서 밀려오는 바람을 가리킨다(W).\n"
                        "잠시 뒤 바람결이 바뀌며 화살이 북동쪽을 향해 천천히 돌아선다(NE).\n"
                        "오늘 바람은 생각보다 예민하게 방향을 틀고 있는 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wind_log_step", "value": 1},
                ),
            ],
        ),
        # 1단계: 남풍(S) → 북동풍(NE) → 서풍(W)
        Combination(
            targets=[KeywordId.CLIFF_WIND, KeywordId.WIND_VANE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE),
                Condition(type=ConditionType.STATE_IS, target="wind_log_step", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "이번에는 바람이 남쪽에서 먼저 가볍게 불어온다(S).\n"
                        "풍향계가 흔들리다가 어느 순간 북동풍 쪽으로 방향을 바꾸고(NE),\n"
                        "마지막에는 다시 서쪽에서 부는 바람이 화살을 밀어낸다(W)."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wind_log_step", "value": 2},
                ),
            ],
        ),
        # 2단계: 서풍(W) → 북동풍(NE) → 서풍(W)
        Combination(
            targets=[KeywordId.CLIFF_WIND, KeywordId.WIND_VANE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE),
                Condition(type=ConditionType.STATE_IS, target="wind_log_step", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "서풍이 강하게 불어와 화살을 서쪽으로 밀어낸다(W).\n"
                        "곧이어 바람이 고개를 틀듯 북동쪽으로 방향을 바꾸더니(NE),\n"
                        "잠시 후 다시 처음처럼 서풍이 돌아와 화살을 원래 자리로 데려다 놓는다(W).\n"
                        "짧은 순간 안에 바람이 세 번이나 방향을 튼 셈이다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wind_log_step", "value": 3},
                ),
            ],
        ),
        # 3단계: 북풍(N)
        Combination(
            targets=[KeywordId.CLIFF_WIND, KeywordId.WIND_VANE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE),
                Condition(type=ConditionType.STATE_IS, target="wind_log_step", value=3),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "풍향계는 한동안 움직이지 않더니, 이내 북쪽을 곧게 가리킨 채 멈춰 선다(N).\n"
                        "바람은 일정하게 머리 위를 스쳐 지나가고, 방향이 바뀔 기미는 보이지 않는다.\n"
                        "오히려 이렇게 한 방향으로 고정된 바람이 더 불길하게 느껴진다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wind_log_step", "value": 4},
                ),
            ],
        ),
        # 4단계: 서풍(W) → 북동풍(NE), 이후 다시 1단계로 루프
        Combination(
            targets=[KeywordId.CLIFF_WIND, KeywordId.WIND_VANE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIND_VANE),
                Condition(type=ConditionType.STATE_IS, target="wind_log_step", value=4),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "서쪽에서 불어온 바람이 잠시 풍향계를 서쪽으로 밀어낸다(W).\n"
                        "그러다 어느 순간 기류가 갈라지듯 방향을 꺾어, 화살이 다시 북동쪽을 향해 돌아선다(NE).\n"
                        "아까와 비슷한 패턴이 반복되는 것으로 보인다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wind_log_step", "value": 1},
                ),
            ],
        ),
    ],
)
