from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

# --- [Scene 1: 그늘진 해변 (베이스캠프)] ---
CH1_SCENE1_DATA = SceneData(
    id=SceneID.CH1_SCENE1,
    name="그늘진 해변 (베이스캠프)",
    initial_text=(
        '"헥헥... 죽는 줄 알았네."\n\n'
        "당신은 젖 먹던 힘을 다해 MK-II를 거대한 야자수 그늘 아래로 옮기는 데 성공했습니다. "
        "기계도 나도 더 이상 직사광선에 고통받지 않아도 됩니다. 이곳은 이제 나의 훌륭한 베이스캠프입니다.\n\n"
        "그늘 밖은 여전히 용광로 같습니다. 동쪽 해변 끝에는 난파선 잔해가 아지랑이 너머로 보이고, "
        "북쪽에는 숲 입구가 보입니다. 바로 앞에는 파도에 떠밀려온 쓰레기 더미가 쌓여 있고, "
        "시원한 바다와 따뜻한 모래사장이 펼쳐져 있습니다.\n\n"
        "일단은 안전합니다. 이제 어떻게 할까요?"
    ),
    initial_state={
        "wreck_path_inspected": False,
        "tree_inspected": False,
        "coconut_obtained": False,  # 코코넛 획득 여부
        "crab_caught": False,
        "searched_trash": False,
        "has_shelter": False,
        "forest_cleared": False,  # 숲길 개척 여부
        "vines_collected": False,
        "mk2_inspected": False,  # MK-II 처음 조사 여부
        # MK-II 최종 수리용 상태
        "mk2_all_parts_gathered": False,  # 석영 조각 / 충전 배터리 / 전선 끝 세 개를 모두 들고 MK-II를 확인했는지
        "mk2_quartz_connected": False,  # 석영 조각 연결 여부
        "mk2_battery_connected": False,  # 충전 배터리 연결 여부
        "mk2_wire_connected": False,  # 전선 끝 연결 여부
        "mk2_launched": False,  # 최종 발진 여부 (플래그용)
    },
    on_enter_actions=[
        # 체력 UI 표시
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        # 1. 모래사장 (안전 지대)
        KeywordId.SAND: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="그늘 아래의 모래는 적당히 따뜻하다. 밖의 모래는 용암처럼 뜨겁겠지만, 여기선 찜질방 수준이다. 안전하다.",
        ),
        # 2. 바다
        KeywordId.SEA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "보기만 해도 시원해 보인다. 하지만 이것은 염분 농도 3.5%의 수용액이다. "
                "마시면 삼투압 현상으로 탈수가 가속화된다는 건 상식이다. "
                "경험적으로든 이론적으로든, 다시는 입에 대고 싶지 않다."
            ),
        ),
        # 3. 난파선 잔해 (이동 포인트)
        KeywordId.WRECKAGE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # 처음 조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동쪽을 보니 **[난파선 잔해]**가 꽤 멀리 있다.\n"
                                "가는 길에 그늘이 하나도 없어서, 저기까지 가려면 땀 좀 뺄 것 같다. (체력 소모 예상)"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한번 **[난파선 잔해]**를 선택하면 이동 여부를 결정합니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wreck_path_inspected", "value": True}),
                    ],
                ),
                # 두 번째 이후: 이동 여부 확인
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "**[난파선 잔해]**로 이동하시겠습니까?\n"
                                    "뜨거운 모래사장을 건너야 하므로 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="뜨거운 태양을 뚫고 난파선을 향해 걷기 시작합니다...",
                                    ),
                                    Action(type=ActionType.MODIFY_STAMINA, value=-2),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="지금은 베이스캠프 그늘에서 쉬는 게 낫겠습니다. 괜히 힘 뺄 필요 없죠.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 6. 숲 입구 (도끼로 길 뚫은 뒤 이동)
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # 숲길 개척 + 아직 덩굴 안 챙김
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="forest_cleared", value=True),
                        Condition(type=ConditionType.STATE_IS, target="vines_collected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "도끼로 잘려 나간 덩굴들이 입구 주변에 수북이 쌓여 있다.\n"
                                "당신은 그중에서 비교적 탄탄한 **[덩굴 줄기]** 몇 가닥을 골라 잘라 챙겨 둔다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.VINE_STEM,
                                "description": "단단하고 질긴 덩굴 줄기다. 뭔가를 묶거나 임시 로프로 쓰기 좋다.",
                            },
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "vines_collected", "value": True},
                        ),
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[숲 입구]**로 진입하시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="잘려 나간 덩굴 사이로 난 길을 따라 울창한 숲속으로 들어갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE4),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="덩굴 줄기를 한 번 더 살펴보다가, 일단은 들어가지 않기로 합니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
                # 숲길 개척 + 덩굴 이미 챙김
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="forest_cleared", value=True),
                        Condition(type=ConditionType.STATE_IS, target="vines_collected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[숲 입구]**로 진입하시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="잘려 나간 덩굴 사이로 난 길을 따라 울창한 숲속으로 들어갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE4),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 준비가 덜 된 것 같다."),
                                ],
                            },
                        ),
                    ],
                ),
                # 기본: 길이 막혀 있음
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "울창한 밀림이다. 억센 덩굴이 그물처럼 얽혀 있어 맨몸으로는 뚫고 지나갈 수 없다.\n"
                                "무언가 **날카롭고 무거운 도구**가 있다면 길을 낼 수 있을 것 같다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # 7. MK-II (최종 수리 대상)
        KeywordId.MK_II: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "그늘에 두니 엔진 열기가 조금 식은 것 같다. 하지만 여전히 작동 불능이다."
                                "거대한 야자수 그늘 아래에 세워둔 MK-II는, 겉보기엔 조용히 식어 가는 고철 덩어리일 뿐이다.\n"
                                "하지만, 한 번쯤은 더, 당신을 어디론가 데려다 줄 힘이 남아 있을지도 모른다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "mk2_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                        Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II의 패널을 열어 보니, 석영 발진기와 주 전원, 외부 통신선을 꽂아야 할 자리가 텅 비어 있다.\n"
                                "이대로는 아무리 버튼을 눌러도, 그저 조용한 철제 상자일 뿐이다.\n\n"
                                "이 기계를 다시 깨우려면, 석영 조각, 완전히 충전된 배터리, 그리고 안테나와 이어진 전선이 필요할 것 같다.\n\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="지금은 MK-II를 고칠 재료가 부족합니다. 세 가지 부품을 모두 모아 다시 점검해 보세요.",
                        ),
                    ],
                ),
                # (1) 아직 mk2_all_parts_gathered == False 이고, 세 부품이 모두 없는/부족한 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                        Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II의 패널을 열어 보니, 석영 발진기와 주 전원, 외부 통신선을 꽂아야 할 자리가 텅 비어 있다.\n"
                                "이대로는 아무리 버튼을 눌러도, 그저 조용한 철제 상자일 뿐이다.\n\n"
                                "이 기계를 다시 깨우려면, 석영 조각, 완전히 충전된 배터리, 그리고 안테나와 이어진 전선이 필요할 것 같다.\n\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="지금은 MK-II를 고칠 재료가 부족합니다. 세 가지 부품을 모두 모아 다시 점검해 보세요.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                        Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.LONG_WIRE_FREE_END),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II의 패널을 열어 보니, 석영 발진기와 주 전원, 외부 통신선을 꽂아야 할 자리가 텅 비어 있다.\n"
                                "이대로는 아무리 버튼을 눌러도, 그저 조용한 철제 상자일 뿐이다.\n\n"
                                "이 기계를 다시 깨우려면, 석영 조각, 완전히 충전된 배터리, 그리고 안테나와 이어진 전선이 필요할 것 같다.\n\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="지금은 MK-II를 고칠 재료가 부족합니다. 세 가지 부품을 모두 모아 다시 점검해 보세요.",
                        ),
                    ],
                ),
                # (2) 부품 세 개를 모두 들고 있는데 아직 mk2_all_parts_gathered는 False인 경우 → '훌륭하다' 멘트 + 준비 완료
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                        Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
                        Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
                        Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LONG_WIRE_FREE_END),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "패널을 열어 내부를 확인하는 순간, 배낭 속에서 딸깍딸깍 서로 부딪히는 세 가지 부품의 감촉이 느껴진다.\n\n"
                                "석영 조각, 완전히 충전된 산업용 배터리, 그리고 능선 위 안테나와 이어질 기다란 전선 끝.\n"
                                "이 섬 구석구석에서 모아 온 조각들이, 이제 눈앞에서 하나의 퍼즐처럼 제자리를 기다리고 있다.\n\n"
                                "이 정도면… 정말로 MK-II를 고칠 준비가 된 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=("훌륭합니다. 이제 부품을 하나씩 연결할 수 있습니다."),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "mk2_all_parts_gathered", "value": True},
                        ),
                    ],
                ),
                # (3) mk2_all_parts_gathered == True 이후 MK-II를 살펴볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=True),
                        Condition(type=ConditionType.STATE_IS, target="mk2_launched", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "MK-II 옆에는 석영 조각과 충전된 배터리, 기다란 전선 끝이 가지런히 놓여 있다.\n\n"
                                "패널 안쪽의 빈 소켓들은 마치 ‘여기에 끼워 달라’고 손을 내밀고 있는 것 같다.\n\n"
                                "이제 남은 일은 간단하다. 그동안의 여정을 함께해 준 이 조각들을, 각자의 자리로 돌려보내는 것뿐이다.\n\n"
                                "연구실에서부터 이 섬 구석구석까지 함께 굴러온 스패너는, 그 마지막 자리를 굳게 잠가 줄 순간만을 조용히 기다리고 있다."
                            ),
                        ),
                    ],
                ),
                # (4) mk2_launched == True 이후 (이 씬으로 다시 돌아올 일은 거의 없겠지만 방어용)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk2_launched", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "지금 이 MK-II는 더 이상 ‘출발 전’ 상태가 아니다.\n"
                                "당신이 내린 마지막 선택은 이미 어딘가로 향해 버렸고, 이곳의 시간은 조용히 흘러갔을 뿐이다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 8. 쓰레기 더미
        KeywordId.TRASH_PILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="searched_trash", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "역겨운 냄새를 참으며 쓰레기를 뒤진다. 베이스캠프 바로 앞이라 안전하게 파밍할 수 있다.\n"
                                "쓸만해 보이는 **[빈 페트병]**과 **[비닐]** 조각을 발견했다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-3),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.PLASTIC_BOTTLE, "description": "찌그러진 페트병이다."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.VINYL, "description": "구멍 나지 않은 튼튼한 비닐이다."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "searched_trash", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="더 이상 쓸만한 건 없다.",
                        )
                    ]
                ),
            ],
        ),
        # 9. 야자수
        KeywordId.PALM_TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 첫 조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="tree_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "매우 높다. 올라가는 건 불가능하다. 위를 보니 **[코코넛]**이 매달려 있다.\n"
                                "무언가 도구로 충격을 주면 떨어질지도 모른다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "tree_inspected", "value": True}),
                    ],
                ),
                # 이후: 발로 차기
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="야자수를 있는 힘껏 발로 찼다! ...꿈쩍도 안 한다. 발가락이 부러질 것 같다.",
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-3),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="[경고] 맨몸으로 도전하다 체력이 감소했습니다.",
                        ),
                    ]
                ),
            ],
        ),
    },
    combinations=[
        # 숲 입구 뚫기: 소방 도끼 + 숲 입구
        Combination(
            targets=[KeywordId.FOREST_ENTRY, KeywordId.FIRE_AXE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "손에 묵직한 **[소방 도끼]**를 쥐었다. 붉은 날이 햇빛을 받아 번뜩인다.\n\n"
                        '"길이 없으면 만들면 그만이지."\n\n'
                        "기합과 함께 도끼를 휘둘렀다. *퍼억! 툭!* 질긴 덩굴들이 허무하게 잘려 나간다.\n"
                        "몇 번의 도끼질 끝에, 사람이 지나갈 만한 통로가 확보되었다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "forest_cleared", "value": True}),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이제 **[숲 입구]**로 진입할 수 있습니다.",
                ),
            ],
        ),
        # 스패너 + 야자수 → 코코넛 떨어뜨리기
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**를 던져 **[코코넛]**을 정확히 맞췄다.\n"
                        "툭, 하고 열매가 떨어진다. 훌륭한 투구였다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.COCONUT, "description": "단단한 껍질의 열매."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "coconut_obtained", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="이미 코코넛을 떨어뜨렸습니다. 더 이상 열매가 없습니다.",
                )
            ],
        ),
        # ==========================
        # MK-II 수리 조합들
        # ==========================
        # (A) 부품이 모두 모이기 전에 조립 시도 → 부정 피드백 (석영/배터리/전선 공통)
        Combination(
            targets=[KeywordId.MK_II, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석영 조각을 손에 쥐고 소켓을 바라보다가, 당신은 잠시 멈칫한다.\n\n"
                        "이 한 조각만 억지로 끼워 넣기엔, 아직 MK-II 안쪽이 너무 많은 빈자리로 가득 차 있다.\n"
                        "모든 부품이 모였을 때 한 번에 조립하는 편이, 이 마지막 기계에게도 예의일 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="아직 필요한 부품들이 모두 모이지 않았습니다. 세 가지 부품을 모두 모은 뒤 다시 조립을 시작하세요.",
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MK_II, KeywordId.CHARGED_HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "충전된 배터리를 들어 단자에 가져가 보지만, 아직은 뭔가 중요한 연결이 빠져 있는 느낌이다.\n\n"
                        "심장을 미리 달아 버리면, 다른 장기들을 달기도 전에 다시 멈춰 버릴지도 모른다.\n"
                        "부품을 모두 모은 뒤, 한 번에 연결해 주는 편이 좋을 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="아직 필요한 부품들이 모두 모이지 않았습니다. 세 가지 부품을 모두 모은 뒤 다시 조립을 시작하세요.",
                ),
            ],
        ),
Combination(
            targets=[KeywordId.MK_II, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "배터리를 들어 단자에 가져가 보지만, "
                        "완전히 충전되지 않은 상태의 배터리로는 MK-II를 작동시킬 수 없을 것 같다.\n"
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="아직 필요한 부품들이 모두 모이지 않았습니다. 세 가지 부품을 모두 모은 뒤 다시 조립을 시작하세요.",
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MK_II, KeywordId.LONG_WIRE_FREE_END],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LONG_WIRE_FREE_END),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "안테나에서 내려온 기다란 전선 끝을 단자에 대 보지만, 아직 전류도, 진동도, 심장도 없다.\n\n"
                        "빈 기계에 줄만 먼저 걸어 놓는 건, 아직 말이 통하지 않는 상대에게 전화를 거는 것과 다르지 않다.\n"
                        "모든 준비가 끝난 뒤, 마지막에 이 전선을 꽂아야 진짜로 이야기가 시작될 것이다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="아직 필요한 부품들이 모두 모이지 않았습니다. 세 가지 부품을 모두 모은 뒤 다시 조립을 시작하세요.",
                ),
            ],
        ),
        # (B) 부품이 모두 모인 뒤 실제 연결: 석영 조각
        Combination(
            targets=[KeywordId.MK_II, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_quartz_connected", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석영 조각을 조심스럽게 발진기 소켓에 꽂아 넣는다.\n\n"
                        "손가락 끝에서 미세한 떨림이 느껴진다. 마치 이 작은 결정이 다시 한 번 진동을 시작해도 좋다고, "
                        "당신에게 허락을 구하는 것 같다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.QUARTZ_SHARD,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mk2_quartz_connected", "value": True},
                ),
            ],
        ),
        # (C) 부품이 모두 모인 뒤 실제 연결: 충전된 산업용 배터리
        Combination(
            targets=[KeywordId.MK_II, KeywordId.CHARGED_HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_battery_connected", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "충전된 산업용 배터리를 주 전원 단자에 밀어 넣는다.\n\n"
                        "단자가 맞물리는 순간, MK-II 내부 어딘가에서 묵직한 ‘탁’ 하는 소리가 난다.\n"
                        "한동안 돌려 두었던 수력 발전기의 시간이, 이제 이 한 기계의 심장으로 흘러들어온다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.CHARGED_HEAVY_BATTERY,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mk2_battery_connected", "value": True},
                ),
            ],
        ),
        # (D) 부품이 모두 모인 뒤 실제 연결: 기다란 전선 끝
        Combination(
            targets=[KeywordId.MK_II, KeywordId.LONG_WIRE_FREE_END],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_wire_connected", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LONG_WIRE_FREE_END),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "능선 위 안테나에서 내려온 기다란 전선 끝을 통신 단자에 감아 매고, 단단히 고정한다.\n\n"
                        "멀리 산 정상에서부터 이 해변까지, 전선이 그려 온 선이 머릿속에 그려진다.\n"
                        "이제 그 선을 따라, 당신의 신호도 함께 흘러갈 것이다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.LONG_WIRE_FREE_END,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mk2_wire_connected", "value": True},
                ),
            ],
        ),
        # (E) MK-II + 스패너 : 최종 조임 & 발진 여부 확인
        #   - 먼저 '모든 부품이 연결된 경우'를 만족하는 조합을 위에 두고,
        #     그렇지 않을 때는 아래의 부정 피드백 조합이 동작하도록 순서를 조절한다.
        Combination(
            targets=[KeywordId.MK_II, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_quartz_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_battery_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_wire_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="mk2_launched", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.REQUEST_CONFIRMATION,
                    value={
                        "prompt": (
                            "스패너를 손에 쥐고 MK-II의 마지막 볼트들을 하나씩 조여 나간다.\n\n"
                            "석영은 제자리를 찾았고, 배터리는 숨을 고르고 있으며, 전선은 능선 위 안테나와 이곳을 단단히 이어 주고 있다.\n"
                            "이제, 이 기계를 다시 한 번 세상으로 던져 보낼 수 있다.\n\n"
                            "MK-II를 기동해 새로운 목적지로 향하시겠습니까?\n"
                            "이 선택 이후에는, 더 이상 이 섬으로 돌아오지 못할 수도 있습니다."
                        ),
                        "confirm_actions": [
                            Action(
                                type=ActionType.PRINT_NARRATIVE,
                                value=(
                                    "마지막 볼트를 조여 고정하자, MK-II 내부에서 저속 모터가 도는 소리가 서서히 커져 간다.\n\n"
                                    "계기판의 불빛들이 하나둘 살아나고, 안테나를 타고 올라간 신호가 어딘가 먼 곳을 향해 날아간다.\n"
                                    "당신은 조용히 숨을 고른 뒤, 기체 안으로 몸을 밀어 넣는다."
                                ),
                            ),
                            Action(
                                type=ActionType.UPDATE_STATE,
                                value={"key": "mk2_launched", "value": True},
                            ),
                            Action(
                                type=ActionType.MOVE_SCENE,
                                value=SceneID.CH1_SCENE10,
                            ),
                        ],
                        "cancel_actions": [
                            Action(
                                type=ActionType.PRINT_NARRATIVE,
                                value=(
                                    "스패너를 잠시 내려놓고 MK-II 옆에 선다.\n"
                                    "지금 이 선택이 마지막일지도 모른다는 생각이 머릿속을 맴돈다.\n"
                                    "조금 더 정리하고, 천천히 마음을 고르기로 한다."
                                ),
                            )
                        ],
                    },
                )
            ],
        ),
        # (F) MK-II + 스패너 : 아직 부품이 덜 연결된 경우 → 부정 피드백
        Combination(
            targets=[KeywordId.MK_II, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mk2_launched", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너를 쥐고 MK-II의 패널을 바라보다가, 당신은 손을 멈춘다.\n\n"
                        "아직은 몇 군데 소켓이 비어 있고, 전선이 연결되지 않은 단자가 남아 있다.\n"
                        "지금 볼트를 조여 버리면, 이 기계는 반쯤만 깨어난 채 다시 잠들지도 모른다."
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="모든 부품을 연결한 뒤에 마지막 조임을 진행하세요. (석영, 배터리, 전선 끝이 모두 연결되어야 합니다.)",
                ),
            ],
        ),
    ],
)
