from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE5_DATA = SceneData(
    id=SceneID.CH1_SCENE5,
    name="죽음의 늪 (Toxic Swamp)",
    initial_text=(
        "관측소 뒤편의 좁은 길을 따라 한참을 내려오자, 발밑 흙이 점점 질어지기 시작한다.\n"
        "한 걸음 내디딜 때마다 진흙이 신발을 붙잡고 늘어지는 느낌이 들고, 공기에서는 썩은 물 냄새가 올라온다.\n\n"
        "앞쪽으로는 녹색 거품이 피어오르는 넓은 늪지대가 펼쳐져 있고, 중앙의 외길 위에는 거대한 악어 한 마리가 몸을 뻗고 누워 있다.\n"
        "그 뒤쪽으로는 물 위에 반쯤 떠 있는 끊어진 다리가 보이고, 그 너머에는 조금 더 단단해 보이는 언덕과 "
        "어두운 동굴 입구 비슷한 것이 희미하게 보인다.\n\n"
        "뒤를 돌아보면, 숲에서 내려온 길 너머로 희미한 수풀과 나무들이 보인다. 필요하다면 다시 숲 입구 쪽으로 올라갈 수도 있을 것 같다."
    ),
    initial_state={
        "gator_removed": False,
        "bucket_filled": False,
        "gas_trap_ready": False,
        "bridge_built": False,
        "forest_path_inspected": False,
        "trash_searched": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # "쓰레기 더미" → "늪 쓰레기 더미"
        KeywordId.SWAMP_TRASH_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,  # 별도로 시야에 안 띄우고, 타이핑으로만 접근
            target=KeywordId.SWAMP_TRASH,
        ),
        # "늪" → "늪물"
        KeywordId.SWAMP_WATER_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,
            target=KeywordId.SWAMP_WATER,
        ),
        # "악어" → "거대한 악어"
        KeywordId.GIANT_CROCODILE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,
            target=KeywordId.GIANT_CROCODILE,
        ),
        # "다리" → "끊어진 다리"
        KeywordId.BROKEN_BRIDGE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            state=KeywordState.HIDDEN,
            target=KeywordId.BROKEN_BRIDGE,
        ),
        # 되돌아가는 길: 숲 입구 -> CH1_SCENE4
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="forest_path_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "뒤쪽 경사로를 따라 올라가면 다시 숲 입구와 생태 관측소 근처로 돌아갈 수 있을 것 같다.\n"
                                "한 번 올라가면 다시 내려오려면 꽤 힘을 써야 할 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한 번 숲 입구를 입력하면 숲 쪽으로 돌아갈지 물어봅니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "forest_path_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="forest_path_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "숲 입구 쪽으로 되돌아가 생태 관측소 근처로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 미련이 남는 늪을 뒤로한 채, 질퍽한 경사로를 따라 천천히 위쪽 숲으로 올라간다.",
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE4,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="조금 더 늪지대를 살펴보기로 한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 늪 주변 쓰레기 더미 (양동이 예비 확보)
        KeywordId.SWAMP_TRASH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "늪 가장자리에는 밀려온 쓰레기 더미가 쌓여 있다.\n"
                "녹슨 캔, 부러진 플라스틱 조각, 정체 모를 금속 부품들이 뒤섞여 있다."
            ),
            interactions=[
                # 처음 뒤질 때만 양동이/페트병 파밍
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="trash_searched",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "쓰레기 더미를 뒤적이다가, 익숙한 모양의 녹슨 양동이 하나를 발견했다.\n"
                                "예전에 난파선 근처에서 주웠던 것과 거의 똑같이 생겼다. 빈 페트병 몇 개도 함께 건져 올렸다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.RUSTY_BUCKET,
                                "description": "바닥이 찌그러졌지만 물을 담을 수 있는 튼튼한 양동이다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.PLASTIC_BOTTLE,
                                "description": "찌그러진 빈 페트병이다. 공기를 가두면 부력이 생길 것 같다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "trash_searched", "value": True},
                        ),
                    ],
                ),
                # 그 다음부터는 묘사만
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="trash_searched",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="더 뒤져봐도 쓸 만한 것은 보이지 않는다. 이미 건질 만한 것은 다 챙긴 것 같다.",
                        )
                    ],
                ),
            ],
        ),
        # 늪물 (전해질)
        KeywordId.SWAMP_WATER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "늪 표면에는 녹색과 갈색이 뒤섞인 거품이 둥둥 떠다닌다.\n"
                "소금기와 각종 광물이 섞여 있는지, 금속을 담그면 곧장 녹슬어 버릴 것 같은 색이다."
            ),
        ),
        # 거대한 악어
        KeywordId.GIANT_CROCODILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 악어가 아직 길을 막고 있을 때
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
                                "길 한가운데에 거대한 악어 한 마리가 몸을 떡하니 뻗고 누워 있다.\n"
                                "눈을 반쯤 감고 있지만, 꼬리 끝이 미세하게 꿈틀거리는 걸 보니 완전히 잠든 것은 아니다.\n"
                                "이대로 가까이 다가갔다간 식사 메뉴로 추가될 공산이 크다."
                            ),
                        )
                    ],
                ),
                # 가스 트랩으로 처리된 뒤
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
                                "악어는 더 이상 길을 막고 있지 않다. 한쪽 늪 가장자리로 비실비실 기어갔다가 "
                                "진흙 속으로 반쯤 몸을 숨긴 채 꿈틀거리지도 않는다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 끊어진 다리
        KeywordId.BROKEN_BRIDGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 악어가 아직 있을 때
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
                                "멀리 끊어진 다리가 보이지만, 그쪽으로 가는 길목을 악어가 통째로 틀어막고 있다.\n"
                                "지금 상태로는 다리까지 다가가 보기도 어렵다."
                            ),
                        )
                    ],
                ),
                # 악어는 치웠지만 아직 다리를 보강하지 못했을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="gator_removed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="bridge_built",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "악어가 길에서 비켜나자 끊어진 다리가 제대로 보인다.\n"
                                "반대편까지의 거리는 애매하게 멀어, 그대로 점프했다간 늪물에 빠져버릴 게 뻔하다.\n"
                                "가볍고 잘 뜨는 무언가로 임시 발판을 만들어 끼워 넣으면 건널 수 있을지도 모르겠다."
                            ),
                        )
                    ],
                ),
                # 이미 임시 다리를 만들어 놓았을 때
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
                                "빈 페트병과 비닐, 테이프를 동원해 만든 임시 다리가 물 위에 떠 있다.\n"
                                "발을 딛으면 살짝 출렁거리지만, 조심해서 건너면 반대편 언덕까지 갈 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # --- [가스 트랩: 염소 가스 살포] ---
        # 1단계: 양동이에 늪물 담기
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.SWAMP_WATER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "양동이를 늪 가장자리로 가져가 조심스럽게 늪물을 퍼담았다.\n"
                        "녹색 거품이 가라앉지 않고 표면에 둥둥 떠다니는 것이 심상치 않다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "bucket_filled", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={
                        "name": KeywordId.RUSTY_BUCKET,
                        "description": "독특한 냄새가 나는 늪물이 가득 담긴 녹슨 양동이다.",
                    },
                ),
            ],
        ),
        # 2단계: 양동이 + 배터리 (비닐과 테이프로 봉인, 전기분해)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATERPROOF_TAPE),
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "늪물이 가득 담긴 양동이 입구를 비닐로 덮고, 방수 테이프로 가장자리를 단단히 감아 봉인했다.\n"
                        "절연된 전선을 통해 산업용 배터리를 연결하자, 물속에서 거품이 더 거세게 피어오르기 시작한다.\n"
                        "잠시 후, 비닐 주머니가 서서히 부풀어 올라 터질 것 같은 모양이 된다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.RUSTY_BUCKET,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.GAS_BUCKET,
                        "description": "늪물을 전기분해해 만든 독가스가 가득 든 양동이다. 비닐이 불룩하게 부풀어 있다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gas_trap_ready", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="독가스 양동이를 만들었습니다. 거대한 악어 쪽으로 굴려 보낼 수 있을 것 같습니다.",
                ),
            ],
        ),
        # 양동이만 든 채로 악어를 노릴 경우 (가스 트랩 준비 안 됨)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="gas_trap_ready", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "양동이를 들어 악어를 향해 던져볼까 생각했지만, "
                        "이 정도 물세례로는 악어가 잠깐 눈만 깜빡이고 말 것 같다.\n"
                        "좀 더 치명적인 내용을 채워 넣어야 할 것 같다."
                    ),
                )
            ],
        ),
        # 3단계: 독가스 양동이를 악어 쪽으로 굴리기
        Combination(
            targets=[KeywordId.GAS_BUCKET, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.GAS_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="gas_trap_ready", value=True),
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "비닐이 불룩하게 부풀어 오른 양동이를 조심스레 악어가 있는 쪽 경사로에 굴렸다.\n"
                        "마지막에 돌멩이를 집어 들어 힘껏 던져 양동이를 가격하자, 펑 소리와 함께 탁한 기체가 퍼져 나간다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "악어는 놀라 몸을 비틀더니, 곧 숨이 막힌 듯 격하게 몸부림친다.\n"
                        "잠시 후 힘이 빠진 듯 늪 가장자리 쪽으로 비틀거리며 물러나더니, "
                        "더 이상 길 한가운데를 막고 있지 않게 된다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.GAS_BUCKET,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gator_removed", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="거대한 악어가 길에서 물러났습니다.",
                ),
            ],
        ),
        # --- [페트병 부교: 부력 발판 제작] ---
        # 1단계: 페트병 + 비닐 = 느슨한 부력 주머니
        Combination(
            targets=[KeywordId.PLASTIC_BOTTLE, KeywordId.VINYL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_BOTTLE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "빈 페트병 여러 개를 커다란 비닐 안에 욱여넣었다.\n"
                        "아직 입구를 막지 않아 공기가 빠져나가기 쉽지만, 부력을 만들 준비는 된 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.PLASTIC_BOTTLE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.FLOATING_BAG,
                        "description": "빈 페트병을 비닐 안에 모아놓은 주머니다. 잘 봉인하면 훌륭한 부력이 나올 것 같다.",
                    },
                ),
            ],
        ),
        # 2단계: 부력 주머니 + 방수 테이프 = 부력 장치
        Combination(
            targets=[KeywordId.FLOATING_BAG, KeywordId.WATERPROOF_TAPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FLOATING_BAG),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATERPROOF_TAPE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "비닐 입구를 돌돌 말아 접은 뒤, 방수 테이프로 여러 겹 칭칭 감아 봉인했다.\n"
                        "공기가 빠져나갈 틈이 거의 없어, 물 위에 던지면 튼튼한 부표처럼 떠 있을 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FLOATING_BAG,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.WATERPROOF_TAPE,
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.FLOATING_DEVICE,
                        "description": "물 위에 띄워 발판으로 쓸 수 있는 임시 부력 장치다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="부력 장치를 만들었습니다. 끊어진 다리 사이를 메우는 데 쓸 수 있을 것 같습니다.",
                ),
            ],
        ),
        # 3단계: 부력 장치 + 끊어진 다리 = 임시 부교 완성
        Combination(
            targets=[KeywordId.FLOATING_DEVICE, KeywordId.BROKEN_BRIDGE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FLOATING_DEVICE),
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=True),
                Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "부력 장치를 조심스럽게 끊어진 다리 아래 틈에 끼워 넣었다.\n"
                        "물 위에 둥둥 떠 있던 장치가 다리의 빈 공간을 받치며, 사람 한 명쯤은 건널 수 있을 정도로 안정된다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FLOATING_DEVICE,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "bridge_built", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="임시 부교가 완성되었습니다. 이제 조심해서 끊어진 다리를 건널 수 있을 것 같습니다.",
                ),
            ],
        ),
        # 악어가 아직 남아 있는데 다리를 보강하려는 경우
        Combination(
            targets=[KeywordId.FLOATING_DEVICE, KeywordId.BROKEN_BRIDGE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FLOATING_DEVICE),
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "부력 장치를 설치하려면 끊어진 다리 가장자리까지 다가가야 하지만, "
                        "그 전에 악어가 길을 막고 있어 접근할 수가 없다.\n"
                        "먼저 길을 막고 있는 녀석부터 어떻게든 치워야 한다."
                    ),
                )
            ],
        ),
    ],
)
