from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

# --- [Scene 1: 그늘진 해변 (베이스캠프)] ---
CH1_SCENE1_DATA = SceneData(
    id=SceneID.CH1_SCENE1,
    name="그늘진 해변 (베이스캠프)",
    initial_text="---\n## 그늘진 해변 (베이스캠프)\n---\n\n",
    body=(
        '"헥헥... 죽는 줄 알았네."\n\n'
        "당신은 젖 먹던 힘을 다해 양자 가마솥을 거대한 야자수 그늘 아래로 옮기는 데 성공했습니다.\n\n"
        "기계도 나도 더 이상 직사광선에 고통받지 않아도 됩니다. 이곳은 이제 나의 훌륭한 베이스캠프입니다.\n\n"
        "동쪽 해변 끝에는 난파선 잔해가 아지랑이 너머로 보이고, 북쪽에는 숲 입구가 보입니다.\n\n"
        "바로 앞에는 파도에 떠밀려온 쓰레기 더미가 쌓여 있고, 시원한 바다와 따뜻한 모래사장이 펼쳐져 있습니다.\n\n"
        "일단은 안전합니다. 하지만 긴장이 풀리자마자 극심한 갈증이 밀려옵니다.\n\n"
        "땀을 너무 많이 흘렸습니다. 바닷물은 마실 수 없으니, 어떻게든 식수를 구할 방법을 찾는 게 급선무입니다."
    ),
    initial_state={
        "wreck_path_inspected": False,
        "tree_inspected": False,
        "coconut_obtained": False,  # 코코넛 획득 여부
        "searched_trash": False,
        "forest_cleared": False,  # 숲길 개척 여부
        "vines_collected": False,
        "forest_inspected": False,
        "quantum_inspected": False,  # 양자 가마솥 처음 조사 여부
        "distiller_built": False,  # 정수기 설치 여부
        # 양자 가마솥 최종 수리용 상태
        "quantum_all_parts_gathered": False,  # 석영 조각 / 충전 배터리 / 전선 끝 세 개를 모두 들고 양자 가마솥를 확인했는지
        "quantum_quartz_connected": False,  # 석영 조각 연결 여부
        "quantum_battery_connected": False,  # 충전 배터리 연결 여부
        "quantum_wire_connected": False,  # 전선 끝 연결 여부
        "quantum_launched": False,  # 최종 발진 여부 (플래그용)
    },
    keywords={
        KeywordId.SAND: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SANDY_BEACH),
        KeywordId.WRECKAGE_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WRECKAGE),
        KeywordId.FOREST: KeywordData(type=KeywordType.ALIAS, target=KeywordId.FOREST_ENTRY),
        # 포탈: 난파선 잔해, 숲 입구
        # 5. 난파선 잔해 (이동 포인트)
        KeywordId.WRECKAGE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # 1. 처음 조사 (기존 동일)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동쪽을 보니 **[난파선 잔해]**가 꽤 멀리 있다.\n\n"
                                "가는 길에 그늘이 하나도 없어서, 저기까지 가려면 땀 좀 뺄 것 같다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wreck_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # 2. [추가] 이동 시도 차단 (정수기가 없을 때)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="distiller_built", value=False),  # 정수기 미완성
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "저 멀리까지 다녀오려면 땀을 비오듯 쏟을 것이다.\n\n"
                                "돌아왔을 때 마실 물이 확보되지 않았다면, 그대로 탈진해버릴지도 모른다.\n\n"
                                "먼저 베이스캠프에 확실한 식수원을 만들어두고 떠나는 게 안전하겠다."
                            ),
                        ),
                    ],
                ),
                # 3. 이동 시도 허용 (정수기가 있을 때)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="wreck_path_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="distiller_built", value=True),  # 정수기 완성됨
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "**[난파선 잔해]**로 이동하시겠습니까?\n\n"
                                    "뜨거운 모래사장을 건너야 하므로 **체력이 2 소모**됩니다."
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="베이스캠프에 물이 있다는 사실에 안심하며, 뜨거운 태양을 뚫고 난파선을 향해 걷기 시작합니다...",
                                    ),
                                    Action(type=ActionType.MODIFY_STAMINA, value=-2),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_0),
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
        # 숲 입구 (도끼로 길 뚫은 뒤 이동)
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # 기본: 길이 막혀 있음
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="forest_cleared", value=False),
                    ],
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
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="forest_cleared", value=True),
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
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_0),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 준비가 덜 된 것 같다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 쓰레기 더미
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
                                "역겨운 냄새를 참으며 쓰레기를 뒤진다.\n\n"
                                "쓸만해 보이는 **[빈 페트병]**과 **[비닐]** 조각을 발견했다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-2),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.PLASTIC_BOTTLE, "description": "찌그러진 페트병이다."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.VINYL, "description": "구멍 나지 않은 튼튼한 비닐이다."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "searched_trash", "value": True}),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.TRASH_PILE, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="searched_trash", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="더 이상 쓸만한 건 없다.",
                        )
                    ],
                ),
            ],
        ),
        # 2. 바다 (물 뜨기 기능 추가)
        KeywordId.SEA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "보기만 해도 시원해 보인다. 하지만 이것은 염분 농도 3.5%의 수용액이다.\n\n"
                                "마시면 삼투압 현상으로 탈수가 가속화된다는 건 상식이다.\n\n"
                                "경험적으로든 이론적으로든, 다시는 입에 대고 싶지 않다."
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 3. 모래사장
        KeywordId.SANDY_BEACH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "달궈진 모래의 열기는 식을 줄 모른다. 엉덩이를 붙이고 앉기 힘들 정도로 뜨겁다.\n\n"
                "하지만 이 **고온**은 열역학적으로 볼 때 **증발**을 가속화하는 훌륭한 에너지원이다.\n\n"
                "간이 정수기를 설치하기엔 더할 나위 없는 조건이다."
            ),
        ),
        # 4. 정수기 제작
        KeywordId.DISTILLER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="모래 구덩이, 바닷물 병, 비닐 덮개로 만든 생존 과학의 결정체다.",
            interactions=[
                # Case 1: 아직 물이 안 고였을 때 (기본)
                Interaction(
                    conditions=[Condition(type=ConditionType.CHAPTER_STATE_IS, target="distiller_state", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "아직은 비닐에 물방울이 맺히지 않았다. 태양열로 물이 증류되려면 시간이 꽤 걸릴 것이다.\n\n"
                                "지금 계속 쳐다봐야 소용없다. 다른 지역을 탐색하고 **나중에 다시 와보자**."
                            ),
                        )
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.CHAPTER_STATE_IS, target="distiller_state", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "비닐 안쪽에 맑은 물방울이 충분히 맺혀 있다. 비닐을 톡 쳐서 컵에 모았다.\n"
                                "미지근하지만, 말라비틀어진 목을 적시는 데는 충분하다. 그 어떤 음료수보다 달콤하다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=20),  # 체력 회복
                        Action(type=ActionType.PRINT_SYSTEM, value="갈증이 해소되고 체력이 크게 회복되었습니다."),
                        # 물을 마셨으므로 다시 빈 상태로 변경
                        Action(type=ActionType.UPDATE_CHAPTER_STATE, value={"key": "distiller_state", "value": 0}),
                    ],
                ),
            ],
        ),
        # 5. 야자수
        KeywordId.PALM_TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 첫 조사
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="tree_inspected", value=False),
                        Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "매우 높다. 올라가는 건 불가능하다. 위를 보니 **[코코넛]**이 매달려 있다.\n\n"
                                "무언가 도구로 충격을 주면 떨어질지도 모른다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "tree_inspected", "value": True}),
                    ],
                ),
                # 이후: 발로 차기
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="tree_inspected", value=True),
                        Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=False),
                    ],
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
                    ],
                ),
                # 코코넛을 얻은 이후
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="이미 코코넛을 따버린 야자수다. 꼭대기에는 거대한 잎사귀만 무심하게 흔들리고 있다.",
                        )
                    ],
                ),
            ],
        ),
        # 6. 양자 가마솥 (최종 수리 대상)
        KeywordId.QUANTUM_CAULDRON: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "그늘에 두니 엔진 열기가 조금 식은 것 같다. 하지만 여전히 작동 불능이다.\n\n"
                                "거대한 야자수 그늘 아래에 세워둔 양자 가마솥은, 겉보기엔 조용히 식어 가는 고철 덩어리일 뿐이다.\n\n"
                                "하지만, 한 번쯤은 더, 당신을 어디론가 데려다 줄 힘이 남아 있을지도 모른다."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "quantum_inspected", "value": True},
                        ),
                    ],
                ),
                # (1) 아직 quantum_all_parts_gathered == False 이고, 세 부품이 모두 없는/부족한 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
                        Condition(
                            type=ConditionType.NOT_HAS_ALL_ITEMS,
                            target=[
                                KeywordId.CHARGED_HEAVY_BATTERY,
                                KeywordId.QUARTZ_SHARD,
                                KeywordId.LONG_WIRE_FREE_END,
                            ],
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "양자 가마솥의 패널을 열어 보니, 석영 발진기와 주 전원, 외부 통신선을 꽂아야 할 자리가 텅 비어 있다.\n\n"
                                "이대로는 아무리 버튼을 눌러도, 그저 조용한 철제 상자일 뿐이다.\n\n"
                                "이 기계를 다시 깨우려면, 석영 조각, 완전히 충전된 배터리, 그리고 안테나와 이어진 전선이 필요할 것 같다.\n\n"
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="지금은 양자 가마솥을 고칠 재료가 부족합니다. 세 가지 부품을 모두 모아 다시 점검해 보세요.",
                        ),
                    ],
                ),
                # (2) 부품 세 개를 모두 들고 있는데 아직 quantum_all_parts_gathered는 False인 경우 → '훌륭하다' 멘트 + 준비 완료
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
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
                                "이 정도면… 정말로 양자 가마솥을 고칠 준비가 된 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=("훌륭합니다. 이제 부품을 하나씩 연결할 수 있습니다."),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "quantum_all_parts_gathered", "value": True},
                        ),
                    ],
                ),
                # (3) quantum_all_parts_gathered == True 이후 양자 가마솥를 살펴볼 때
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=True),
                        Condition(type=ConditionType.STATE_IS, target="quantum_launched", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "양자 가마솥 옆에는 석영 조각과 충전된 배터리, 기다란 전선 끝이 가지런히 놓여 있다.\n\n"
                                "패널 안쪽의 빈 소켓들은 마치 ‘여기에 끼워 달라’고 손을 내밀고 있는 것 같다.\n\n"
                                "이제 남은 일은 간단하다. 그동안의 여정을 함께해 준 이 조각들을, 각자의 자리로 돌려보내는 것뿐이다.\n\n"
                                "연구실에서부터 이 섬 구석구석까지 함께 굴러온 스패너는, 그 마지막 자리를 굳게 잠가 줄 순간만을 조용히 기다리고 있다."
                            ),
                        ),
                    ],
                ),
                # (4) quantum_launched == True 이후 (이 씬으로 다시 돌아올 일은 거의 없겠지만 방어용)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_launched", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "지금 이 양자 가마솥은 더 이상 ‘출발 전’ 상태가 아니다.\n\n"
                                "당신이 내린 마지막 선택은 이미 어딘가로 향해 버렸고, 이곳의 시간은 조용히 흘러갔을 뿐이다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # --- 배경/분위기용 UNSEEN 오브젝트 ---
        "그늘": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="생와 사의 경계선이다. 이 선 밖으로 나가는 순간, 나는 '잘 익은 대학원생 구이'가 될 것이다.",
        ),
        "아지랑이": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="지면의 열기 때문에 공기가 흐물거린다. 내 멘탈도 저렇게 녹아서 흐물거리고 있다.",
        ),
        "갈증": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="목구멍이 사포로 문지른 것처럼 까끌거린다. 얼음 가득 채운 아이스 아메리카노 한 잔만 마실 수 있다면 영혼이라도 팔겠다.",
        ),
        "파도": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="철썩거리는 소리가 시원하게 들리지만 속지 않는다. 저건 마시는 순간 요단강 익스프레스를 타게 해줄 소금물이다.",
        ),
        "베이스캠프": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="거창하게 베이스캠프라고 불렀지만, 사실 야자수 한 그루와 찌그러진 솥단지 하나가 전부다. 내 인생처럼 초라하다.",
        ),
        "직사광선": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="살인적인 햇빛이다. 자외선 차단제도 안 발랐는데. 피부 노화가 걱정되는 걸 보니 아직 살만한가 보다.",
        ),
        "동쪽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="난파선 잔해가 보인다. 보물선이면 좋겠지만, 확률적으로 고철 덩어리일 가능성이 99.9%다.",
        ),
        "북쪽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="숲 입구가 보인다. 그늘은 있겠지만 뱀이나 벌레가 우글거릴 것이다. 연구실이나 정글이나 생존 경쟁이 치열한 건 매한가지다.",
        ),
        "땀": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="비 오듯 쏟아진다. 내 몸의 수분이 실시간으로 증발하고 있다. 이대로라면 곧 건어물이 될 것이다.",
        ),
        "안전": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="'일단은' 안전하다는 말만큼 불안한 말도 없다. 언제 머리 위로 코코넛이 떨어져 뇌진탕에 걸릴지 모르는 일이다.",
        ),
        "젖 먹던 힘": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="내 근섬유 하나하나가 비명을 지르고 있다. 평소에 운동 좀 할걸. '코딩은 체력전'이라는 교수님의 말씀이 이제야 뼈저리게 이해된다.",
        ),
        "기계": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="한때는 첨단 과학의 정수였지만, 지금은 야자수 그늘 아래 퍼져있는 무거운 쇳덩이다. 그래도 내가 가진 유일한 희망이다.",
        ),
        "나": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="땀에 절고 모래 범벅이 된 꼴이 가관이다. 대학원 면접 날 이후로 이렇게 엉망인 모습은 처음이다.",
        ),
        "고통": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="온몸이 욱신거린다. 하지만 살아있다는 증거라고 생각하니... 그래도 아픈 건 아픈 거다.",
        ),
        "긴장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="아드레날린 분비가 멈추자 급격한 피로가 몰려온다. 밤새 논문 쓰고 제출 버튼 누른 직후의 그 기분이다.",
        ),
        "식수": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="인간의 몸은 70%가 물이다. 지금 나는 65% 정도로 떨어지고 있는 것 같다. 빨리 보충하지 않으면 시스템이 종료될 것이다.",
        ),
    },
    combinations=[
        # 페트병에 바닷물 담기
        Combination(
            targets=[KeywordId.SEA, KeywordId.PLASTIC_BOTTLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.PLASTIC_BOTTLE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="빈 페트병을 바닷물에 푹 담가 가득 채웠다. 묵직하다.\n\n그냥 마실 수는 없지만, 정수할 방법이 있을 것이다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.PLASTIC_BOTTLE),  # 빈 병 제거
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SEAWATER_BOTTLE,  # "바닷물이 담긴 페트병"
                        "description": "바닷물이 찰랑거리는 페트병이다. 뚜껑을 열면 짠 냄새가 진동한다. 그냥 마시면 탈수 증상이 올 것이다.",
                    },
                ),
            ],
        ),
        # 비닐 + 바닷물이 담긴 페트병 = 간이 정수기 키트 제작 (인벤토리 아이템)
        Combination(
            targets=[KeywordId.VINYL, KeywordId.SEAWATER_BOTTLE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINYL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SEAWATER_BOTTLE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "비닐과 바닷물이 든 페트병을 챙겨서 정수기를 만들 준비를 마쳤다.\n\n"
                        "이제 볕이 좋은 곳에 설치하기만 하면 된다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINYL),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SEAWATER_BOTTLE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SIMPLE_DISTILLER_KIT,  # const.py에 추가 필요
                        "description": "간이 정수기를 설치할 수 있는 재료 모음이다. (비닐 + 바닷물 병)",
                    },
                ),
            ],
        ),
        # 바닷물이 없는 병으로 시도했을 때의 피드백
        Combination(
            targets=[KeywordId.VINYL, KeywordId.PLASTIC_BOTTLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="정수기를 만들려면 증발시킬 물이 필요하다. 페트병에 먼저 바닷물을 담아와야 한다.",
                ),
            ],
        ),
        # 바닷물 병 + 모래사장 (비닐 없이) -> 네거티브 피드백
        Combination(
            targets=[KeywordId.SEAWATER_BOTTLE, KeywordId.SANDY_BEACH],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SEAWATER_BOTTLE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "뜨거운 모래 위에 바닷물을 그냥 붓겠다고? 그건 **천일염**을 만드는 방법이지 식수를 얻는 방법이 아니다.\n\n"
                        "순식간에 증발해 버릴 수증기를 포집하려면, 위를 덮을 장치가 반드시 필요하다.\n\n"
                        "귀한 물을 땅에 버리는 멍청한 짓은 하지 말자."
                    ),
                ),
            ],
        ),
        # 6) [신규] 간이 정수기 키트 + 모래 = 정수기 설치
        Combination(
            targets=[KeywordId.SIMPLE_DISTILLER_KIT, KeywordId.SANDY_BEACH],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SIMPLE_DISTILLER_KIT),
                Condition(type=ConditionType.STATE_IS, target="distiller_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "양지바른 모래사장에 구덩이를 파고, 바닷물이 든 페트병을 가운데 두었다.\n\n"
                        "그 위를 비닐로 덮고 가장자리를 모래로 덮어 밀봉한 뒤, 중앙에 작은 돌을 올렸다.\n\n"
                        "태양열 증류기가 완성되었다! 이제 기다리면 식수가 모일 것이다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SIMPLE_DISTILLER_KIT),
                Action(type=ActionType.UPDATE_STATE, value={"key": "distiller_built", "value": True}),
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.DISTILLER),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="베이스캠프에 **[정수기]**가 설치되었습니다. 이제 물을 모을 수 있습니다.",
                ),
            ],
        ),
        # 1) [수정] 숲 입구 + 소방 도끼 = 덩굴 획득 & 길 개척
        Combination(
            targets=[KeywordId.FOREST_ENTRY, KeywordId.FIRE_AXE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="forest_cleared", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[소방 도끼]**를 휘둘러 억센 덩굴들을 베어냈다. *퍼억! 툭!*\n\n"
                        "길을 막고 있던 덩굴들이 잘려나가며 사람이 지나갈 만한 통로가 확보되었다.\n\n"
                        "바닥에 떨어진 **[덩굴 줄기]**는 쓸만해 보여서 몇 개 챙겼다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.VINE_STEM,
                        "description": "단단하고 질긴 덩굴 줄기다. 뭔가를 묶거나 임시 로프로 쓰기 좋다.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "forest_cleared", "value": True}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "vines_collected", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 **[숲 입구]**로 진입할 수 있습니다."),
            ],
        ),
        # 2) [수정] 야자수 + 소방 도끼 = 코코넛 획득
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.FIRE_AXE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="coconut_obtained", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[소방 도끼]**로 야자수 기둥을 힘껏 내리찍었다. *쾅!* \n\n"
                        "나무 전체가 휘청거리더니, 꼭대기에서 **[코코넛]**이 툭 하고 떨어졌다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.COCONUT, "description": "단단한 껍질의 열매."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "coconut_obtained", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.PALM_TREE, "state": KeywordState.UNSEEN}
                ),
            ],
        ),
        # 3) [수정] 야자수 + 스패너 = 네거티브 피드백 (획득 불가)
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.SPANNER],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**를 던져 보았지만, 야자수 껍질에 흠집만 내고 튕겨 나왔다.\n\n"
                        "이 정도 충격으로는 열매가 떨어지지 않는다. 더 무겁고 강력한 도구가 필요하다."
                    ),
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.PALM_TREE, KeywordId.FIRE_AXE],
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
        # 양자 가마솥 수리 조합들
        # ==========================
        # (A) 부품이 모두 모이기 전에 조립 시도 → 부정 피드백 (석영/배터리/전선 공통)
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.QUARTZ_SHARD),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "석영 조각을 손에 쥐고 소켓을 바라보다가, 당신은 잠시 멈칫한다.\n\n"
                        "이 한 조각만 억지로 끼워 넣기엔, 아직 양자 가마솥 안쪽이 너무 많은 빈자리로 가득 차 있다.\n"
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
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.CHARGED_HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
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
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "배터리를 들어 단자에 가져가 보지만, "
                        "완전히 충전되지 않은 상태의 배터리로는 양자 가마솥를 작동시킬 수 없을 것 같다.\n"
                    ),
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="아직 필요한 부품들이 모두 모이지 않았습니다. 세 가지 부품을 모두 모은 뒤 다시 조립을 시작하세요.",
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.LONG_WIRE_FREE_END],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=False),
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
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.QUARTZ_SHARD],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_quartz_connected", value=False),
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
                    value={"key": "quantum_quartz_connected", "value": True},
                ),
            ],
        ),
        # (C) 부품이 모두 모인 뒤 실제 연결: 충전된 산업용 배터리
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.CHARGED_HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_battery_connected", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CHARGED_HEAVY_BATTERY),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "충전된 산업용 배터리를 주 전원 단자에 밀어 넣는다.\n\n"
                        "단자가 맞물리는 순간, 양자 가마솥 내부 어딘가에서 묵직한 ‘탁’ 하는 소리가 난다.\n"
                        "한동안 돌려 두었던 수력 발전기의 시간이, 이제 이 한 기계의 심장으로 흘러들어온다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.CHARGED_HEAVY_BATTERY,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "quantum_battery_connected", "value": True},
                ),
            ],
        ),
        # (D) 부품이 모두 모인 뒤 실제 연결: 기다란 전선 끝
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.LONG_WIRE_FREE_END],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_all_parts_gathered", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_wire_connected", value=False),
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
                    value={"key": "quantum_wire_connected", "value": True},
                ),
            ],
        ),
        # (E) 양자 가마솥 + 스패너 : 최종 조임 & 발진 여부 확인
        #   - 먼저 '모든 부품이 연결된 경우'를 만족하는 조합을 위에 두고,
        #     그렇지 않을 때는 아래의 부정 피드백 조합이 동작하도록 순서를 조절한다.
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_quartz_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_battery_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_wire_connected", value=True),
                Condition(type=ConditionType.STATE_IS, target="quantum_launched", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.REQUEST_CONFIRMATION,
                    value={
                        "prompt": (
                            "스패너를 손에 쥐고 양자 가마솥의 마지막 볼트들을 하나씩 조여 나간다.\n\n"
                            "석영은 제자리를 찾았고, 배터리는 숨을 고르고 있으며, 전선은 능선 위 안테나와 이곳을 단단히 이어 주고 있다.\n"
                            "이제, 이 기계를 다시 한 번 세상으로 던져 보낼 수 있다.\n\n"
                            "양자 가마솥를 기동해 새로운 목적지로 향하시겠습니까?\n"
                            "이 선택 이후에는, 더 이상 이 섬으로 돌아오지 못할 수도 있습니다."
                        ),
                        "confirm_actions": [
                            Action(
                                type=ActionType.PRINT_NARRATIVE,
                                value=(
                                    "마지막 볼트를 조여 고정하자, 양자 가마솥 내부에서 저속 모터가 도는 소리가 서서히 커져 간다.\n\n"
                                    "계기판의 불빛들이 하나둘 살아나고, 안테나를 타고 올라간 신호가 어딘가 먼 곳을 향해 날아간다.\n"
                                    "당신은 조용히 숨을 고른 뒤, 기체 안으로 몸을 밀어 넣는다."
                                ),
                            ),
                            Action(
                                type=ActionType.UPDATE_STATE,
                                value={"key": "quantum_launched", "value": True},
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
                                    "스패너를 잠시 내려놓고 양자 가마솥 옆에 선다.\n"
                                    "지금 이 선택이 마지막일지도 모른다는 생각이 머릿속을 맴돈다.\n"
                                    "조금 더 정리하고, 천천히 마음을 고르기로 한다."
                                ),
                            )
                        ],
                    },
                )
            ],
        ),
        # (F) 양자 가마솥 + 스패너 : 아직 부품이 덜 연결된 경우 → 부정 피드백
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="quantum_launched", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너를 쥐고 양자 가마솥의 패널을 바라보다가, 당신은 손을 멈춘다.\n\n"
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
        Combination(
            targets=[KeywordId.SANDY_BEACH, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.AIR_DUSTER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "치익-! 뜨거운 모래사장을 향해 비장하게 먼지 제거제를 분사했다.\n\n"
                        "모래알이 사방으로 튀어 오르며 내 얼굴을 강타했다.\n\n"
                        "이 광활한 해변의 모래를 이걸로 다 치우려면, 우주가 멸망할 때까지 뿌려도 모자랄 것이다.\n\n"
                        "괜히 눈에 모래만 들어갔다."
                    ),
                ),
            ],
        ),
        # [신규] 먼지 제거제 + 양자 가마솥 (실패)
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.AIR_DUSTER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "기계 틈새의 먼지라도 털어볼까 싶어 '치익-' 하고 뿌려보았다.\n\n"
                        "검은 연기가 잠시 흩어지나 싶더니, 매캐한 그을음이 역류해서 뿜어져 나왔다. 쿨럭!\n\n"
                        "이건 먼지 문제가 아니다. 물리적으로 '박살'이 난 거다.\n\n"
                        "본체 케이스가 찌그러졌는데 먼지를 털어봤자 성능은 그대로다."
                    ),
                ),
            ],
        ),
        # [신규] 코코넛 껍질에 바닷물 담기
        Combination(
            targets=[KeywordId.SEA, KeywordId.COCONUT_SHELL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="코코넛 껍질을 바닷물에 담가 찰랑거리게 채웠습니다. 꽤 튼튼한 그릇 역할을 합니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT_SHELL),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SEAWATER_FILLED_COCONUT,  # "바닷물이 담긴 코코넛 껍질"
                        "description": "바닷물이 가득 담긴 코코넛 껍질입니다. 짭짤한 냄새가 납니다.",
                    },
                ),
            ],
        ),
        # [신규] 정수기 + 코코넛 껍질 (실패 - 용도 부적합)
        Combination(
            targets=[KeywordId.DISTILLER, KeywordId.COCONUT_SHELL],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="distiller_built", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "정수기에서 떨어지는 물방울은 겨우 한 모금 분량입니다.\n\n"
                        "이 커다란 코코넛 껍질을 채우기엔 턱없이 부족합니다.\n\n"
                        "차라리 저 넘실거리는 바닷물을 한가득 퍼 나르는 용도로 쓰는 게 낫겠습니다."
                    ),
                ),
            ],
        ),
    ],
)
