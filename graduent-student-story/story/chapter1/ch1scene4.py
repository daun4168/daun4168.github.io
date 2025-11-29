from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE4_DATA = SceneData(
    id=SceneID.CH1_SCENE4,
    name="공명하는 숲 (생태 관측소)",
    body=(
        "모래사장에서 숲 입구를 지나 북쪽으로 조금 더 걸어가자, 공기부터 달라진다.\n"
        "짙은 초록빛 그림자가 드리운 숲의 입구. 빛과 소리가 뒤섞여 머릿속까지 울린다.\n\n"
        "숲 한가운데에는 낡은 생태 관측소 건물이 반쯤 덩굴에 먹힌 채 서 있고, "
        "관측소 앞쪽에는 예전에 누군가 손질했던 흔적이 남아 있는 작은 화단이 보인다.\n"
        "건물 벽면은 촘촘한 덩굴에 뒤덮여 있어 안쪽이 거의 보이지 않는다.\n\n"
        "관측소 옆에는 하늘로 곧게 뻗은 나무 한 그루가 서 있고, 높은 가지 위에 작은 새 한 마리가 내려앉아 있다.\n"
        "새는 일정한 간격으로 몇 번 울어 대다가 잠시 숨을 고른 뒤, 다시 비슷한 패턴을 반복하는 것처럼 들린다.\n"
        "관측소 뒤편으로는 습한 공기와 썩은 물 냄새가 희미하게 풍기는 좁은 길이 나 있는데, "
        "아마도 늪지대로 가는 길인 것 같다."
    ),
    initial_state={
        "labdoor_unlocked": False,
        "locker_opened": False,
        "mic_fixed": False,
        "mic_stage": 0,
        "pipe_step": 0,
        "forest_entrance_inspected": False,
        "vines_cleared": False,
        "swamp_path_inspected": False,
    },
    on_enter_actions=[
        Action(type=ActionType.SHOW_STAMINA_UI, value=True),
    ],
    keywords={
        KeywordId.SWAMP_PATH_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SWAMP_PATH),
        # 되돌아가는 길: 숲 입구 -> 베이스캠프
        KeywordId.FOREST_ENTRY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            description=None,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="forest_entrance_inspected",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "숲 가장자리, 나뭇가지 사이로 해변 쪽 하얀 모래와 야자수 그늘이 멀리 보인다.\n"
                                "그쪽으로 한참 내려가면 다시 베이스캠프로 돌아갈 수 있을 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="다시 한번 숲 입구를 입력하면 베이스캠프로 돌아갈지 물어봅니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "forest_entrance_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="forest_entrance_inspected",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "숲 입구 쪽으로 되돌아가 해변 베이스캠프로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 숲의 그늘을 벗어나 다시 뜨거운 모래사장으로 내려간다.",
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE1,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 이 숲에서 할 일이 남은 것 같다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 늪지대로 가는 길: Scene5 포탈 (락커를 열어야 통과 가능)
        KeywordId.SWAMP_PATH: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 락커를 아직 열지 않았을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "관측소 뒤편으로 이어진 좁은 길 끝에서 축축한 흙냄새와 썩은 물 냄새가 올라온다.\n"
                                "아마도 이 길을 따라가면 늪지대로 내려갈 수 있을 것 같다.\n"
                                "하지만 지금 가진 장비만으로는 그쪽을 헤쳐 나가기에 준비가 부족해 보인다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="먼저 관측소 안을 조사해 보급품 로커를 열고 장비를 갖추는 편이 좋겠습니다.",
                        ),
                    ],
                ),
                # 락커를 열어 보급품을 챙긴 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "늪지대로 가는 길을 따라 맹독 늪지대로 내려가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "당신은 관측소를 한 번 뒤돌아본 뒤, "
                                            "축축한 공기가 감도는 좁은 길을 따라 서서히 아래로 내려가기 시작한다."
                                        ),
                                    ),
                                    Action(
                                        type=ActionType.MOVE_SCENE,
                                        value=SceneID.CH1_SCENE5,
                                    ),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직은 숲과 관측소 주변을 조금 더 살펴보고 싶다.",
                                    )
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 나무 (새소리 패턴 힌트) — const에서 KeywordId.TREE = "나무"
        KeywordId.TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "관측소 옆 나무 위쪽으로 시선을 올려다보면, 높은 가지에 작은 새 한 마리가 앉아 있다.\n"
                "첫 울림은 길고 묵직하게 깔리더니, 곧이어 두 번 가볍게 튀어 오르는 짧은 울음이 뒤를 따른다.\n"
                "잠시 숨을 고른 듯한 정적 뒤에, 다시 한 번 길고 여운 있는 울음이 퍼지고, "
                "마지막으로 또 한 번 짧고 날카로운 소리가 잽싸게 끼어든다.\n\n"
                "숲 전체가 이 다섯 번의 리듬을 시간을 대신하는 박자처럼 반복되고 있다."
            ),
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "나무 위의 새가 다시 울기 시작한다.\n"
                                "길고 묵직한 울림 하나, 가볍게 튀는 짧은 소리 둘, "
                                "다시 길게 이어지는 울림 하나, 마지막으로 짧게 튀는 소리 하나가 귀에 또렷하게 박힌다."
                            ),
                        )
                    ]
                )
            ],
        ),
        # 생태 관측소 외관
        KeywordId.ECO_OBSERVATORY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                # 덩굴이 아직 있을 때
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="vines_cleared",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "나무들 사이로 건물의 윤곽이 어렴풋이 보인다.\n"
                                "시멘트 외벽과 문이 있을 것 같은 위치는 감이 오지만, "
                                "두꺼운 덩굴과 잎이 그 위를 완전히 뒤덮고 있다.\n"
                                "먼저 이 덩굴부터 어떻게든 치워야 관측소가 어떤 상태인지 확인할 수 있을 것 같다."
                            ),
                        )
                    ],
                ),
                # 덩굴을 치운 뒤
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="vines_cleared",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "덩굴이 걷히자 관측소 외벽이 드러난다.\n"
                                "이끼와 곰팡이가 얼룩진 시멘트 벽 사이로 작은 벽화가 눈에 띄고, "
                                "정면에는 전자 도어락이 달린 관측소 문이 있다.\n"
                                "문 앞쪽에는 시들어버린 꽃들이 자리만 남겨 둔 화단이 있고, "
                                "벽 한쪽에는 종이가 반쯤 찢어진 관찰 일지가 못질되어 있다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 덩굴
        KeywordId.VINE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="두꺼운 덩굴줄기가 관측소 벽면과 문틀을 칭칭 감고 있다. 맨손으로는 떼어낼 수 없을 것 같다.",
        ),
        # 벽화
        KeywordId.BOTANIST_MURAL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "![벽화 시계](assets/chapter1/flower_clock.svg)\n\n"
                "덩굴 뒤에는 커다란 시계 모양의 벽화가 숨어 있었다.\n"
                "12, 3, 6, 9시 방향 눈금이 희미하게 남아 있고, 그 사이사이에 다섯 송이의 꽃이 "
                "각기 다른 시간 위치에 그려져 있다.\n\n"
                "나팔꽃, 닭의장풀, 자귀나무, 분꽃, 달맞이꽃…\n"
                "어딘가에서 이 꽃들을 실제로 키우던 화단을 본 적이 있는 것 같다.\n\n"
                "벽 한쪽에는 누군가 남긴 듯한 낡은 관찰 일지가 박혀 있다."
            ),
        ),
        # 화단
        KeywordId.FLOWER_BED: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "작은 화단에 시들어버린 꽃들이 자리만 남겨 두고 서 있다.\n"
                "각 위치 앞에는 녹슨 금속 팻말이 꽂혀 있고, 희미한 글씨가 남아 있다.\n\n"
                "🌺 나팔꽃: 표본 번호 3\n"
                "💠 닭의장풀: 표본 번호 0\n"
                "🌿 자귀나무: 표본 번호 8\n"
                "🌸 분꽃: 표본 번호 4\n"
                "🌼 달맞이꽃: 표본 번호 1\n\n"
                "꽃 자체의 순서가 아니라, 번호들 사이의 간격을 기록하려 했던 것처럼 보인다."
            ),
        ),
        # 관찰 일지
        KeywordId.BOTANY_NOTE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '"...개화의 순서는 누구나 볼 수 있다."\n'
                '"하지만 서로 얼마나 떨어져 피었는지는, 해가 두 번은 떠야 눈치챌 수 있는 법이다."\n'
                '"나는 첫 꽃과 마지막 꽃을 책갈피처럼 꽂아두고, '
                '그 사이에서 일어나는 변화의 크기만을 기록하기로 했다."\n\n'
                "벽화의 꽃 순서와 화단의 표본 번호를 떠올리자, 슬슬 패턴이 보이기 시작한다."
            ),
        ),
        # 관측소 문
        KeywordId.OBSERVATORY_DOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=None,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="labdoor_unlocked",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "관측소 문 옆 전자 도어락이 죽은 눈으로 날 바라본다.\n"
                                "전원은 들어오지 않지만, 비밀번호를 입력하면 내부 백업 전원이 "
                                "잠깐 살아날지도 모르겠다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="관측소 문 : [4자리 비밀번호] 형식으로 입력할 수 있을 것 같다.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="labdoor_unlocked",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="문은 이미 살짝 열린 상태다. 안쪽에서 서늘한 공기가 새어 나온다.",
                        )
                    ],
                ),
            ],
        ),
        # 관측소 내부
        KeywordId.OBSERVATORY_INSIDE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=None,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "관측소 문을 밀고 안으로 들어서자, 곰팡이 냄새와 함께 축축한 공기가 들이친다.\n"
                                "벽 쪽에는 금속 문짝이 달린 보급품 로커가 붙어 있고, "
                                "그 옆에는 덜렁거리는 마이크가 전선 몇 가닥에 매달려 있다.\n"
                                "천장 근처로는 긴 파이프와 짧은 파이프가 벽을 뚫고 지나가 있어, "
                                "두드리면 꽤 크게 울릴 것처럼 보인다."
                            ),
                        ),
                    ]
                )
            ],
        ),
        # 보급품 로커
        KeywordId.SUPPLY_LOCKER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=None,
            interactions=[
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "관측소 한쪽 벽에 보급품 로커가 붙어 있다.\n"
                                "문짝에는 낡은 마이크와 'Voice Pattern Lock'이라는 글자가 적혀 있다.\n"
                                "로커는 손으로는 열리지 않고, 일정한 소리 패턴을 인식해야만 열리는 구조 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="새가 내는 울음소리의 리듬을 잘 들어보는 것이 좋겠다.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=True,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="이미 비워진 로커다. 안에는 먼지와 녹슨 선반만 남아 있다.",
                        )
                    ],
                ),
            ],
        ),
        # 마이크 (단계별 수리)
        KeywordId.MICROPHONE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=None,
            interactions=[
                # 단계 0: 완전 고장
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_stage",
                            value=0,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "마이크 단자가 덜렁거리고, 케이블 피복은 군데군데 벗겨져 있다.\n"
                                "이 상태로는 소리를 제대로 전달해 줄 것 같지 않다. "
                                "먼저 나사를 조이고 케이블을 정리해야 할 것 같다."
                            ),
                        ),
                    ],
                ),
                # 단계 1: 고정은 했지만 전원 없음
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_stage",
                            value=1,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "마이크 몸체와 단자는 이제 단단히 고정되어 있다. 덜렁거리던 문제는 해결됐다.\n"
                                "하지만 표시등은 여전히 꺼져 있고, 전원이 들어오지 않는 것 같다."
                            ),
                        ),
                    ],
                ),
                # 단계 2: 완전 수리
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_stage",
                            value=2,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "마이크는 단단히 고정되어 있고, 작은 표시등이 꾸준히 불을 밝히고 있다.\n"
                                "이제는 파이프를 두드리는 소리도 문제없이 인식해 줄 것 같다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        # 긴 파이프
        KeywordId.LONG_PIPE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="벽 밖으로 길게 튀어나온 금속 파이프다. 두드리면 낮고 묵직한 울림이 날 것 같다.",
            interactions=[
                # 마이크 수리 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="파이프를 두드리자 낮고 둔탁한 울림이 퍼지지만, 로커 쪽에서는 아무 반응이 없다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="마이크가 고장난 상태에서는 아무리 두드려도 의미가 없다.",
                        ),
                    ],
                ),
                # 패턴 1단계: step == 0
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="pipe_step",
                            value=0,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="긴 파이프를 두드리자, 숲 바닥까지 울리는 낮고 묵직한 소리가 길게 깔린다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 1},
                        ),
                    ],
                ),
                # 패턴 4단계: step == 3
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="pipe_step",
                            value=3,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다시 한 번 낮은 울림이 길게 이어진다. 이제 마지막 한 음만 맞추면 될 것 같다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 4},
                        ),
                    ],
                ),
                # 다른 조합: 패턴 깨짐 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="울림이 숲의 리듬과 어딘가 어긋난 느낌이다. 처음부터 다시 시도해야 할 것 같다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 0},
                        ),
                    ],
                ),
                # 로커가 이미 열린 뒤
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="긴 파이프를 두드리자 낮은 울림이 한 번 울려 퍼질 뿐이다.",
                        )
                    ]
                ),
            ],
        ),
        # 짧은 파이프
        KeywordId.SHORT_PIPE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="짧고 두꺼운 금속 파이프다. 두드리면 밝고 날카로운 금속음이 튈 것 같다.",
            interactions=[
                # 마이크 수리 전
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=False,
                        )
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="짧은 파이프를 톡 치자 맑은 금속음이 울리지만, 로커는 반응하지 않는다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="먼저 마이크를 수리해야 소리를 인식할 수 있을 것 같다.",
                        ),
                    ],
                ),
                # 패턴 2단계: step == 1
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="pipe_step",
                            value=1,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="짧은 파이프를 치자 가볍게 튀어 오르는 소리가 한 번 울린다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 2},
                        ),
                    ],
                ),
                # 패턴 3단계: step == 2
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="pipe_step",
                            value=2,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="같은 짧은 음이 한 번 더, 조금 더 높이 튀어 오르는 느낌으로 이어진다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 3},
                        ),
                    ],
                ),
                # 패턴 5단계: step == 4 (마지막 음 + 로커 개방)
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="pipe_step",
                            value=4,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "짧은 파이프에서 마지막으로 날카롭고 가벼운 소리가 튀어나온다.\n"
                                "순간 숲속의 새 울음과 완벽하게 겹쳐지며, 공명이 일어난 듯한 기분이 든다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="관측소 안쪽에서 '철컥' 하는 자물쇠 푸는 소리가 들린다. 보급품 로커가 열린 것 같다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "locker_opened", "value": True},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 0},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.VINEGAR,
                                "description": "강한 산성 냄새가 나는 투명한 액체다. 라벨에는 '실험용 식초'라고 적혀 있다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.WATERPROOF_TAPE,
                                "description": "두껍고 끈끈한 방수 테이프다. 임시 수리용으로 안성맞춤이다.",
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산업용 배터리는 아직 사용할 수 있을 것 같다. 이제 로커는 열렸으니 챙겨두자.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.HEAVY_BATTERY,
                                "description": "한동안 마이크 전원으로 쓰였던 산업용 배터리다. 꽤 무겁지만 아직 쓸 수 있을 것 같다.",
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=(
                                "보급품 로커에서 식초와 방수 테이프를 챙겼다.\n"
                                "이제 관측소 뒤편의 늪지대로 가는 길을 따라가도 될 것 같다."
                            ),
                        ),
                    ],
                ),
                # 그 외: 패턴 깨짐 → 리셋
                Interaction(
                    conditions=[
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="mic_fixed",
                            value=True,
                        ),
                        Condition(
                            type=ConditionType.STATE_IS,
                            target="locker_opened",
                            value=False,
                        ),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="짧은 금속음이 허공에 흩어진다. 숲의 리듬과는 맞지 않는 조합인 듯하다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "pipe_step", "value": 0},
                        ),
                    ],
                ),
                # 로커가 이미 열린 뒤
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="짧은 파이프를 두드리자 가벼운 금속음이 한 번 튀어 오를 뿐이다.",
                        )
                    ]
                ),
            ],
        ),
    },
    combinations=[
        # 덩굴 제거: 소방 도끼 + 덩굴
        Combination(
            targets=[KeywordId.FIRE_AXE, KeywordId.VINE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "소방 도끼로 덩굴을 몇 번이고 찍어내자, 축축한 줄기들이 우수수 바닥으로 떨어진다.\n"
                        "덩굴이 걷히자 그 뒤로 낯익은 모양의 벽화가 모습을 드러낸다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_KEYWORD,
                    value=KeywordId.VINE,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "vines_cleared", "value": True},
                ),
                # 벽화 / 관찰 일지 / 관측소 문 / 화단 활성화 (HIDDEN)
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.BOTANIST_MURAL,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.BOTANY_NOTE,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.OBSERVATORY_DOOR,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.FLOWER_BED,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.ECO_OBSERVATORY,
                        "state": KeywordState.DISCOVERED,
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value=(
                        "새로운 상호작용 대상이 여러 개 발견되었습니다. "
                        "덩굴이 사라진 생태 관측소를 살펴보는 것이 좋습니다."
                    ),
                ),
            ],
        ),
        # 관측소 문 비밀번호: 1218
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.OBSERVATORY_DOOR, "1218"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "도어락에 숫자 1218을 입력하자, 한동안 침묵이 이어진 뒤 "
                        "짧은 부팅음과 함께 잠금 장치가 해제된다.\n"
                        "문틈 사이로 서늘한 공기와 곰팡이 냄새가 새어 나온다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "labdoor_unlocked", "value": True},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.OBSERVATORY_INSIDE,
                        "state": KeywordState.DISCOVERED,
                    },
                ),
                # 내부 오브젝트들을 HIDDEN으로 활성화
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SUPPLY_LOCKER,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.MICROPHONE,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.LONG_PIPE,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SHORT_PIPE,
                        "state": KeywordState.HIDDEN,
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="관측소 문이 열렸습니다. 관측소 내부를 입력해 안으로 들어가 볼 수 있습니다.",
                ),
            ],
        ),
        # 마이크 1단계 수리: 마이크 + 스패너
        Combination(
            targets=[KeywordId.MICROPHONE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="mic_stage", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너로 마이크 고정 나사를 하나씩 조이고, 헐거워진 브래킷을 다시 맞춰 끼웠다.\n"
                        "덜렁거리던 마이크가 제자리를 찾으며 더 이상 흔들리지 않는다."
                    ),
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mic_stage", "value": 1},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="마이크가 고정되었습니다. 이제 전원을 공급하기 위해 마이크 + 산업용 배터리를 시도해 볼 수 있습니다.",
                ),
            ],
        ),
        # 마이크 + 스패너 (이미 고정된 상태)
        Combination(
            targets=[KeywordId.MICROPHONE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mic_stage", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="마이크는 이미 단단히 고정되어 있습니다.",
                )
            ],
        ),
        # 마이크 2단계 수리: 마이크 + 산업용 배터리
        Combination(
            targets=[KeywordId.MICROPHONE, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HEAVY_BATTERY),
                Condition(type=ConditionType.STATE_IS, target="mic_stage", value=1),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "산업용 배터리를 마이크 옆 단자에 연결하자, 약간의 스파크와 함께 케이블을 타고 전류가 흐른다.\n"
                        "잠시 뒤 마이크의 작은 표시등이 천천히 켜지더니, 일정한 밝기로 안정된다."
                    ),
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.HEAVY_BATTERY,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mic_stage", "value": 2},
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"key": "mic_fixed", "value": True},
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="마이크에 전원이 공급되었습니다. 이제 파이프를 두드리는 소리를 인식할 수 있습니다.",
                ),
            ],
        ),
        # 마이크 + 산업용 배터리 (이미 전원 연결됨)
        Combination(
            targets=[KeywordId.MICROPHONE, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mic_stage", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="마이크에는 이미 전원이 연결되어 있습니다.",
                )
            ],
        ),
        # 스패너 작업 없이 바로 배터리를 연결하려 할 때
        Combination(
            targets=[KeywordId.MICROPHONE, KeywordId.HEAVY_BATTERY],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="mic_stage", value=0),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "배터리를 억지로 연결해 보지만, 마이크가 덜렁거려 접점이 제대로 닿지 않는다.\n"
                        "먼저 스패너로 마이크를 고정하는 편이 나을 것 같다."
                    ),
                ),
            ],
        ),
    ],
)
