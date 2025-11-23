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
    initial_text=(
        "절벽을 따라 도르래에 몸을 맡기고 천천히 올라가자, 시야가 순식간에 넓어지며 능선 위가 모습을 드러낸다.\n"
        "발밑에는 오래전부터 쓰이던 듯한 좁은 콘크리트 기단이 있고, 그 위로는 녹슨 볼트와 부러진 금속 파이프 조각들이 흩어져 있다.\n\n"
        "바람이 쉴 새 없이 머리 위를 훑고 지나가며, 이곳이 한때 안테나나 관측 장비를 세워 두던 자리였다는 사실을 조용히 말해 주는 듯하다."
    ),
    initial_state={
        "antenna_build_step": 0,  # 0~9 : 파이프→볼트→스패너 × 3회
        "antenna_built": False,  # 안테나 기계 구조 완성 여부
        "antenna_puzzle_solved": False,  # 안테나 관련 퍼즐 해결 여부
        "antenna_wire_connected": False,  # 긴 전선을 안테나에 연결했는지 여부
    },
    keywords={
        KeywordId.CLIFF_FACE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,  # 처음부터 보이도록
            description=None,
            interactions=[
                # 처음 내려가는 길을 살펴볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="cliff_down_path_inspected", value=False),
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
                        Condition(type=ConditionType.STATE_IS, target="cliff_down_path_inspected", value=True),
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
                                        value=SceneID.CH1_SCENE8,  # 절벽 아래(MK-II 근처) 씬으로 이동
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
        # 이 씬에서 보이는 오브젝트는 이 하나뿐
        KeywordId.ANTENNA_MOUNT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "능선 중앙에는 좁은 콘크리트 기단이 있다. 네 귀퉁이에 녹슨 볼트 자국이 남아 있고,\n"
                "가운데에는 끊어진 금속 파이프 조각이 비스듬히 튀어나와 있다.\n"
                "주변을 둘러보니, 누군가 새로 가져온 금속 파이프 묶음과 볼트 상자, 스패너가 어지럽게 놓여 있다."
            ),
            interactions=[
                # step 0: 완전 작업 전
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=0),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=1),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=2),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=3),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "첫 번째 파이프는 이제 기단에 단단히 고정되어, 손으로 힘껏 밀어도 거의 움직이지 않는다.\n"
                                "기둥 높이는 아직 허리께 정도에 불과하지만, 그 위로 같은 작업을 몇 번 더 반복하면 꽤 쓸 만한 안테나가 될 것 같다."
                            ),
                        )
                    ],
                ),
                # step 4: 두 번째 파이프를 올려둔 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=4),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=5),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=6),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=7),
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
                        Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=8),
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
                # 안테나가 완성되었지만, 퍼즐은 아직: 퍼즐 힌트 및 안내 (placeholder)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "여러 겹의 금속 파이프를 이어 붙인 안테나 기둥이 능선 위를 가늘게 가르고 서 있다.\n"
                                "기단 옆 콘솔에는 희미하게 남아 있는 눈금과 몇 개의 스위치, 다이얼이 있다.\n"
                                "어떤 패턴으로 스위치를 눌러야, 이 안테나가 제대로 외부와 통신을 시작할 수 있을까?"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="(placeholder) `안테나 : [퍼즐 정답]` 형태로 값을 입력해 퍼즐을 푸는 구조로 사용할 수 있습니다.",
                        ),
                    ],
                ),
                # 안테나 + 퍼즐까지 해결, 아직 전선을 안 연결한 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=True),
                        Condition(type=ConditionType.STATE_IS, target="antenna_wire_connected", value=False),
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
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="기다란 전선을 안테나에 연결하려면, `안테나 기단 + 기다란 전선` 조합을 사용하세요.",
                        ),
                    ],
                ),
                # 모든 작업 완료 후
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=True),
                        Condition(type=ConditionType.STATE_IS, target="antenna_wire_connected", value=True),
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
    },
    combinations=[
        # =======================================
        # 1) 안테나 조립: 파이프 → 볼트 → 스패너 × 3회
        # antenna_build_step: 0~9
        #   0,3,6: 금속 파이프 묶음 사용
        #   1,4,7: 볼트 세트 사용
        #   2,5,8: 스패너 사용
        #   9: 안테나 완성 (antenna_built=True)
        # =======================================
        # --- 첫 번째 사이클: step 0 → 1 → 2 → 3 ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE_BUNDLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE_BUNDLE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="금속 파이프 묶음에서 가장 곧은 파이프를 골라 기단 중앙의 옛 기둥 자리에 맞춰 끼워 넣는다.",
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
                    value="볼트 상자에서 적당한 길이의 볼트를 꺼내, 파이프와 기단을 관통하도록 끼워 넣는다.",
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
                    value="스패너를 이용해 볼트를 조여, 첫 번째 파이프를 기단에 단단히 고정한다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 3},
                ),
            ],
        ),
        # --- 두 번째 사이클: step 3 → 4 → 5 → 6 ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE_BUNDLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE_BUNDLE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=3),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="두 번째 금속 파이프를 첫 번째 파이프 위에 이어 붙여, 기둥을 한 마디 더 높인다.",
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
                    value="이어 붙인 부분에 볼트를 끼워 넣어, 두 파이프가 어긋나지 않도록 중심을 잡는다.",
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
                    value="스패너로 볼트를 하나씩 조여 주자, 두 파이프가 하나의 기둥처럼 단단하게 이어진다.",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_build_step", "value": 6},
                ),
            ],
        ),
        # --- 세 번째 사이클: step 6 → 7 → 8 → 9 (완성) ---
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.METAL_PIPE_BUNDLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.METAL_PIPE_BUNDLE),
                Condition(type=ConditionType.STATE_IS, target="antenna_build_step", value=6),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="금속 파이프 묶음에서 마지막 남은 가장 긴 파이프를 골라 기둥 맨 위에 이어 붙인다.",
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
                    value="볼트 상자에서 남은 볼트들을 긁어모아, 마지막 이음새를 단단히 고정한다.",
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
                        "스패너를 끝까지 돌려 마지막 볼트를 조여 주자, 긴 안테나 기둥이 미세하게 떨리다 곧 곧게 서서 바람을 가른다.\n"
                        "금속 파이프 묶음과 볼트 상자는 이제 텅 비어, 더 이상 쓸 수 있는 조각이 남지 않았다."
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
                # 세 번 사용 후 파이프 묶음과 볼트는 사라짐
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.METAL_PIPE_BUNDLE,
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
        # 2) 안테나 퍼즐 (placeholder)
        #    - 퍼즐 로직은 나중에 교체 가능
        # =======================================
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.ANTENNA_MOUNT, "0000"],  # 임시 정답
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="antenna_built", value=True),
                Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "콘솔의 다이얼과 스위치를 조심스럽게 조작하자, 안테나 기둥 어딘가에서 미세한 공명음이 들려온다.\n"
                        "잠시 후 지시등이 일정한 간격으로 점멸하며, 통신 회선이 안정적으로 열린 것 같은 느낌이 든다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_puzzle_solved", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="(placeholder) 안테나 퍼즐이 해결되었습니다. 이제 긴 전선을 연결할 수 있습니다.",
                ),
            ],
        ),
        # =======================================
        # 3) 안테나에 기다란 전선 연결
        #    - 긴 전선 아이템은 다른 씬에서 획득했다고 가정
        # =======================================
        Combination(
            targets=[KeywordId.ANTENNA_MOUNT, KeywordId.LONG_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LONG_WIRE),
                Condition(type=ConditionType.STATE_IS, target="antenna_puzzle_solved", value=True),
                Condition(type=ConditionType.STATE_IS, target="antenna_wire_connected", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "기다란 전선 한쪽 끝의 피복을 벗겨 안테나 기둥 하단 단자에 감아 매고, 단단히 고정한다.\n"
                        "전선은 능선 가장자리를 따라 절벽 아래로 흘러내리고, 다른 쪽 끝만 손에 남는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "antenna_wire_connected", "value": True},
                ),
                # 원래 전선 아이템은 소모되고,
                # MK-II에 연결하러 갈 때 사용할 '전선의 반대쪽 끝'만 인벤토리에 남기는 식으로 구성
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.LONG_WIRE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.LONG_WIRE_FREE_END,
                        "description": "한쪽 끝은 능선 위 안테나에 고정되어 있고, 다른 쪽 끝만 손에 남아 있는 긴 전선이다. MK-II 단자에 연결할 수 있을 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 MK-II로 내려가, 남은 전선 끝을 단자에 연결할 수 있습니다.",
                ),
            ],
        ),
    ],
)
