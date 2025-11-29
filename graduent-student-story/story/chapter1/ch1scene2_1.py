from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_1_DATA = SceneData(
    id=SceneID.CH1_SCENE2_1,
    name="선원 숙소",
    body=(
        '"우욱... 곰팡이 냄새가 진동을 하네."\n\n'
        "문짝이 덜렁거리는 선원 숙소 내부입니다. 바닥에는 썩은 물이 발목까지 차올라 찰랑거리고,\n\n"
        "2층 침대들은 지진이라도 난 듯 어지럽게 뒤엉켜 있습니다.\n\n"
        "눅눅한 매트리스 위에는 주인을 잃은 일기장들이 덩그러니 놓여 있고,\n\n"
        "벽면에는 녹슬어 붉게 변한 철제 사물함 세 개가 위태롭게 매달려 있습니다."
    ),
    initial_state={
        "hallway_inspected": False,
        "diary_inspected": False,
        "lockers_inspected": False,
        "locker_boatswain_opened": False,
        "locker_navigator_opened": False,
        "locker_radioman_opened": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.LOCKER: KeywordData(type=KeywordType.ALIAS, target=KeywordId.LOCKER_GROUP),
        # 1. 나가기 (복도 포탈) - 요청하신 확인 로직 적용
        KeywordId.HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='"으... 빨리 나가고 싶다."\n\n문밖으로 어두침침한 복도가 보입니다. 적어도 여기보다는 공기가 낫겠지요.',
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "hallway_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "음산한 숙소를 나가 **[복도]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="도망치듯 숙소를 빠져나와 복도로 나갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_0),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 미련이 남았습니다. 조금 더 뒤져봅니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 2. 일기장 (오브젝트 그룹)
        KeywordId.DIARY_BUNDLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="diary_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.UPDATE_STATE, value={"key": "diary_inspected", "value": True}),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.DIARY_BOATSWAIN),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.DIARY_NAVIGATOR),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.DIARY_RADIOMAN),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "물에 젖어 쭈글쭈글해진 공책 세 권입니다. 각각 다른 필체로 절박했던 마지막 순간이 적혀 있습니다.\n\n"
                                "어떤 일기를 읽으시겠습니까?\n\n<br>"
                                f"· **[{KeywordId.DIARY_BOATSWAIN}]**\n\n"
                                f"· **[{KeywordId.DIARY_NAVIGATOR}]**\n\n"
                                f"· **[{KeywordId.DIARY_RADIOMAN}]**"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 2-1. 갑판장의 기도문 (9271)
        KeywordId.DIARY_BOATSWAIN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "폭풍우가 몰아치던 아홉시 경, 배가 암초에 부딪혔다.\n\n"
                "아무리 둘러봐도 보이는 건 끝없는 수평선과 절망뿐이다.\n\n"
                "고향에 있는 딸아이가 올해로 일곱 살이 되었을 텐데...\n\n"
                "하나님, 어찌하여 죄 없는 우리를 버리시나이까."
            ),
        ),
        # 2-2. 항해사의 유서 (1682)
        KeywordId.DIARY_NAVIGATOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "일기장에 남기는 이 글이 유언이 되지 않기를 바란다.\n\n"
                "육지가 보인다고 소리쳤지만, 그것은 신기루였다.\n\n"
                "팔다리에 감각이 없다. 저체온증이 시작된 것 같다.\n\n"
                "이젠 더 이상 버틸 힘이 남아있지 않다."
            ),
        ),
        # 2-3. 통신사의 전문 (3578)
        KeywordId.DIARY_RADIOMAN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "숨을 쉴 수가 없다. 물이 턱밑까지 차올랐다.\n\n"
                "아무리 소리쳐도 대답하는 이는 없다.\n\n"
                "마지막 구조 신호를 보냈다. 닿기를 바랄 뿐.\n\n<br>"
                "우리는 항로를 이탈하지 말았어야 했다.\n\n"
                "오늘따라 고향의 하늘이 보고 싶구나.\n\n<br>"
                "차가운 바닷물이 뼈속까지 스며든다.\n\n"
                "이젠 손가락 감각조차 느껴지지 않는다.\n\n"
                "라디오는 끊긴 지 오래다. 지지직거리는 소리뿐.\n\n<br>"
                "파도가 모든 것을 집어삼키려 한다.\n\n"
                "아직... 아직은 죽고 싶지 않은데.\n\n"
                "라일락 꽃향기가... 어디선가 나는 것 같다."
            ),
        ),
        # 3. 사물함 (오브젝트 그룹)
        KeywordId.LOCKER_GROUP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 첫 조사 시 하위 키워드 발견
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="lockers_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.UPDATE_STATE, value={"key": "lockers_inspected", "value": True}),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LOCKER_BOATSWAIN),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LOCKER_NAVIGATOR),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LOCKER_RADIOMAN),
                    ],
                    continue_matching=True,
                ),
                # 묘사 및 목록 출력
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "개인 물품을 보관하던 캐비닛입니다. 세 개 모두 4자리 번호 자물쇠로 잠겨 있습니다.\n\n"
                                "어느 사물함을 확인하시겠습니까?\n\n<br>"
                                f"· **[{KeywordId.LOCKER_BOATSWAIN}]**\n\n"
                                f"· **[{KeywordId.LOCKER_NAVIGATOR}]**\n\n"
                                f"· **[{KeywordId.LOCKER_RADIOMAN}]**"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 3-1. 갑판장의 사물함 (Boatswain)
        KeywordId.LOCKER_BOATSWAIN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="locker_boatswain_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="갑판장의 사물함이 열려 있습니다. 안에는 거친 밧줄 조각과 먼지뿐입니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LOCKER_BOATSWAIN, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="갑판장이라는 명찰이 붙어 있습니다. 투박하고 묵직한 강철 자물쇠가 굳게 닫혀 있습니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.LOCKER_BOATSWAIN} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # 3-2. 항해사의 사물함 (Navigator)
        KeywordId.LOCKER_NAVIGATOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="locker_navigator_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="항해사의 사물함입니다. 텅 비어있지만 바닥에 젖은 별자리 지도가 붙어 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LOCKER_NAVIGATOR, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="항해사의 사물함입니다. 바닷바람에 하얗게 소금기가 낀 황동 자물쇠가 문을 막고 있습니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.LOCKER_NAVIGATOR} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # 3-3. 통신사의 사물함 (Radioman)
        KeywordId.LOCKER_RADIOMAN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="locker_radioman_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="통신사의 사물함이 열려 있습니다. 끊어진 전선 조각들이 굴러다닙니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LOCKER_RADIOMAN, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="통신사의 사물함입니다. 얇고 긴 쇠고리가 달린 자물쇠가 걸려 있습니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.LOCKER_RADIOMAN} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # --- 배경/분위기용 UNSEEN 오브젝트 ---
        "선원 숙소": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="닭장처럼 좁아터졌다. 배 안이나 대학원 연구실이나 사람을 부품처럼 갈아 넣는 공간인 건 매한가지인가 보다.",
        ),
        "냄새": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="장마철에 환기 안 시킨 자취방 냄새의 100배 농축 버전이다. 숨을 쉴 때마다 폐포에 포자가 심어지는 기분이다.",
        ),
        "문짝": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="덜렁거리는 게 꼭 내 멘탈 같다. 손가락으로 툭 치면 바로 떨어져 나갈 기세다.",
        ),
        "바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="무엇이 가라앉아 있을지 모르는 지뢰밭이다. 녹슨 못이라도 밟는 날엔 파상풍 주사도 없이 요단강 건너는 거다.",
        ),
        "썩은 물": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="온갖 세균과 박테리아의 뷔페가 열린 배양액이다. 상처 난 부위가 닿는 순간 파상풍 당첨은 확정이다.",
        ),
        "발목": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="차가운 썩은 물이 닿는 느낌이 끔찍하다. 이대로 오래 있으면 군대에서도 안 걸려본 참호족 당첨이다.",
        ),
        "2층 침대": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="지진이라도 난 것처럼 뒤엉켜 있다. '혼돈과 파괴'라는 제목의 현대 미술 작품이라고 해도 믿겠다.",
        ),
        "매트리스": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="물을 잔뜩 머금은 거대한 스펀지다. 눕는 순간 등 뒤로 차가운 썩은 물이 배어 나올 상상을 하니 소름이 돋는다.",
        ),
        "주인": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="일기장의 주인들이다. 그들은 지금 어디에 있을까? 적어도 나보다는 편한 곳에 있기를 바랄 뿐이다.",
        ),
        "벽면": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="녹이 슬어 붉게 변했다. 긁히면 패혈증으로 요단강을 건널 수 있는 훌륭한 생물학적 무기다.",
        ),
        "곰팡이": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="배양기에 방치된 페트리 접시 속 균사체처럼 화려하게 피어있다. 이걸 긁어가면 신종 발견으로 논문을 쓸 수 있을까? 아니, 그전에 내 폐가 먼저 썩을 것이다.",
        ),
        "지진": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="진도 7.0의 강진이 휩쓸고 지나간 듯하다. 물론 진짜 지진은 아니고, 그냥 관리가 안 된 거다. 내 자취방 풍경과 묘하게 겹쳐 보인다.",
        ),
        "진동": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="물리적 진동이 아니라, 후각적 타격감이 고막까지 울리는 기분이다. 냄새가 소리로 들린다면 분명 데스메탈일 것이다.",
        ),
        "철제": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="한때는 튼튼한 강철이었겠지만, 지금은 산화철 덩어리다. 화학적으로 매우 안정한 상태... 즉, 더 이상 쓸모없다는 뜻이다.",
        ),
        "위태": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="금방이라도 떨어질 듯 아슬아슬하게 매달려 있다. 교수님 눈밖에 난 내 처지와 데칼코마니처럼 닮았다.",
        ),
        "우욱": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="위장이 요동친다. 어제 먹은 라면이 역류하려는 걸 간신히 참았다. 여기서 토하면 위생 점수가 마이너스 무한대가 될 것이다.",
        ),
    },
    combinations=[
        # 갑판장 사물함 해제 (9271) -> 쪽지 1 획득
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.LOCKER_BOATSWAIN, "9271"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="철컥! 갑판장의 사물함이 열렸습니다. 안에서 **[갑판사의 쪽지]**를 발견했습니다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.NOTE_1,
                        "description": (
                            "선장님은 그 번쩍거리는 배를 아끼시는 모양인데, 전문가인 내 눈엔 그냥 예쁜 쓰레기야.\n\n"
                            "이 거친 바다에서 살아남으려면 적어도 돛대가 두 개 이상은 돼야지.\n\n"
                            "열쇠같이 중요한 걸 그런 '약해빠진' 배에 실었을 리가 없어."
                        ),
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "locker_boatswain_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.DIARY_BOATSWAIN, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # 항해사 사물함 해제 (1682) -> 쪽지 2 획득
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.LOCKER_NAVIGATOR, "1682"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="달그락. 항해사의 사물함이 열렸습니다. **[항해사의 쪽지]**가 들어있습니다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.NOTE_2,
                        "description": (
                            "붉은 노을은 뱃사람의 기쁨이라지만, 바닥에 붉은 피가 고인 배는 이야기가 다르지. "
                            "선장님도 그 배를 볼 때마다 '피 비린내가 난다'며 고개를 돌리시더군. "
                            "미신을 끔찍하게 믿는 그 양반 성격에, 절대 그 '재수 없는' 배에 열쇠를 두진 않았을 거야. 장담해."
                        ),
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "locker_navigator_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.DIARY_NAVIGATOR, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # 통신사 사물함 해제 (3578) -> 쪽지 3 획득
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.LOCKER_RADIOMAN, "3578"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="삐그덕. 통신사의 사물함 문이 열립니다. 구석에서 **[통신사의 쪽지]**를 찾아냈습니다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.NOTE_3,
                        "description": (
                            "무전기 너머로 들리는 잡음보다 더 무서운 건 선장님의 표정이야.\n\n"
                            "아까 유리병에 담긴 배를 보며 사색이 되시더군. 내부가 까맣게 그을려 있는 게 꼭 불타버린 유령선 같다나.\n\n"
                            "그 배는 '저주받았다'면서 손가락 하나 대기 싫어하셨어."
                        ),
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "locker_radioman_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.DIARY_RADIOMAN, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
    ],
)
