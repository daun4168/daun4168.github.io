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

CH1_SCENE9_DATA = SceneData(
    id=SceneID.CH1_SCENE9,
    name="가파른 능선 꼭대기 (섬 정상)",
    body=(
        "절벽을 따라 도르래에 몸을 맡기고 천천히 올라가자, "
        "시야가 순식간에 넓어지며 능선 위가 모습을 드러낸다.\n"
        "발밑에는 오래전부터 쓰이던 듯한 좁은 콘크리트 기단이 있고, "
        "그 위로는 녹슨 볼트와 부러진 금속 파이프 조각들이 흩어져 있다.\n"
        "조금 떨어진 바위 그늘 아래에는, 흙에 반쯤 묻힌 작은 금속 상자가 보인다. "
        "누군가가 서둘러 숨겨 놓고 떠난 흔적처럼, 뚜껑 틈으로 낡은 전선 뭉치가 살짝 비친다.\n\n"
        "바람이 쉴 새 없이 머리 위를 훑고 지나가며, "
        "이곳이 한때 안테나나 관측 장비를 세워 두던 자리였다는 사실을 조용히 말해 주는 듯하다."
    ),
    initial_state={
        "antenna_build_step": 0,  # 0~9 : 파이프→볼트→스패너 × 3회
        "antenna_built": False,  # 안테나 기계 구조 완성 여부
        "antenna_puzzle_solved": False,  # 안테나 퍼즐 해결 여부
        "antenna_wire_connected": False,  # 긴 전선을 안테나에 연결했는지 여부
        "cliff_down_path_inspected": False,  # 절벽 아래로 내려가는 길을 살펴봤는지
        "wire_crate_opened": False,  # 전선 상자를 연 적 있는지
    },
    keywords={
        KeywordId.WIRE_CRATE_ALIAS1: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WIRE_CRATE),
        KeywordId.WIRE_CRATE_ALIAS2: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WIRE_CRATE),
        # 절벽 아래(관측소 기단)로 내려가는 길
        KeywordId.CLIFF_FACE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,  # 처음부터 보이도록
            description=None,
            interactions=[
                # 처음 내려가는 길을 살펴볼 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="cliff_down_path_inspected",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "능선 가장자리에서는 절벽 아래 협곡으로 이어지는 가파른 경사로가 내려다보인다.\n"
                                "곳곳에 박힌 바위 턱과 잡초 뿌리를 손잡이 삼으면, 조심스럽게 내려가 아래 기단과 장비 쪽으로 돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "cliff_down_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 이미 길을 확인한 뒤, 실제로 내려갈지 선택
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="cliff_down_path_inspected",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "절벽 아래 협곡(관측소 아래 기단)으로 내려가시겠습니까?\n"
                                    "내려갔다가 다시 이 능선으로 돌아오면 **체력이 2 소모**됩니다."
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 바위 턱과 잡초 뿌리를 하나씩 짚으며, 조심스럽게 절벽 아래로 내려간다.\n"
                                            "잠시 후, 익숙한 장비와 기단이 보이는 지점에 발을 디딘다."
                                        ),
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
                                        type=ActionType.PRINT_SYSTEM,
                                        value="아직 능선 위에서 확인해야 할 것들이 남아 있는 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 안테나 기단(골조를 세우는 자리)
        KeywordId.ANTENNA_MOUNT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "능선 중앙에는 좁은 콘크리트 기단이 있다. 네 귀퉁이에 녹슨 볼트 자국이 남아 있고,\n"
                "가운데에는 끊어진 금속 파이프 조각이 비스듬히 튀어나와 있다.\n"
                "주변을 둘러보니, 누군가 새로 가져온 금속 파이프 묶음과 볼트 상자, 스패너가 어지럽게 놓여 있다."
            ),
            interactions=[
                # step 0: 완전 작업 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=0,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기단 위에 남아 있는 자국들로 보아, 이곳에는 원래 길쭉한 안테나 기둥이 세워져 있었던 것 같다.\n"
                                "지금은 뿌리만 남아 있어, 새 파이프를 이어 붙이고 볼트로 고정한 뒤 스패너로 조여야 다시 세울 수 있을 듯하다.\n"
                                "한 번에 끝날 작업은 아니고, 같은 작업을 몇 번이고 반복해서 기둥을 원하는 높이까지 올려야 할 것 같다."
                            ),
                        )
                    ],
                ),
                # step 1: 첫 파이프만 올려둔 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=1,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기단 중앙에 첫 번째 금속 파이프가 세워져 있다. 아직 볼트로 고정하지 않아,\n"
                                "손으로 살짝 밀어 보기만 해도 흔들리며 위태롭게 앞뒤로 기울어진다."
                            ),
                        )
                    ],
                ),
                # step 2: 볼트는 끼웠지만 조이기 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=2,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "첫 번째 파이프와 기단을 가로지르는 볼트가 끼워져 있어, 아까보다는 훨씬 덜 흔들린다.\n"
                                "하지만 너트는 아직 느슨하게 남아 있어, 스패너로 단단히 조여 주어야 진짜 기둥 역할을 할 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # step 3: 첫 구간 완전히 고정
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=3,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "첫 번째 파이프는 이제 기단에 단단히 고정되어, 손으로 힘껏 밀어도 거의 움직이지 않는다.\n"
                                "기둥 높이는 아직 허리께 정도에 불과하지만, 그 위로 같은 작업을 몇 번 더 반복하면 "
                                "꽤 쓸 만한 안테나를 세울 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # step 4: 두 번째 파이프를 올려둔 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=4,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "첫 번째 파이프 위에 두 번째 파이프가 덧대어져 있다. 이음새는 아직 임시로 끼워 둔 수준이라,\n"
                                "세로로는 꽤 높아졌지만, 옆에서 보면 미묘하게 뒤틀린 것처럼 보인다."
                            ),
                        )
                    ],
                ),
                # step 5: 두 번째 구간 볼트까지 끼운 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=5,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "두 번째 파이프와 첫 번째 파이프를 관통하는 볼트가 이음새를 붙잡고 있다.\n"
                                "아직 너트를 꽉 조인 건 아니라, 손으로 잡아 당기면 미세하게 돌아가는 느낌이 남아 있다."
                            ),
                        )
                    ],
                ),
                # step 6: 두 번째 구간까지 완전히 고정
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=6,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "두 번째 이음새까지 단단히 조여져, 기둥은 이제 어깨를 훌쩍 넘는 높이까지 자라났다.\n"
                                "바람이 불 때마다 기둥이 살짝 휘어지긴 하지만, 뿌리와 이음새는 꽤 믿음직스럽다.\n"
                                "이 위에 마지막 파이프를 한 번 더 올리면, 본격적인 안테나 기둥으로 쓸 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # step 7: 세 번째 파이프를 올려둔 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=7,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "가장 긴 마지막 파이프가 기둥 맨 위에 이어져 있다. 전체 기둥은 이미 능선의 바람을 정면으로 맞으며 흔들리고 있다.\n"
                                "하지만 최상단 이음새는 아직 임시로 얹어 둔 수준이라, 지금 상태로 바람을 오래 맞게 두기엔 다소 불안해 보인다."
                            ),
                        )
                    ],
                ),
                # step 8: 최상단 볼트까지 끼웠지만 아직 조이기 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_build_step",
                            value=8,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "세 번째 파이프와 그 아래 파이프를 잇는 볼트가 이음새를 관통하고 있다.\n"
                                "기둥은 거의 완성된 모양새지만, 마지막 너트가 아직 느슨하게 남아 있어 바람을 탈 때마다 상단이 미세하게 떨린다.\n"
                                "스패너로 이 부분만 단단히 조여 주면, 제대로 된 안테나 기둥이 완성될 것이다."
                            ),
                        )
                    ],
                ),
                # 안테나 완성 후: 기단만 남은 느낌
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_built",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기단 위에는 이미 길쭉한 안테나가 곧게 서 있다.\n"
                                "이제는 기단이 아니라, 완성된 안테나 자체를 살펴보는 편이 좋을 것 같다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # 완성된 안테나 본체
        KeywordId.ANTENNA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # 완성 전에는 보이지 않음
            description=(
                "여러 겹의 금속 파이프를 이어 붙여 세운 안테나다.\n"
                "능선 위 바람을 곧게 가르며 서 있고, 기단 옆 콘솔에는 희미한 눈금과 스위치들이 남아 있다."
            ),
            interactions=[
                # 안테나 완성, 퍼즐은 아직
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_built",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_puzzle_solved",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "여러 겹의 금속 파이프를 이어 붙인 안테나 기둥이 능선 위를 가늘게 가르고 서 있다.\n"
                                "기단 옆 콘솔에는 희미한 눈금과 스위치들 사이로, 작은 숫자 표시창이 깜빡이고 있다.\n"
                                "마치 이 섬에 도착한 이후 당신이 내린 모든 선택과 움직임을 하나씩 세어 온 듯, 숫자는 조용히 어떤 값을 가리키고 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`안테나 : [숫자]` 형식으로 입력해 보세요.\n",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=(
                                "이 섬에서 지나온 선택들이, 이제 하나의 숫자로 이어지고 있습니다.\n\n"
                                "떠올려 보세요. 몇 번을 고민하고, 결심하고, 다시 움직였는지.\n\n"
                                "그리고 기억하세요. 지금 입력하려는 그 순간도… 선택의 수를 하나 더 늘립니다."
                            ),
                        ),
                    ],
                ),
                # 퍼즐은 풀었지만 전선을 아직 안 연결한 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_built",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_puzzle_solved",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_wire_connected",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "안테나는 이제 안정적으로 서 있고, 콘솔의 지시등도 규칙적인 간격으로 점멸하고 있다.\n"
                                "이제 남은 건, 기다란 전선을 안테나 하단 단자에 연결해 신호를 아래 MK-II까지 끌어내리는 일뿐이다.\n"
                                "전선 한쪽 끝을 여기 단자에 고정하면, 다른 쪽 끝만 손에 쥔 채 절벽 아래로 내려갈 수 있을 것 같다."
                            ),
                        ),
                    ],
                ),
                # 퍼즐 + 전선까지 모두 끝난 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_built",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_puzzle_solved",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="antenna_wire_connected",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "안테나는 바람을 가르며 묵묵히 서 있고, 긴 전선은 기단 옆을 따라 절벽 아래로 흘러내린다.\n"
                                "손에는 전선의 다른 끝이 남아 있다. 이제 MK-II로 돌아가 이 끝을 연결하기만 하면 된다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 누군가가 남겨 둔 듯한 전선 상자
        KeywordId.WIRE_CRATE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "능선 한쪽 바위 그늘 아래, 작은 금속 상자가 반쯤 흙에 묻혀 있다.\n"
                "녹슨 자물쇠와 찌그러진 뚜껑 사이로, 안쪽에 감겨 있는 전선 뭉치가 어렴풋이 보인다."
            ),
            interactions=[
                # 아직 상자를 열지 않은 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="wire_crate_opened",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "상자를 가까이 들여다보니, 내부에 꽤 긴 전선이 정갈하게 감겨 있다.\n"
                                "마치 누가 나중에 올 사람을 알고, 일부러 여기 숨겨 두고 간 비상용 장비처럼 보인다.\n"
                                "뚜껑은 찌그러져 손으로는 열기 힘들다. 단단한 도끼 같은 것이 있다면 비틀어 벌릴 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # 이미 한 번 열어본 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="wire_crate_opened",
                            value=True,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "뚜껑이 벌어진 상자 안에는 잘려 나간 전선 조각들과, 빈 케이블 드럼만 덩그러니 남아 있다.\n"
                                "누군가를 위해 남겨져 있던 길다란 전선은 이제 당신 손으로 옮겨졌다."
                            ),
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # --- 첫 번째 사이클: step 0 → 1 → 2 → 3 ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "교수님이 ‘이건 논문이 아니다’라며 원고를 밀어내던 그 표정이 떠오른다.\n\n"
                        "그날은 모든 문이 닫힌 것 같았지만, 지금은 이 파이프 하나라도 세우면 어딘가로 통할 것 같은 기분이다.\n\n"
                        "첫 파이프를 기단에 끼워 넣자, 능선 위 바람 속에 아주 작은 가능성이 섞인다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 1},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.BOLT_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BOLT_SET),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "제 2 연구실에서 쓰레기통을 뒤지고, 랩 가운 주머니를 털고, "
                        "열쇠로 청소도구함을 열어 겨우 빗자루 하나를 꺼냈던 일이 떠오른다.\n\n"
                        "바닥 한 번 쓸려면 그 정도 삽질은 해야 굴러가는 곳이었다.\n\n"
                        "볼트를 끼우자, 금속 기둥이 막 청소 끝낸 바닥처럼 비로소 단정한 자세를 잡기 시작한다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 2},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너로 MK-II 해치를 조이던 순간이 떠오른다. 그 한 바퀴로 연구실에서 이 섬까지, 인생 궤도가 통째로 틀어졌다.\n\n"
                        "그래도 조여야 할 때는 조여야 했다. 그때도, 지금도.\n\n"
                        "스패너가 딸칵 소리를 내며 멈추자, 첫 기둥이 기단에 제대로 뿌리를 내린다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 3},
                ),
            ],
        ),
        # --- 두 번째 사이클: step 3 → 4 → 5 → 6 ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=3),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "늪에서 양동이를 굴려 독가스를 만들고, 공명하는 숲에서 꽃무늬와 새소리를 맞춰 길을 열던 순간들이 차례로 떠오른다.\n\n"
                        "그때는 냄새와 소리를 다루었다면, 지금은 금속과 높이를 다루는 중이다.\n\n"
                        "두 번째 파이프를 얹자, 기둥은 숲의 나무들보다 훨씬 높이 솟구친다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 4},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.BOLT_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BOLT_SET),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=4),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석회 패널의 순서를 맞춰 문을 열고, 눈앞에 새로운 길이 펼쳐지던 그 조용한 순간이 떠오른다.\n\n"
                        "여기서도 마찬가지로, 제자리에 꽂힌 하나가 전체를 안정시킨다.\n\n"
                        "볼트를 끼우자 삐걱거리던 이음새가 잠잠해지고, 기둥은 다시 중심을 찾는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 5},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=5),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "난파선에서 문이 터져 나가고, 황산을 부어 숨겨진 금속 결을 드러내던 순간이 스쳐 간다.\n\n"
                        "그때는 금속을 녹여 길을 열었다면, 지금은 그 금속을 붙잡아 세워야 하는 자리다.\n\n"
                        "스패너를 천천히 돌리자 두 번째 구간이 맞물리고, 기둥은 거친 파도 대신 산바람을 버틸 준비를 마친 돛대처럼 느껴진다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 6},
                ),
            ],
        ),
        # --- 세 번째 사이클: step 6 → 7 → 8 → 9 ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=6),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "지하 호수에서 코일과 자철석을 맞추며 물 위로 번지던 희미한 불빛을 바라보던 장면이 떠오른다.\n\n"
                        "그 빛이 이 기둥을 따라 다시 위로 흘러오는 것 같다.\n\n"
                        "마지막 긴 파이프가 이어지자, 안테나는 처음으로 ‘하늘을 향한 선’ 같은 모양을 갖춘다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 7},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.BOLT_SET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BOLT_SET),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=7),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "절벽 아래에서 돌 다섯 개로 평형추를 맞추고, 능선 위에 풍향계를 세워 바람의 방향을 읽어내던 순간이 떠오른다.\n\n"
                        "이제 그 바람이 이 안테나를 흔들겠지만, 쓰러뜨리지는 못하게 할 차례다.\n\n"
                        "최상단에 볼트를 끼우자, 기둥은 세찬 바람에도 꺾이지 않을 듯한 표정을 짓는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 8},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=8),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "이 스패너는 참 많이 돌았다. 연구실 해치에서도, 풍향계 축에서도, 도르래와 난파선 문에서도.\n\n"
                        "섬을 한 바퀴 도는 동안 ‘조여야 할 것들’을 묵묵히 정리해 준 건 언제나 이 금속 막대였다.\n\n"
                        "이번에도 한 바퀴, 또 한 바퀴 돌리자 금속이 끝까지 물리는 감각이 손끝에 또렷하다.\n\n"
                        "안테나 기둥은 바람을 가르는 선으로 곧게 선다. 거의 다 왔다.\n\n"
                        "이제 남은 건, 이 작은 신호를 MK-II까지 이어 주는 일뿐이다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 9},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_built", "value": True},
                ),
                # 안테나가 완성되는 순간 ANTTENA 키워드를 활성화
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.ANTENNA, "state": KeywordState.DISCOVERED},
                ),
                # 재료 소진
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.METAL_PIPE,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.BOLT_SET,
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="금속 파이프 묶음과 볼트를 모두 사용해 안테나 기둥을 완성했습니다.",
                ),
            ],
        ),
        # =======================================
        # 안테나 퍼즐 (placeholder)
        #  - 실제 정답은 '행동 수'를 기반으로 바뀔 예정이지만,
        #    현재는 0000 등 정해진 값으로 테스트할 수 있다.
        # =======================================
        Combination(
            type=CombinationType.PASSWORD_CH1_FINAL,
            targets=[KeywordId.ANTENNA, "eq"],  # 임시 정답
            conditions=[
                Condition(
                    type=ConditionType.STATE_IS,
                    target="antenna_built",
                    value=True,
                ),
                Condition(
                    type=ConditionType.STATE_IS,
                    target="antenna_puzzle_solved",
                    value=False,
                ),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "숫자를 입력하자, 콘솔의 작은 표시창이 잠시 숨을 고르듯 깜빡이더니 조용히 멈춘다.\n\n"
                        "다이얼과 스위치 주변의 미세한 떨림이 가라앉고, 안테나 기둥 어딘가에서 낮은 공명음이 길게 울려 퍼진다.\n\n"
                        "이 섬에 발을 디딘 뒤로 당신이 쌓아 올린 모든 선택들이, 이제 하나의 신호로 정리되어 하늘을 향해 뻗어 나가는 듯하다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_puzzle_solved", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "안테나 설정이 안정되었습니다.\n\n"
                        "이제 기다란 전선을 연결해, 여기서 만들어 낸 신호를 MK-II까지 이어 보낼 수 있을 것 같습니다."
                    ),
                ),
            ],
        ),
        # 정답일 때
        Combination(
            type=CombinationType.PASSWORD_CH1_FINAL,
            targets=[KeywordId.ANTENNA, "eq"],  # 임시 정답
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "숫자를 입력하자, 콘솔의 작은 표시창이 잠시 숨을 고르듯 깜빡이더니 조용히 멈춘다.\n\n"
                        "다이얼과 스위치 주변의 미세한 떨림이 가라앉고, 안테나 기둥 어딘가에서 낮은 공명음이 길게 울려 퍼진다.\n\n"
                        "이 섬에 발을 디딘 뒤로 쌓아 올린 모든 선택들이, 이제 하나의 신호로 정리되어 하늘을 향해 뻗어 나가는 듯하다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_puzzle_solved", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "안테나 설정이 안정되었습니다.\n\n"
                        "이제 기다란 전선을 연결해, 여기서 만들어 낸 신호를 MK-II까지 이어 보낼 수 있을 것 같습니다."
                    ),
                ),
            ],
        ),
        # 사용자가 '정답보다 작은 숫자'를 입력했을 때 (lt)
        Combination(
            type=CombinationType.PASSWORD_CH1_FINAL,
            targets=[KeywordId.ANTENNA, "lt"],  # 임시 정답
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "입력한 숫자가 콘솔에 찍히자, 표시창이 한 번 깜빡이고는 금세 힘을 잃은 듯 어둡게 가라앉는다.\n\n"
                        "안테나 기둥도 잠깐 떨렸다가, 이내 아무 일도 없었다는 듯 고요해진다.\n\n"
                        "이 숫자로는 아직, 이 섬에서 걸어온 발자국들을 다 셀 수 없는 모양이다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "조금 더 많은 선택을 떠올려 보세요.\n\n"
                        "당신이 생각하는 것보다, 이곳에서 이미 더 멀리 와 있을지도 모릅니다."
                    ),
                ),
            ],
        ),
        # 사용자가 '정답보다 큰 숫자'를 입력했을 때 (gt)
        Combination(
            type=CombinationType.PASSWORD_CH1_FINAL,
            targets=[KeywordId.ANTENNA, "gt"],  # 임시 정답
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "숫자를 입력하자, 표시창의 숫자들이 잠시 과열된 듯 빠르게 요동치다가 원래 자리로 되돌아온다.\n\n"
                        "안테나 기둥에서도 불안정한 잡음이 몇 번 튀어나오다가 금세 끊긴다.\n\n"
                        "이 정도 숫자는, 아직 밟지 않은 발자국까지 미리 더해 버린 셈인지도 모른다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=("조금 덜 앞서 나가도 괜찮습니다.\n\n지금까지의 선택들만, 정확히 세어 보세요."),
                ),
            ],
        ),
        # =======================================
        # 안테나에 기다란 전선 연결
        # =======================================
        Combination(
            targets=[KeywordId.ANTENNA, KeywordId.LONG_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LONG_WIRE),
                Condition(
                    type=ConditionType.STATE_IS,
                    target="antenna_puzzle_solved",
                    value=True,
                ),
                Condition(
                    type=ConditionType.STATE_IS,
                    target="antenna_wire_connected",
                    value=False,
                ),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "기다란 전선 한쪽 끝의 피복을 벗겨 안테나 기둥 하단 단자에 감아 매고, 단단히 고정한다.\n"
                        "이제 다른 쪽 끝만 손에 남는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_wire_connected", "value": True},
                ),
                # 기존 전선 아이템 제거
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.LONG_WIRE,
                ),
                # MK-II에 연결하기 위한 '남은 전선 끝' 아이템 지급
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.LONG_WIRE_FREE_END,
                        "description": (
                            "한쪽 끝은 능선 위 안테나에 고정되어 있고, 다른 쪽 끝만 손에 남아 있는 긴 전선이다.\n"
                            "MK-II 단자에 연결할 수 있을 것 같다."
                        ),
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 MK-II로 내려가, 남은 전선 끝을 단자에 연결할 수 있습니다.",
                ),
            ],
        ),
        # =======================================
        # 감춰진 전선 상자 + 소방 도끼 → 기다란 전선 획득
        # =======================================
        Combination(
            targets=[KeywordId.WIRE_CRATE, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(
                    type=ConditionType.STATE_IS,
                    target="wire_crate_opened",
                    value=False,
                ),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼의 날을 상자 틈에 비스듬히 밀어 넣고, 힘껏 비튼다.\n"
                        "찌그러진 뚜껑이 끌려 올라가며 녹슨 자물쇠가 부서지고, 안쪽에 감겨 있던 긴 전선이 모습을 드러낸다.\n"
                        "누군가가 언젠가 이곳까지 올라올 사람을 알았다는 듯, 딱 한 번 쓸 만큼의 여분이 남겨져 있었다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.LONG_WIRE,
                        "description": (
                            "능선 위 상자에서 꺼낸 기다란 전선이다.\n"
                            "한쪽 끝은 안테나에, 다른 한쪽 끝은 MK-II에 연결해 신호를 전달할 수 있을 것 같다."
                        ),
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "wire_crate_opened", "value": True},
                ),
            ],
        ),
    ],
)
