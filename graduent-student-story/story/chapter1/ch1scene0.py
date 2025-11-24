from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE0_DATA = SceneData(
    id=SceneID.CH1_SCENE0,
    name="이름 모를 해변 (불시착)",
    initial_text=(
        "---\n"
        "# Chapter 1\n"
        "## 과학적 생존법\n"
        "---\n\n"
        "쿠당탕!!\n"
        "엄청난 굉음과 함께 엉덩이에 전해지는 고통. 전두엽까지 울리는 충격에 정신이 아득하다.\n\n"
        "눈을 떠보니 익숙한 회색 랩실 천장이 아니라, 눈이 시릴 만큼 파란 하늘과 작열하는 태양이 보인다.\n\n"
        '"...살아 있나?"\n\n'
        "속이 울렁거린다. 옆에는 MK-II가 모래사장에 꼴사납게 처박혀 검은 연기를 내뿜고 있다. "
        "주변은 온통 망망대해. 바다뿐이다. "
        "덥다. 너무 덥다. 에어컨이 고장 난 8월의 서버실보다 더 덥다."
    ),
    initial_state={
        "mk_inspected": False,
        "comm_connected": False,
        "comm_found": False,
        "sea_step": 0,
        "sand_step": 0,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
        Action(type=ActionType.SAVE_CHECKPOINT, value=None),
        Action(
            type=ActionType.PRINT_SYSTEM,
            value="[System] 낯선 환경에 진입했습니다. 현재 상태가 **체크포인트**에 저장됩니다.",
        ),
        Action(
            type=ActionType.PRINT_SYSTEM,
            value="[System] 오른쪽 상단에 체력이 생겼습니다. 이제 체력을 신경쓰면서 움직여야 합니다.",
        ),
        Action(type=ActionType.PRINT_SYSTEM, value="[Tip] 체력이 0이 되면 이 지점에서 다시 시작합니다."),
    ],
    keywords={
        KeywordId.SANDY_BEACH: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SAND),
        KeywordId.MK_II: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="mk_inspected", value=False),
                        Condition(type=ConditionType.STATE_IS, target="comm_found", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기계는 엉망진창이다. 외장 패널은 찌그러졌고 엔진 쪽에서 검은 연기가 난다.\n"
                                "내부를 들여다보니 다행히 핵심 부품은 무사한 것 같다.\n"
                                "특히 계기판 안쪽에서 **[통신기]**라고 적힌 모듈의 붉은 LED가 깜빡거리고 있다. 아직 작동하는 것 같다!"
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.COMMS, "state": KeywordState.HIDDEN},
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="**[통신기]**를 조사할 수 있게 되었습니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "mk_inspected", "value": True}),
                    ],
                ),
                Interaction(
                    # 이미 조사한 후
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="찌그러진 고철 덩어리처럼 보이지만, 내부는 아직 살아있다. **[통신기]** 쪽을 좀 더 살펴봐야 한다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.COMMS: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            # 힌트 강화: 도구 사용 유도
            description="전선이 끊어져 지직거리는 소리만 난다. 단단한 **[도구]**로 커버를 뜯어내고 내부 회로를 다시 연결하면 될 것 같다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(type=ActionType.UPDATE_STATE, value={"key": "comm_found", "value": True}),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="지지직... 거리는 잡음 사이로 희미하게 사람 목소리가 들린다. **[스패너]** 같은 걸로 고칠 수 있을까?",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.SEA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sea_step", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="끝없이 펼쳐진 수평선. 바닷물이 시원해 보인다. 한 모금 정도 마셔볼까?",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sea_step", "value": 1}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sea_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "목이 너무 말라 바닷물이라도 마시려 손을 뻗었다.\n"
                                "...윽! 혀가 아릴 정도로 짜다. 구역질이 올라오며 오히려 더 목이 마르다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-10),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="[경고] 짠물을 마셔 체력이 감소했습니다. 잘못된 행동은 생명을 위협합니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sea_step", "value": 2}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sea_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="바닷물은 마시면 안 된다. 이건 상식이다. 상식이 부족하면 몸이 고생한다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.SUN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="머리 꼭대기에서 이글거린다. 가만히 서 있어도 수분이 증발하는 기분이다.",
        ),
        KeywordId.SKY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="구름 한 점 없이 맑다. 너무 광활해서 오히려 공포감이 든다. 교수가 없는 하늘은 이렇게나 넓구나.",
        ),
        KeywordId.SAND: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_step", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "손을 대자마자 화상을 입을 뻔했다. 삼겹살을 올려두면 3초 만에 마이야르 반응이 일어날 온도다.\n"
                                "신발 밑창이 녹기 전에 그늘을 찾아야 한다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sand_step", "value": 1}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다시 만져봐도 여전히 뜨겁다. 호기심이 고양이를 죽이고 대학원생을 태운다.",
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-5),
                        Action(type=ActionType.PRINT_SYSTEM, value="[경고] 뜨거운 모래에 데여 체력이 감소했습니다."),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="여기서 모래를 더 만질 일은 없다. 찜질방 불가마가 그립다.",
                        ),
                    ],
                ),
            ],
        ),
    },
    combinations=[
        # [수정] 통신기 + 스패너: 수리 시도 -> 희망 -> 절망(폭발) -> 씬 이동
        Combination(
            targets=[KeywordId.COMMS, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="comm_connected", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**로 찌그러진 커버를 뜯어내고 끊어진 전선을 억지로 이었다. 배터리 단자를 조이자 기계음이 들린다.\n\n"
                        "[System] 자가 수리 프로토콜 가동... 엔진 냉각 시작.\n\n"
                        "[System] 태양광 충전 모듈 전개. 배터리 충전 중...\n\n"
                        "성공이다! 펜이 힘차게 돌아가며 통신기에 불이 들어왔다.\n"
                        '교수님: "아아, 들리냐? 야! MK-II 상태 어때? 엔진 고치고 배터리만 충전하면 다시 날아오를 수 있어!"\n\n'
                        '나: "교수님! 성공입니다! 지금 충전 시작했..."\n\n'
                        "**퍼버벅-!!!**\n\n"
                        "말이 끝나기도 전에 통신기에서 시커먼 연기와 함께 불꽃이 튀었다. 과부하다.\n"
                        '교수님: "어? 야! 잠깐만! 통신기 꺼야... 끊긴다! 살아남아라!"\n\n'
                        "통신 모듈이 완전히 새까맣게 타버렸다. 더 이상 쓸 수 없다. "
                    ),
                ),
                Action(type=ActionType.PRINT_SYSTEM, value="[목표 갱신] 1. MK-II 수리 재료 찾기"),
                Action(type=ActionType.UPDATE_STATE, value={"key": "comm_connected", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 본격적으로 섬을 탐색하기 위해 이동합니다."),
                Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
            ],
        ),

        # [추가] 네거티브 피드백: MK-II 본체 + 스패너
        Combination(
            targets=[KeywordId.MK_II, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="기계 본체를 **[스패너]**로 두들겨 봤자 찌그러진 외장만 더 찌그러질 뿐이다. 수리가 필요한 건 내부의 통신기다."
                )
            ]
        ),

        # [추가] 네거티브 피드백: 바다 + 스패너
        Combination(
            targets=[KeywordId.SEA, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="바다를 향해 **[스패너]**를 휘둘러 보았다. 파도를 고칠 수는 없다."
                )
            ]
        ),

        # [추가] 네거티브 피드백: 태양 + 스패너
        Combination(
            targets=[KeywordId.SUN, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="태양을 향해 **[스패너]**를 들어 올렸다. 눈만 부시다. 쓸데없는 짓으로 체력을 낭비하지 말자."
                )
            ]
        ),
    ],
)
