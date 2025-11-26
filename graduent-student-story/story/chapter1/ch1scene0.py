from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE0_DATA = SceneData(
    id=SceneID.CH1_SCENE0,
    name="이름 모를 해변 (불시착)",
    initial_text="---\n# Chapter 1\n## 과학적 생존법\n---\n\n",
    body=(
        "쿠당탕!!\n"
        "엄청난 굉음과 함께 엉덩이에 전해지는 고통. 전두엽까지 울리는 충격에 정신이 아득하다.\n\n"
        "눈을 떠보니 익숙한 회색 랩실 천장이 아니라, 눈이 시릴 만큼 파란 하늘과 작열하는 태양이 보인다.\n\n"
        '"...살아 있나?"\n\n'
        "속이 울렁거린다. 옆에는 양자 가마솥이 모래사장에 꼴사납게 처박혀 검은 연기를 내뿜고 있다.\n\n"
        "주변은 온통 망망대해. 바다뿐이다.\n\n"
        "덥다. 너무 덥다. 에어컨이 고장 난 8월의 서버실보다 더 덥다."
    ),
    initial_state={
        "quantum_inspected": False,
        "sea_step": 0,
        "sand_step": 0,
        "antenna_found": False,
        "comms_exploded": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
        Action(type=ActionType.SAVE_CHECKPOINT, value=None),
        Action(
            type=ActionType.PRINT_SYSTEM,
            value=(
                "⚠️ **[System] 낯선 차원에 진입했습니다.**\n\n"
                "현재 시공간 좌표가 **[체크포인트]**로 저장되었습니다.\n"
                "우측 상단에 **[체력]** 게이지가 활성화됩니다. 무리한 행동으로 체력이 0이 되면, 시간은 다시 이곳으로 되감깁니다."
            ),
        ),
    ],
    keywords={
        KeywordId.SANDY_BEACH: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SAND),
        KeywordId.QUANTUM_CAULDRON: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="quantum_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기계는 엉망진창이다. 외장 패널은 찌그러졌고 엔진 쪽에서 검은 연기가 난다.\n\n"
                                "내부를 들여다보니 다행히 핵심 부품은 무사한 것 같다.\n\n"
                                "하지만 **[통신기]** 모듈 쪽이 심하게 파손되어 있다."
                            ),
                        ),
                        Action(
                            type=ActionType.DISCOVER_KEYWORD,
                            value=KeywordId.COMMS,
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "quantum_inspected", "value": True}),
                    ],
                ),
                Interaction(
                    # 이미 조사한 후
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("찌그러진 고철 덩어리처럼 보이지만, 내부는 아직 살아있다.\n\n"
                                  "**[통신기]**를 살려내야 구조 요청이라도 할 수 있다."),
                        )
                    ]
                ),
            ],
        ),
        KeywordId.COMMS: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="comms_exploded", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "상태가 심각하다. 신호를 잡을 안테나가 통째로 부러져 사라졌다.\n\n"
                                "충격으로 인해 근처 어딘가에 파묻힌 것 같다.\n\n"
                                "부품을 찾아서 다시 끼워 넣어야 한다."
                            ),
                        ),
                    ]
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="comms_exploded", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("새까맣게 타버린 통신기다. 더 이상 작동하지 않는다.\n\n"
                                  "교수님의 마지막 말을 기억해야 한다."),
                        ),
                    ]
                ),
            ],
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
                                "손을 대자마자 화상을 입을 뻔했다. 삼겹살을 올려두면 3초 만에 마이야르 반응이 일어날 온도다.\n\n"
                                "신발 밑창이 녹기 전에 그늘을 찾아야 한다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sand_step", "value": 1}),
                    ],
                ),
                # [수정] 맨손으로 만지면 무조건 화상 (도구 사용 유도)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "맨손으로 모래를 파헤치려다 비명을 지를 뻔했다.\n"
                                "삼겹살 불판 수준으로 뜨겁다. 맨손으로는 무리다. 무언가 **도구**를 이용해 파봐야 한다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-5),
                        Action(type=ActionType.PRINT_SYSTEM, value="[경고] 뜨거운 모래에 데여 체력이 감소했습니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sand_step", "value": 2}),
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
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_step", value=3)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="이미 **[안테나]**를 찾았다. 굳이 이 지옥불 같은 모래사장을 더 뒤지고 싶지는 않다.",
                        ),
                    ],
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
                            value="목이 너무 말라 바닷물이라도 마시려 손을 뻗었다. ...윽! 혀가 아릴 정도로 짜다.",
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-5),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="[경고] 짠물을 마셔 체력이 감소했습니다. 갈증이 더 심해집니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sea_step", "value": 2}),
                    ],
                ),
            ],
        ),
        # [신규] 그늘진 해변 (다음 씬 이동 포탈)
        KeywordId.SHADY_BEACH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.INACTIVE, # 통신기 폭발 후 활성화
            description="해변 가장자리에 거대한 바위 절벽이 만든 그늘이 있다. 저기라면 타죽지 않고 가마솥을 점검할 수 있을 것 같다.",
            interactions=[
                # [수정] 이동 시 예/아니오 확인
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "양자 가마솥을 끌고 **[그늘진 해변]**으로 이동하시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "통신기는 망가졌지만, **[양자 가마솥]** 본체는 무사하다.\n\nn"
                                            "다른 잡동사니를 챙길 여력은 없다. 오직 이 기계만이 나의 유일한 희망이다."
                                        ),
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 이곳에서 더 조사할 것이 남았을지도 모른다. 잠시 숨을 고른다.",
                                    ),
                                ],
                            },
                        ),
                    ]
                )
            ]
        ),
        # --- 배경/분위기용 UNSEEN 오브젝트 (게임 플레이에 영향 없음) ---
        "태양": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="머리 꼭대기에서 이글거린다. 가만히 서 있어도 수분이 증발하는 기분이다.",
        ),
        "하늘": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="구름 한 점 없이 맑다. 너무 광활해서 오히려 공포감이 든다. 교수가 없는 하늘은 이렇게나 넓구나.",
        ),
    },
    combinations=[
        # [수정] 모래 + 스패너 = 안테나 획득 (안전한 탐색)
        Combination(
            targets=[KeywordId.SAND, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="antenna_found", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**를 이용해 기계 주변의 뜨거운 모래를 파헤쳤다.\n"
                        "한참을 휘젓자 '틱' 하는 금속음이 들린다.\n"
                        "모래 속에서 반짝이는 부품을 건져 올렸다. 부러진 **[안테나]**다!"
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.ANTENNA, "description": "통신기의 부러진 안테나 부품이다."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "antenna_found", "value": True}),
                Action(type=ActionType.UPDATE_STATE, value={"keyword": "sand", "state": KeywordState.UNSEEN}),
            ],
        ),
        # [수정] 안테나 + 통신기 = 이벤트 발생 (수리 과정 없이 즉시 진행)
        Combination(
            targets=[KeywordId.COMMS, KeywordId.ANTENNA],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ANTENNA)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "부러진 **[안테나]**를 통신기 홈에 맞춰 끼워 넣자마자, 갑자기 기계가 웅웅거리며 작동하기 시작한다!\n\n"
                        '교수님: "아아, 들리냐? 야! 양자 가마솥 상태 어때? **배터리 충전하고, 발진기 고치고, 통신선만 연결하면** 다시 날아오를 수 있어!"\n\n'
                        '나: "교수님! 그게 무슨...!"\n\n'
                        "**퍼버벅-!!!**\n\n"
                        "말이 끝나기도 전에 통신기에서 시커먼 연기와 함께 불꽃이 튀었다.\n\n"
                        '교수님: "어? 야! 잠깐만! 통신기 꺼야... 끊긴다! 살아남아라!"\n\n'
                        "통신 모듈이 완전히 새까맣게 타버렸다.\n\n"
                        "태양은 점점 더 뜨거워진다. 여기서 멍하니 있다간 통구이가 될 것이다.\n\n"
                        "저 멀리 보이는 **[그늘진 해변]**으로 가마솥을 옮겨야 한다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ANTENNA),
                Action(type=ActionType.UPDATE_STATE, value={"key": "comms_exploded", "value": True}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "sand_step", "value": 3}),
                Action(type=ActionType.PRINT_SYSTEM, value="[목표 갱신] 1. **[그늘진 해변]**으로 가마솥 옮기기"),
                Action(type=ActionType.DISCOVER_KEYWORD, value="그늘진 해변"), # 이동 포인트 발견
            ],
        ),
    ],
)