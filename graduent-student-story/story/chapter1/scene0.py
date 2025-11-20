from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID, CombinationType
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
        "mk_inspected": False,  # 기계 조사 여부
        "comm_connected": False,  # 통신 연결 여부
        "sand_inspected": False,  # [추가] 모래 조사 여부 확인용 변수
    },
    # 씬 진입 시 자동 저장 (체크포인트 생성)
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),  # 체력 UI 켜기!
        Action(type=ActionType.SAVE_CHECKPOINT, value=None),
        Action(
            type=ActionType.PRINT_SYSTEM,
            value="[System] 낯선 환경에 진입했습니다. 현재 상태가 **체크포인트**에 저장됩니다.",
        ),
        Action(type=ActionType.PRINT_SYSTEM, value="[Tip] 체력이 0이 되면 이 지점에서 다시 시작합니다."),
    ],
    keywords={
        KeywordId.SANDY_BEACH: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SAND),
        # 1. MK-II: [수정] 초기 상태 HIDDEN으로 변경
        KeywordId.MK_II: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # 시야 목록에 안 뜸. 직접 입력해서 발견해야 함.
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="mk_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "기계는 엉망진창이다. 외장 패널은 찌그러졌고 엔진 쪽에서 검은 연기가 난다.\n"
                                "다행히 내부 회로는 살아있는지, 계기판 안쪽에서 통신기의 불빛이 깜빡거리고 있다."
                            ),
                        ),
                        # 통신기를 발견 상태로 변경 (시스템적으로는 발견되지만, 힌트는 주지 않음)
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.COMMS, "state": KeywordState.HIDDEN},
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="새로운 상호작용 대상이 발견되었습니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "mk_inspected", "value": True}),
                    ],
                ),
                Interaction(
                    # 이미 조사한 후
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="찌그러진 고철 덩어리처럼 보인다. 엔진 열기가 뜨거워 가까이 가기 힘들다.",
                        )
                    ]
                ),
            ],
        ),
        # 2. 통신기: 챕터 시작을 위한 필수 오브젝트
        KeywordId.COMMS: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # MK-II 조사 전에는 안 보임
            description="지직거리는 잡음이 들린다. 교수님의 목소리일까, 아니면 저승에서 부르는 소리일까. 고치려면 무언가 단단한 게 필요하다.",
        ),
        # 3. 바다: 함정 (체력 시스템 튜토리얼)
        KeywordId.SEA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # [수정] 텍스트에 있으므로 HIDDEN으로 시작해 발견의 재미 부여
            description="끝없이 펼쳐진 수평선. 보기에는 시원해 보이지만, 마시면 죽을 것이다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "목이 너무 말라 바닷물이라도 마시려 손을 뻗었다.\n"
                                "...윽! 혀가 아릴 정도로 짜다. 구역질이 올라오며 오히려 더 목이 마르다."
                            ),
                        ),
                        # 체력 감소 액션
                        Action(type=ActionType.MODIFY_STAMINA, value=-10),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="[경고] 짠물을 마셔 체력이 감소했습니다. 잘못된 행동은 생명을 위협합니다.",
                        ),
                    ]
                )
            ],
        ),
        # 4. 태양: 환경 묘사
        KeywordId.SUN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,  # [수정] 마찬가지로 HIDDEN
            description="머리 꼭대기에서 이글거린다. 가만히 서 있어도 수분이 증발하는 기분이다.",
        ),
        KeywordId.SKY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "구름 한 점 없이 맑다. 랩실 구석 창문으로 보던 네모난 하늘과는 다르다.\n"
                "너무 광활해서 오히려 공포감이 든다. 교수가 없는 하늘은 이렇게나 넓구나."
            ),
        ),
        KeywordId.SAND: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 첫 번째 조사: 설명만 출력하고 상태 변경
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="sand_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "손을 대자마자 화상을 입을 뻔했다. 삼겹살을 올려두면 3초 만에 마이야르 반응이 일어날 온도다.\n"
                                "신발 밑창이 녹기 전에 그늘을 찾아야 한다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "sand_inspected", "value": True}),
                    ],
                ),
                # 두 번째 이후: 데미지 입음
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다시 만져봐도 여전히 뜨겁다. 호기심이 고양이를 죽이고 대학원생을 태운다.",
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-5),
                        Action(type=ActionType.PRINT_SYSTEM, value="[경고] 뜨거운 모래에 데여 체력이 감소했습니다."),
                    ]
                ),
            ],
        ),
    },
    combinations=[
        # 통신기 + 스패너 -> 씬 이동
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
                        "**[스패너]**로 **[통신기]**를 쾅! 내려쳤다.\n"
                        "지지직... 삐- 소리와 함께 익숙한 목소리가 터져 나온다.\n\n"
                        '교수님: "아아, 마이크 테스트. 야! 들리냐? 너 거기 좌표가 왜 이래?"\n'
                        '나: "교수님! 여기 무인도 같은데요?!"\n'
                        '교수님: "GPS가 고장 났어. 거기가 어딘진 모르겠지만, 일단 살아서 돌아와야 논문 쓸 거 아니야?"\n'
                        '교수님: "MK-II 엔진 좀 식히고 배터리 충전해서 다시 가동해. 아, 통신비 비싸니까 용건만 해라. 끊는다."'
                    ),
                ),
                Action(type=ActionType.PRINT_SYSTEM, value="[목표 갱신] 1. 깨끗한 물 구하기 / 2. MK-II 수리하기"),
                Action(type=ActionType.UPDATE_STATE, value={"key": "comm_connected", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 본격적으로 섬을 탐색하기 위해 이동합니다."),
                # 다음 씬으로 이동
                Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
            ],
        )
    ],
)
