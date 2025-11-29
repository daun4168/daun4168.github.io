from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_6_DATA = SceneData(
    id=SceneID.CH1_SCENE2_6,
    name="난파선 주방",
    body=(
        '"우웩! 썩은 치즈랑 식초를 끓인 냄새가 나!"\n\n'
        "난파선 주방입니다. 한때는 요리를 했겠지만, 지금은 쥐들의 뷔페가 되었습니다.\n\n"
        "중앙의 조리대에는 셰프가 차려놓은 기괴한 코스 요리가 그대로 남아있고, "
        "벽면에는 굳게 잠긴 청소 도구함이 보입니다.\n\n"
        "구석에는 쓰레기통이 넘쳐흐르고 있고, 바닥에는 터진 포대가 널려 있습니다.\n\n"
        "선반 위에는 수상한 약품 선반도 보입니다."
    ),
    initial_state={
        "locker_opened": False,
        "bottle_found": False,
        "starch_found": False,
        "corridor_inspected": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.HALLWAY: KeywordData(type=KeywordType.ALIAS, target=KeywordId.TOXIC_CORRIDOR),
        KeywordId.SHELF: KeywordData(type=KeywordType.ALIAS, target=KeywordId.POISON_SHELF),
        KeywordId.FLOUR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.FLOUR_SACK),
        # 0. 나가는 길 (지하 복도)
        KeywordId.TOXIC_CORRIDOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="corridor_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="산성 웅덩이가 있는 복도 쪽 문입니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "corridor_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="corridor_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[지하 복도]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="주방을 나갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_5),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 찾을 게 남았습니다.")
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 쓰레기통 (소스통 파밍)
        KeywordId.TRASH_CAN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bottle_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="쓰레기통을 뒤져서 깨끗한 **[빈 소스통]**을 하나 건졌습니다. 입구가 좁아 위험한 액체를 담기 좋아 보입니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.SAUCE_BOTTLE, "description": "말랑말랑한 플라스틱 소스통."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "bottle_found", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="더 뒤져봤자 파상풍만 걸릴 것 같습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.TRASH_CAN, "state": KeywordState.UNSEEN},
                        ),
                    ]
                ),
            ],
        ),
        # 2. 터진 포대 (전분 파밍) - 위치 변경됨
        KeywordId.FLOUR_SACK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="starch_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="바닥에 쏟아진 밀가루 포대들 사이에서, 멀쩡한 **[전분 가루]** 한 봉지를 발견했습니다. 요리용 감자 전분입니다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.POTATO_STARCH, "description": "요리용 감자 전분."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "starch_found", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE, value="빈 껍데기뿐입니다. 쥐들이 이미 파티를 끝냈습니다."
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.FLOUR_SACK, "state": KeywordState.UNSEEN},
                        ),
                    ]
                ),
            ],
        ),
        # 3. 청소 도구함 (가성소다 - 잠김)
        KeywordId.CLEANING_LOCKER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="locker_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="문이 열려 있습니다. 안에는 **[가성소다 포대]**가 들어있습니다. 너무 무거워서 통째로는 못 가져갑니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.CLEANING_LOCKER, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "위험물 표시가 붙은 철제 캐비닛입니다. 전자식 키패드가 달려 있습니다.\n"
                                "옆에는 셰프가 남긴 **[코스 요리 메뉴판]**이 붙어 있습니다."
                            ),
                        ),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.COURSE_MENU),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.CLEANING_LOCKER} : [비밀번호 6자리]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # 4. 코스 요리 메뉴판 (힌트 텍스트)
        KeywordId.COURSE_MENU: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '"내 주방의 도구를 탐내는 자여, 접시 위의 진실을 보라."\n\n<br>'
                "① Appetizer: 바나나. 오직 신선한 부분만.\n\n"
                "② Main: 파스타. 가장 양이 적은 접시 하나면 충분하다.\n\n"
                "③ Dessert: 독약. 붉은 피가 담긴 것만이 진정한 끝을 선사한다."
            ),
        ),
        # 5. 조리대 (음식 힌트 관찰)
        KeywordId.COOKING_TABLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "셰프가 차려놓은 마지막 만찬입니다. 음식이라기보단 실험체 같습니다.\n\n"
                                "**[바나나]**와 **[파스타]**가 접시에 담겨 있습니다."
                            ),
                        ),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.BANANA_OBJ),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.PASTA_OBJ),
                    ]
                )
            ],
        ),
        # 5-1. 바나나 (힌트: Ba-Na-Na 중 가운데 = Na = 11)
        KeywordId.BANANA_OBJ: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # 조리대 봐야 나옴
            description=(
                "도마 위에 바나나 하나가 칼로 정확히 3등분 되어 있습니다.\n\n"
                "양쪽 끝부분은 시커멓게 썩어 문드러졌지만, \n\n"
                "가운데 토막만은 신선해 보입니다."
            ),
        ),
        # 5-2. 파스타 (힌트: P-As-Ta 중 가장 작은 것 = P = 15)
        KeywordId.PASTA_OBJ: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "세 개의 접시에 파스타가 담겨 있습니다.\n\n"
                "가운데와 오른쪽 접시는 면이 산더미처럼 쌓여 있는데,\n\n"
                "왼쪽 접시만 양이 다른 접시의 절반 정도로 적습니다."
            ),
        ),
        # 6. 약품 선반 (힌트: P-O-I-S-O-N 중 3번째 = I = 53)
        KeywordId.POISON_SHELF: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/poison.png" alt="독약" width="540">\n\n'
                                "선반 위에 똑같이 생긴 독약 병 6개가 일렬로 늘어서 있습니다.\n\n"
                            ),
                        ),
                    ]
                )
            ],
        ),
        # 4. 가성소다 포대 (새로운 오브젝트)
        KeywordId.CAUSTIC_SODA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # 초기엔 숨겨짐
            description="공업용 가성소다(NaOH)가 가득 찬 무거운 포대입니다.\n\n맨손으로 만지면 위험하고, 통째로 들기엔 너무 무겁습니다.\n\n내용을 담을 용기가 필요합니다.",
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="너무 무겁고 위험해서 맨손으로는 옮길 수 없습니다.\n\n담을 도구가 필요합니다.",
                        )
                    ]
                )
            ],
        ),
        # --- UNSEEN 오브젝트 (난파선 주방) ---
        "치즈": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="발효의 경계를 넘어 생화학 무기가 되었다. 냄새만으로도 쥐를 기절시킬 수 있을 것 같다.",
        ),
        "식초": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="코가 뻥 뚫리다 못해 뇌까지 시큰거린다. 위산이 역류하는 기분이다.",
        ),
        "쥐": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="살이 포동포동하게 올랐다. 이 배에서 가장 잘 먹고 지낸 녀석들일 것이다. 눈이 마주친 것 같아 기분이 나쁘다.",
        ),
        "뷔페": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="쥐와 벌레들을 위한 5성급 호텔 뷔페다. 내가 여기 계속 서 있다간 '오늘의 특선 고기'가 될지도 모른다.",
        ),
        "셰프": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이런 지옥 같은 곳에서 코스 요리를 만들다니, 그는 요리사가 아니라 매드 사이언티스트였을 것이 분명하다.",
        ),
        "냄새": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="코가 마비될 지경이다. 이 냄새를 향수로 만들면 '지옥의 향기'라는 이름으로 대박 날지도 모르겠다.",
        ),
        "벽면": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="기름때와 곰팡이가 추상화처럼 얼룩져 있다. 예술 점수는 0점, 위생 점수는 마이너스 100점이다.",
        ),
        "바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="밟을 때마다 '찌걱' 소리가 난다. 신발 밑창에 껌이 붙은 기분보다 백 배는 더 찝찝하고 불쾌하다.",
        ),
        "구석": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="어둠 속에서 무언가 번뜩인다. 라따뚜이의 주인공을 기대하기엔 위생 상태가 너무 절망적이다.",
        ),
        "코스 요리": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="보기만 해도 배가 아프다. 파인다이닝(Fine Dining)이 아니라 다잉(Dying)이다. 먹는 순간 요단강 뷰를 감상하게 될 것이다.",
        ),
        "우웩": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="조건반사다. 파블로프의 개처럼, 이 냄새를 맡자마자 위장이 수축 운동을 시작했다.",
        ),
    },
    combinations=[
        # 1. 도구함 암호 해제
        # 해석:
        # 바나나(가운데) -> Na (11)
        # 파스타(가장 작은 왼쪽) -> P (15)
        # 독약(3번째 붉은 병) -> I (53)
        # 정답: 111553
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.CLEANING_LOCKER, "111553"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="삐리릭! 잠금 장치가 해제됩니다. 안에서 공업용 **[가성소다 포대]**를 발견했습니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "locker_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.BANANA_OBJ, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.PASTA_OBJ, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.COOKING_TABLE, "state": KeywordState.UNSEEN},
                ),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.COURSE_MENU, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.POISON_SHELF, "state": KeywordState.UNSEEN},
                ),
                Action(
                    type=ActionType.DISCOVER_KEYWORD,
                    value=KeywordId.CAUSTIC_SODA,
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.SAUCE_BOTTLE, KeywordId.CAUSTIC_SODA],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="소스병 입구가 너무 좁습니다. 입구가 넓은 용기가 필요합니다.",
                )
            ],
        ),
        # 2. 가성소다 담기 (양동이 + 도구함)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.CAUSTIC_SODA],
            conditions=[Condition(type=ConditionType.STATE_IS, target="locker_opened", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="녹슨 양동이에 가성소다 가루를 가득 퍼담았습니다. 꽤 무겁습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUSTY_BUCKET),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.FILLED_BUCKET, "description": "가성소다가 담긴 양동이."},
                ),
            ],
        ),
    ],
)
