from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE5_DATA = SceneData(
    id=SceneID.CH1_SCENE5,
    name="죽음의 늪 (맹독의 길목)",
    body=(
        "생태 관측소 뒤편의 좁은 길을 따라 한참을 내려오자, 발밑 흙이 점점 질어지기 시작한다.\n"
        "발밑에는 탁한 늪물이 질척거리며 고여 있어, 어디든 발을 잘못 디디면 그대로 빠질 것 같다.\n"
        "길 옆에는 껍질이 두껍고 줄기가 굵은 고무나무 몇 그루가 서 있고, 공기에서는 썩은 물 냄새가 올라온다.\n\n"
        "앞쪽으로는 녹색 거품이 피어오르는 넓은 늪지대가 펼쳐져 있고, 중앙의 외길 위에는 거대한 악어 한 마리가 몸을 뻗고 누워 있다.\n"
        "늪 가장자리에는 물살에 떠밀려 온 듯한 늪 쓰레기 더미가 쌓여 있어, 무언가 쓸 만한 것이 있을지도 모른다.\n"
        "그 뒤쪽으로는 물 위에 반쯤 떠 있는 끊어진 다리가 보이고, 그 너머에는 조금 더 단단해 보이는 언덕과 "
        "어두운 동굴 입구 비슷한 것이 희미하게 보인다.\n\n"
    ),
    initial_state={
        "gator_removed": False,
        "bucket_filled": False,
        "gas_trap_ready": False,
        "bridge_built": False,
        "forest_path_inspected": False,
        "trash_searched": False,
        "cave_inspected": False,
        "rubber_sap_opened": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # === ALIAS 키워드들 ===
        # "쓰레기 더미" → "늪 쓰레기 더미"
        KeywordId.SWAMP_TRASH_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            target=KeywordId.SWAMP_TRASH,
        ),
        # "늪" → "늪물"
        KeywordId.SWAMP_WATER_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            target=KeywordId.SWAMP_WATER,
        ),
        # "악어" → "거대한 악어"
        KeywordId.GIANT_CROCODILE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            target=KeywordId.GIANT_CROCODILE,
        ),
        # "다리" → "끊어진 다리"
        KeywordId.BROKEN_BRIDGE_ALIAS: KeywordData(
            type=KeywordType.ALIAS,
            target=KeywordId.BROKEN_BRIDGE,
        ),
        KeywordId.CAVE: KeywordData(
            type=KeywordType.ALIAS,
            target=KeywordId.CAVE_ENTRANCE,
        ),
        # 되돌아가는 길: 숲 입구 -> CH1_SCENE4
        # 되돌아가는 길: 관측소 쪽으로 -> CH1_SCENE4
        KeywordId.ECO_OBSERVATORY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                # 처음 확인
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
                                "뒤쪽 경사로를 따라 조금만 올라가면 다시 관측소 근처 숲으로 돌아갈 수 있을 것 같다.\n"
                                "한 번 올라가면 다시 내려오려면 꽤 힘을 써야 할 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=("다시 한 번 **[생태 관측소]**를 입력하면 숲 쪽으로 돌아갈지 물어봅니다.\n"),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "forest_path_inspected", "value": True},
                        ),
                    ],
                ),
                # 이후에는 확인 프롬프트
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
                                "prompt": (
                                    "관측소 쪽으로 되돌아가 생태 관측소 근처로 돌아가시겠습니까?\n"
                                    "가파른 경사로를 올라가야 하므로 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 미련이 남는 늪을 뒤로한 채, "
                                            "질퍽한 경사로를 따라 천천히 위쪽 숲과 관측소 쪽으로 올라간다."
                                        ),
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,  # ✅ 체력 소모
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
        KeywordId.CAVE_ENTRANCE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 1) 다리가 아직 없을 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "저쪽 언덕 아래로 어렴풋이 동굴 입구가 보이지만, "
                                "그 앞까지 가려면 먼저 끊어진 다리를 건널 수 있어야 한다.\n"
                                "지금은 발을 디딜 곳이 없어, 이 거리에서 바라보기만 할 수 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="임시 다리를 만들어 끊어진 구간을 메워야 동굴 입구까지 갈 수 있을 것 같다.",
                        ),
                    ],
                ),
                # 2) 다리가 완성된 뒤, 처음 조사
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bridge_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="cave_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "임시 다리를 조심스레 건너 언덕 쪽으로 다가가자, "
                                "바위 사이로 어두운 동굴 입구가 뚜렷이 드러난다.\n"
                                "안쪽에서는 차갑고 축축한 공기가 흘러나오고, "
                                "희미하게 물 떨어지는 소리가 들리는 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=("다시 한 번 **[동굴 입구]**를 입력하면 석회 동굴 안으로 들어갈지 물어봅니다.\n"),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "cave_inspected", "value": True},
                        ),
                    ],
                ),
                # 3) 다리가 완성된 뒤, 이동 여부 확인 (+ 체력 2 소모)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bridge_built", value=True),
                        Condition(type=ConditionType.STATE_IS, target="cave_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "동굴 입구를 통해 석회 동굴 안으로 들어가시겠습니까?\n"
                                    "미끄러운 경사로를 오르내려야 하므로 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 한 번 깊게 숨을 들이마시고, "
                                            "임시 다리를 건너 어두운 석회 동굴 속으로 조심스럽게 발을 들인다."
                                        ),
                                    ),
                                    Action(
                                        type=ActionType.MODIFY_STAMINA,
                                        value=-2,  # ✅ 여기서 체력 2 소모
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE6,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 늪지대를 조금 더 살펴보기로 한다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 늪 주변 쓰레기 더미 (양동이, 페트병, 염소 소독제 파밍)
        KeywordId.SWAMP_TRASH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "늪 가장자리에는 밀려온 쓰레기 더미가 쌓여 있다.\n"
                "녹슨 캔, 부러진 플라스틱 조각, 정체 모를 금속 부품들이 뒤섞여 있다."
            ),
            interactions=[
                # 처음 뒤질 때
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
                                "예전에 난파선 근처에서 주웠던 것과 거의 똑같이 생겼다. "
                                "찌그러진 빈 페트병 몇 개와, 글자가 반쯤 벗겨진 염소 소독제 통도 함께 건져 올렸다."
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
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.CHLORINE_AGENT,
                                "description": "‘수처리용 소독제’라고 적힌 낡은 통이다. 염소 냄새가 강하게 난다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "trash_searched", "value": True},
                        ),
                    ],
                ),
                # 이후에는 더 이상 쓸만한게 없음
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
        # 늪물
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
                # 아직 길을 막고 있을 때
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
                # 이미 독가스로 물러난 뒤
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
                                "악어는 더 이상 외길을 막고 있지 않다.\n"
                                "늪 가장자리 진흙 속으로 반쯤 몸을 숨긴 채, 씁쓸한 표정으로 이쪽을 노려볼 뿐이다."
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
                # 악어는 치웠지만 다리를 보강하지 못했을 때
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
                # 이미 임시 다리가 설치된 경우
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
        KeywordId.RUBBER_TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,  # 상태별로 인터랙션에서 출력하니까 None으로 두는 걸 추천
            interactions=[
                # 아직 도끼질 안 해서 수액이 많이 안 나올 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="rubber_sap_opened",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "껍질이 두껍고 줄기가 굵은 나무다. 여기저기 오래된 상처 자국이 보이고, "
                                "갈라진 틈에서 하얀 진이 조금씩 배어나오고 있다.\n"
                                "가까이 다가가면 나무 수액 특유의 약간 달큰한 냄새가 난다."
                            ),
                        ),
                    ],
                ),
                # 한 번 도끼질 해서 rubber_sap_opened == True인 상태
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="rubber_sap_opened",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "껍질이 갈라진 고무나무 줄기에서 하얀 수액이 계속 흘러내리고 있다.\n"
                                "진이 굳어가며 줄기 표면에 두꺼운 층을 만들고, 바닥에는 점점점 작은 방울 자국이 쌓여 있다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # === [독가스 트랩: 늪물 → 염소 양동이 → 독가스 양동이] ===
        # 1단계: 녹슨 양동이 + 늪물 → 늪물 담은 양동이
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
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUSTY_BUCKET),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WATER_BUCKET,
                        "description": "독특한 냄새가 나는 늪물이 가득 담긴 녹슨 양동이다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "bucket_filled", "value": True},
                ),
            ],
        ),
        # 늪물 담은 양동이 + 식초만 먼저 넣으려 할 때 → "먼저 염소부터" 힌트
        Combination(
            targets=[KeywordId.WATER_BUCKET, KeywordId.VINEGAR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATER_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "늪물이 담긴 양동이에 식초를 조금 부어 보았지만, 거품이 약하게 일어날 뿐이다.\n"
                        "그냥 냄새만 더 고약해졌을 뿐, 강력한 가스가 만들어지는 느낌은 아니다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="먼저 염소 성분이 충분히 녹아들도록 염소 소독제를 섞는 편이 좋을 것 같다.",
                ),
            ],
        ),
        # 늪물 담은 양동이 + 반쯤 남은 식초일 때도 비슷한 힌트
        Combination(
            targets=[KeywordId.WATER_BUCKET, KeywordId.VINEGAR_HALF],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATER_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR_HALF),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "남아 있던 식초를 조금 넣어 보았지만, 거품이 잠깐 일다가 금세 사그라든다.\n"
                        "이 정도로는 넓은 공간에 영향을 줄 만한 양의 가스를 만들 수 없다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="역시 먼저 염소 소독제를 풀어서, 물 전체를 반응할 준비가 된 상태로 만드는 편이 좋겠다.",
                ),
            ],
        ),
        # 2단계: 늪물 담은 양동이 + 염소 소독제 → 염소 양동이
        Combination(
            targets=[KeywordId.WATER_BUCKET, KeywordId.CHLORINE_AGENT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WATER_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "늪물이 담긴 양동이에 염소 소독제를 조금씩 부어 넣었다.\n"
                        "거품이 일어나며 특유의 수영장 냄새가 더 강해진다. 염소 성분이 물에 충분히 녹아든 것 같다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.WATER_BUCKET),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CHLORINE_AGENT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.CHLORINE_BUCKET,
                        "description": "늪물에 염소 소독제가 녹아든 양동이다. 가까이 가기만 해도 눈이 시큰거린다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 산성을 가진 무언가를 더하면 위험한 기체가 나올 것 같다.",
                ),
            ],
        ),
        # 염소 소독제 + 식초만 바로 섞으려 할 때 → "물에 먼저 풀어라" 힌트
        Combination(
            targets=[KeywordId.CHLORINE_AGENT, KeywordId.VINEGAR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소독제 가루 위에 식초 몇 방울을 떨어뜨리자 미세한 거품이 일어나긴 하지만, 양이 워낙 적어 금방 끝나 버린다.\n"
                        "이 정도로는 늪 전체에 퍼질 만한 가스를 만들 수 없다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="소독제를 먼저 늪물 같은 액체에 충분히 녹인 뒤, 그 양동이에 식초를 붓는 편이 더 효과적일 것 같다.",
                ),
            ],
        ),
        # 염소 소독제 + 반쯤 남은 식초만 바로 섞으려 할 때도 비슷한 힌트
        Combination(
            targets=[KeywordId.CHLORINE_AGENT, KeywordId.VINEGAR_HALF],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR_HALF),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소독제 가루 위에 남아 있던 식초를 조금 부어 보았지만, 아주 약한 거품만 일어났다.\n"
                        "마치 실험실의 미니어처를 보는 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="역시 넉넉한 양의 물에 소독제를 풀어 준 뒤, 거기에 식초를 붓는 편이 더 나을 것 같다.",
                ),
            ],
        ),
        # 염소 양동이 + 산업용 배터리 → 전기분해보다는 산·염기 반응이 낫다는 힌트
        Combination(
            targets=[KeywordId.CHLORINE_BUCKET, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "염소 양동이에 전극을 담가 전기를 흘려 보낼까 고민해 보지만, "
                        "어떤 극성으로 얼마나 흘려야 할지 가늠이 되지 않는다.\n"
                        "괜히 실수했다가 자기 쪽으로 가스를 뒤집어쓰는 수가 있다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="복잡한 전기분해보다는, 산-염기 반응을 이용하는 편이 더 간단하고 안전할 것 같다.",
                ),
            ],
        ),
        # 3단계: 염소 양동이 + 식초(풀) → 독가스 양동이 + 반쯤 남은 식초
        Combination(
            targets=[KeywordId.CHLORINE_BUCKET, KeywordId.VINEGAR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "염소 양동이에 식초를 천천히 부었다.\n"
                        "순식간에 거품이 일어나면서 코와 눈을 동시에 자극하는 독한 냄새가 치솟는다.\n"
                        "허겁지겁 고개를 돌려 숨을 참고 있는 사이, 양동이 위쪽에 위험한 기체가 가득 찬 느낌이 든다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CHLORINE_BUCKET),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINEGAR),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.GAS_BUCKET,
                        "description": "염소와 산이 반응해 만들어진 독가스가 가득한 양동이다. 가까이 서 있기만 해도 눈물이 날 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.VINEGAR_HALF,
                        "description": "반쯤 남은 식초다. 이미 상당량을 써 버렸지만, 한번 더 사용할 만큼 남아 있다.",
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
        # 3단계(변형): 염소 양동이 + 반쯤 남은 식초 → 독가스 양동이 (식초 완전 소진)
        Combination(
            targets=[KeywordId.CHLORINE_BUCKET, KeywordId.VINEGAR_HALF],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR_HALF),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "남아 있던 식초를 한 번에 염소 양동이에 부었다.\n"
                        "잠깐의 침묵 뒤, 양동이 안에서 치익 하는 소리와 함께 매캐한 기체가 몰려 나온다.\n"
                        "통 안을 모두 쥐어짜낸 기분이 들 만큼 강한 냄새다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CHLORINE_BUCKET),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINEGAR_HALF),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.GAS_BUCKET,
                        "description": "염소와 산이 반응해 만들어진 독가스가 가득한 양동이다. 더 이상 식초는 남지 않았다.",
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gas_trap_ready", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="독가스 양동이를 만들었습니다. 이제 식초는 전부 사용되었습니다.",
                ),
            ],
        ),
        # 독가스 양동이를 악어 쪽으로 굴리기
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
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.GAS_BUCKET),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gator_removed", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "gas_trap_ready", "value": False},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="거대한 악어가 길에서 물러났습니다.",
                ),
            ],
        ),
        # 염소 소독제만 들고 악어를 노릴 때 → 힌트
        Combination(
            targets=[KeywordId.CHLORINE_AGENT, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "염소 소독제 통을 그냥 악어 쪽으로 던져 볼까 생각하지만, "
                        "멀리서 튕겨 맞는 정도로는 효과가 있을 것 같지 않다.\n"
                        "가스를 만들어 넓게 퍼뜨리는 쪽이 훨씬 효율적일 것이다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="소독제를 통째로 던지기보다는, 늪물 양동이에 섞어 가스를 만들어 보는 편이 좋겠다.",
                ),
            ],
        ),
        # === [부교 퍼즐: 페트병 부표 → 끊어진 다리 보강] ===
        # 1단계: 플라스틱 병 + 비닐 → 부력 주머니
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
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.PLASTIC_BOTTLE),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINYL),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.FLOATING_BAG,
                        "description": "빈 페트병을 비닐 안에 모아놓은 주머니다. 잘 봉인하면 훌륭한 부력이 나올 것 같다.",
                    },
                ),
            ],
        ),
        # 2단계: 부력 주머니 + 방수 테이프 → 부력 장치
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
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FLOATING_BAG),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.WATERPROOF_TAPE),
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
        # 3단계: 부력 장치 + 끊어진 다리 → 임시 부교 완성
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
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FLOATING_DEVICE),
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
        # 녹슨 양동이 + 거대한 악어 → 의미 없음을 알려주는 피드백 + 힌트
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.GIANT_CROCODILE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.STATE_IS, target="gator_removed", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "빈 양동이를 들고 악어 쪽으로 다가가려 하지만, "
                        "악어가 눈을 번쩍 뜨며 낮게 으르렁거린다.\n"
                        "이 정도 무게감의 물건을 던진다고 해서 거대한 악어가 물러날 것 같진 않다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="단순한 타격보다는, 악어를 멀리서 쫓아낼 수 있는 강한 무언가가 필요해 보인다.",
                ),
            ],
        ),
        # 녹슨 양동이 + 염소 소독제 → 물이 필요함을 알려주는 피드백
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.CHLORINE_AGENT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUSTY_BUCKET),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
                # 늪물 없이 소독제만 넣어서는 안 됨
                Condition(type=ConditionType.STATE_IS, target="bucket_filled", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "빈 양동이에 염소 소독제를 붓자, 바닥에 하얀 가루가 얇게 깔린다.\n"
                        "하지만 액체가 없어 반응이 거의 일어나지 않고, 바람에 조금씩 날려 사라질 뿐이다."
                    ),
                ),
            ],
        ),
        # 늪물 + 빈 페트병 → 양이 너무 적다는 힌트 (큰 용기 유도)
        Combination(
            targets=[KeywordId.SWAMP_WATER, KeywordId.PLASTIC_BOTTLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_BOTTLE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "페트병을 늪 가장자리로 가져가 조심스럽게 늪물을 떠 보았다.\n"
                        "탁한 녹색 액체가 병 안에 차오르긴 했지만, 이렇게 작은 병 하나에 담긴 양으로는 "
                        "무언가를 본격적으로 실험하기엔 턱없이 부족해 보인다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "이 정도 작은 용량으로는 늪 전체나 거대한 악어에게 영향을 줄 만한 일을 하기 어렵다.\n"
                        "한 번에 더 많은 양을 옮기고 섞을 수 있는, 좀 더 큼직한 그릇이 필요할 것 같다."
                    ),
                ),
            ],
        ),
        # 늪물 + 염소 소독제 → 약한 가스 + 악어가 잠시 반응 (독가스 아이디어 힌트)
        Combination(
            targets=[KeywordId.SWAMP_WATER, KeywordId.CHLORINE_AGENT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_AGENT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "늪 가장자리 늪물 위에 염소 소독제를 조금 뿌려 보았다.\n"
                        "탁한 물 표면에서 거품이 피어오르더니, 연한 황록색 기포와 함께 수영장 냄새 같은 냄새가 살짝 퍼진다.\n"
                        "멀찍이 누워 있던 악어가 코를 벌름거리며 몸을 한 번 비틀지만, 이내 다시 제자리로 늘어지듯 눕는다."
                    ),
                ),
                Action(
                    type=ActionType.MODIFY_STAMINA,
                    value=-1,
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "[경고] 늪물과 염소 성분이 반응하면서 약한 독성 기체가 발생해서 체력이 감소했습니다. "
                        "지금처럼 조금씩 흘려 보내면 주변 공기만 미묘하게 독해질 뿐, "
                        "악어를 쫓아낼 정도의 효과는 없습니다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "독가스를 제대로 쓰려면, 넓게 흩어지기 전에 한데 모아서 "
                        "더 진하게 만들어 한 번에 퍼뜨리는 방법을 고민해 보는 편이 좋겠습니다."
                    ),
                ),
            ],
        ),
        # 늪물 + 염소 양동이 → 가스가 밖으로 새어 나가 버리는 낭비 + 독가스 트랩 힌트
        Combination(
            targets=[KeywordId.SWAMP_WATER, KeywordId.CHLORINE_BUCKET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHLORINE_BUCKET),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "염소 양동이를 들고 늪 가장자리로 다가가, 바깥 늪물을 한 번 더 끼얹어 보았다.\n"
                        "탁한 물이 넘치면서 가장자리에서 거품이 일어나고, 코를 찌르는 냄새가 늪 위로 퍼져 나간다.\n"
                        "멀찍이 누워 있던 악어가 코를 씰룩이며 몸을 한 번 비틀지만, 곧 다시 자리를 고쳐 눕는다."
                    ),
                ),
                Action(
                    type=ActionType.MODIFY_STAMINA,
                    value=-1,
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "[경고] 염소 양동이에서 새어 나온 기체가 공기 중으로 흩어지고 있습니다. "
                        "이렇게 밖으로 조금씩 새게 하면 악어도, 자신도 애매하게만 괴롭힐 뿐입니다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "독가스를 제대로 쓰려면, 늪 전체에 흘려 보내기보다는 "
                        "양동이 안에서 반응을 한 번에 폭발적으로 일으킨 뒤, "
                        "악어 쪽으로 한꺼번에 퍼뜨리는 편이 훨씬 효과적일 것 같습니다."
                    ),
                ),
            ],
        ),
        # 소방 도끼 + 고무나무 (처음 찍어서 수액 흐르게 만들기)
        Combination(
            targets=[KeywordId.FIRE_AXE, KeywordId.RUBBER_TREE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼로 고무나무 줄기를 살짝 내리치자, 두껍게 갈라진 껍질 사이로 하얀 수액이 더 힘차게 배어나오기 시작한다.\n"
                        "진이 줄기를 따라 천천히 흘러내리며 바닥에 작은 점들을 찍는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "rubber_sap_opened", "value": True},
                ),
            ],
        ),
        # 소방 도끼 + 고무나무 (이미 수액이 흐르고 있을 때 다시 찍기)
        Combination(
            targets=[KeywordId.FIRE_AXE, KeywordId.RUBBER_TREE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "이미 도끼질한 상처에서 하얀 수액이 계속 흘러내리고 있다.\n"
                        "더 찍어 봐야 수액만 괜히 낭비될 것 같다."
                    ),
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.RUBBER_TREE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛 껍질 안쪽을 고무나무 수액에 슥슥 문지르자, 표면에 끈적한 막이 생긴다.\n"
                        "잠시 말려 두면 물에도 잘 버티는 튼튼한 수차 날개가 될 것 같다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT_SHELL),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COATED_COCONUT_SHELL,
                        "description": "고무 수액으로 코팅한 코코넛 껍질이다. 수차 날개로 쓰기 좋다.",
                    },
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.COPPER_WIRE, KeywordId.RUBBER_TREE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COPPER_WIRE),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "피복이 벗겨진 구리 전선을 고무나무 수액에 여러 번 담갔다 빼낸다.\n"
                        "수액이 굳으면서 전선 주변에 얇은 고무막이 형성된다.\n"
                        "완벽한 공인 규격은 아니지만, 무인도 표준으로는 충분히 안전한 절연 전선이다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COPPER_WIRE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.INSULATED_COPPER_WIRE,
                        "description": "고무 수액으로 임시 피복을 씌운 구리 전선이다. 임시 회로를 짜기에 충분하다.",
                    },
                ),
            ],
        ),
        # 고무나무 + 코코넛 껍질 (아직 수액을 안 틔운 상태)
        Combination(
            targets=[KeywordId.RUBBER_TREE, KeywordId.COCONUT_SHELL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛 껍질을 고무나무 줄기에 대 보지만, 겉껍질이 단단해 수액이 거의 묻지 않는다.\n"
                        "먼저 줄기에 상처를 좀 더 내서 수액이 잘 나오게 만들어야 할 것 같다."
                    ),
                ),
            ],
        ),
        # 고무나무 + 구리 전선 (아직 수액을 안 틔운 상태)
        Combination(
            targets=[KeywordId.RUBBER_TREE, KeywordId.COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COPPER_WIRE),
                Condition(type=ConditionType.STATE_IS, target="rubber_sap_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "피복이 벗겨진 구리 전선을 고무나무 줄기에 대 보지만, 겉껍질만 미끄럽게 스칠 뿐이다.\n"
                        "먼저 줄기를 살짝 찍어 상처를 내고, 수액이 흘러나오도록 만들어야 전선에 제대로 묻을 것 같다."
                    ),
                ),
            ],
        ),
    ],
)
