from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE5_DATA = SceneData(
    id=SceneID.CH1_SCENE5,
    name="죽음의 늪 (맹독 늪지대)",
    initial_text=(
        "숲을 더 깊이 파고들자 나무뿌리 사이로 진흙탕과 썩은 냄새가 치고 올라옵니다.\n"
        "얼마 지나지 않아 발밑은 탁한 물과 진흙이 뒤섞인 늪지대로 바뀌고, "
        "황록색 거품이 피어오르는 웅덩이들 사이로 얇은 통로만이 아슬아슬하게 이어져 있습니다.\n\n"
        "앞쪽 좁은 길을 따라가자, 거대한 악어 한 마리가 몸을 길게 뻗은 채 통로를 막고 있습니다. "
        "멀리에는 끊어진 나무 다리가 깊은 물 위에 매달려 있고, 그 너머로는 더 안전해 보이는 언덕이 희미하게 보입니다.\n"
        "뒤를 돌아보면 방금 지나온 숲길이 어둑하게 이어져 있습니다."
    ),
    initial_state={
        "camp_path_inspected": False,  # 숲으로 되돌아가는 길 설명 여부
        "bucket_filled": False,  # 양동이에 늪물이 담겼는지
        "gas_trap_ready": False,  # 독가스 양동이 준비 여부
        "gator_removed": False,  # 악어 퇴치 여부
        "bridge_built": False,  # 부교/부력 장치 설치 여부
    },
    on_enter_actions=[],
    keywords={
        # 숲으로 돌아가는 길 (포탈)
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 1회차: 설명
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="camp_path_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "뒤편으로는 조금 전 지나온 울창한 숲길이 어둑하게 이어져 있다. "
                                "조금만 걸어가면 다시 생태 관측소 근처로 돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한번 **[숲 입구]**를 입력하면 되돌아갈지 물어봅니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "camp_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 2회차 이후: 이동 여부 확인
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="camp_path_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "숲 쪽으로 되돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 썩은 물과 진흙을 뒤로하고 다시 숲의 그늘 속으로 발을 옮긴다.",
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE4,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="지금은 이 늪지대를 먼저 돌파해야 할 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 거대 악어
        KeywordId.GIANT_CROCODILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 아직 퇴치 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="gator_removed",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "거대한 악어가 진흙탕 위에 몸을 길게 뻗고 있다. "
                                "등껍질은 작은 언덕처럼 불룩 솟아 있고, 숨을 쉴 때마다 옆구리가 미세하게 들썩인다.\n"
                                "이대로는 악어를 자극하지 않고는 통로를 지나갈 수 없어 보인다."
                            ),
                        )
                    ],
                ),
                # 퇴치 후
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="gator_removed",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "악어는 이미 불쾌한 냄새를 피해 늪 깊은 곳으로 사라졌다. "
                                "통로에는 이제 미끄러운 진흙 자국만 남아 있다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 늪물
        KeywordId.SWAMP_WATER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=(
                "회녹색으로 탁한 늪물이다. 표면에는 거품과 기름막이 떠 있고, "
                "코를 찌르는 냄새가 난다. 물 속에는 각종 염류와 유기물이 뒤섞여 있을 것이다.\n"
                "전극을 꽂아 전류를 흘리면 뭔가 위험한 기체가 나올지도 모른다."
            ),
        ),
        # 끊어진 다리
        KeywordId.BROKEN_BRIDGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 아직 부교가 없을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="bridge_built",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "썩은 나무로 된 다리가 중간에서 똑 부러져 있다. "
                                "그 아래는 발이 닿지 않을 만큼 깊어 보이는 물이다.\n"
                                "그냥 뛰어넘기에는 거리가 애매하고, 그대로 떨어지면 늪 바닥으로 빨려 들어갈 것 같다.\n"
                                "가벼운 공기주머니나 부표 같은 것을 끼워 넣어 다리를 받쳐야 할 것 같다."
                            ),
                        )
                    ],
                ),
                # 부교 설치 후
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="bridge_built",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "임시로 만든 부력 장치 덕분에 다리가 간신히 형태를 유지하고 있다.\n"
                                "조심해서 이동하면 건너편 언덕까지 넘어갈 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # [악어 퍼즐] 1단계: 양동이에 늪물 담기
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.SWAMP_WATER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "양동이를 들어 늪물 속으로 천천히 밀어 넣었다. 거품과 기름막이 들러붙으며 "
                        "탁한 물이 양동이 안을 가득 채운다.\n"
                        "전해질은 충분히 많아 보인다. 전류를 흘리면 뭔가가 나올 것이다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={
                        "keyword": KeywordId.RUSTY_BUCKET,
                        "field": "description",
                        "value": "탁한 늪물이 가득 담긴 녹슨 양동이.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "bucket_filled", "value": True},
                ),
            ],
        ),
        # 이미 물이 담겨 있을 때
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.SWAMP_WATER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="양동이는 이미 늪물로 가득 차 있다.",
                )
            ],
        ),
        # [악어 퍼즐] 2단계: 전기분해용 가스 양동이 준비 (양동이 + 비닐)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.VINYL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATERPROOF_TAPE),
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=True),
                Condition(type=ConditionType.STATE_IS, target="gas_trap_ready", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "양동이 입구를 비닐로 덮고 방수 테이프로 단단히 감아 밀봉했다. "
                        "배터리에서 뽑은 전선을 양동이 안 늪물에 꽂자, 곧 거친 기포와 함께 독한 냄새가 비닐 안에 갇힌다.\n"
                        "비닐 풍선이 천천히 부풀어 오른다. 아주 위험한 즉석 가스 폭탄이 완성됐다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.VINYL,
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={
                        "keyword": KeywordId.RUSTY_BUCKET,
                        "field": "description",
                        "value": "부풀어 오른 비닐이 입구를 막고 있는, 위험한 가스로 가득 찬 양동이.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gas_trap_ready", "value": True},
                ),
            ],
        ),
        # 준비되지 않은 상태에서 비닐만 쓰려 할 때
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.VINYL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="비닐을 씌워도 안에 든 게 없다. 먼저 양동이에 적당한 용액을 채워야 한다.",
                )
            ],
        ),
        # [악어 퍼즐] 3단계: 가스 양동이를 악어에게 사용
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="gas_trap_ready", value=True),
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "부풀어 오른 양동이를 악어 쪽으로 굴렸다. 양동이가 악어 앞에서 멈추자, "
                        "돌을 하나 들어 정확히 던져 비닐을 터뜨렸다.\n"
                        "순간 지독한 냄새의 가스가 폭발하듯 퍼지고, 악어가 몸부림치며 늪 깊은 곳으로 도망친다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.RUSTY_BUCKET,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gator_removed", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gas_trap_ready", "value": False},
                ),
            ],
        ),
        # 이미 악어가 사라진 뒤에 다시 시도할 때
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="악어는 이미 이 근처에 없다.",
                )
            ],
        ),
        # [다리 퍼즐] 1단계: 페트병 + 비닐로 부력 장치 만들기
        Combination(
            targets=[KeywordId.PLASTIC_BOTTLE, KeywordId.VINYL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_BOTTLE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATERPROOF_TAPE),
                Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "주워 모은 페트병들을 큰 비닐 조각 안에 가득 집어넣고, "
                        "방수 테이프로 틈새가 없도록 칭칭 감아 묶었다.\n"
                        "커다란 공기 주머니 같은 부력 장치가 완성됐다. 다리 밑에 끼워 넣으면 버팀목이 되어 줄 것이다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.PLASTIC_BOTTLE,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.VINYL,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.FLOATING_BAG,
                        "description": "페트병과 비닐, 방수 테이프로 만든 거대한 공기 주머니. 꽤 든든해 보인다.",
                    },
                ),
            ],
        ),
        # [다리 퍼즐] 2단계: 부력 장치를 다리에 설치
        Combination(
            targets=[KeywordId.FLOATING_BAG, KeywordId.BROKEN_BRIDGE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FLOATING_BAG),
                Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "부력 장치를 끊어진 다리 아래 틈새에 밀어 넣고 온몸으로 눌러 고정했다.\n"
                        "잠시 삐걱거리는 소리가 나더니, 다리가 간신히 수평을 되찾는다. "
                        "조심해서라면 건너편 언덕까지 갈 수 있을 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FLOATING_BAG,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "bridge_built", "value": True},
                ),
            ],
        ),
        # 이미 다리가 보강된 뒤에 다시 시도할 때
        Combination(
            targets=[KeywordId.FLOATING_BAG, KeywordId.BROKEN_BRIDGE],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="bridge_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="다리는 이미 임시 보강이 끝난 상태다.",
                )
            ],
        ),
    ],
)
