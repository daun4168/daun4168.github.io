from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_2_DATA = SceneData(
    id=SceneID.CH1_SCENE2_2,
    name="선장실",
    body=(
        '"오오... 역시 캡틴의 방은 클래스가 다르구만!"\n\n'
        "문짝부터 남다른 선장실입니다. 바닥은 기울어졌지만, 중후한 마호가니 책상과 가죽 의자는 여전히 권위를 뽐내고 있습니다.\n"
        "방 안에는 묵은 종이 냄새와 고급 시가 냄새가 은은하게 배어 있습니다.\n\n"
        "벽면에는 항해 일지가 꽂힌 책장이 있고, 머리 위 선반에는 비싸 보이는 유리병 배들이 진열되어 있습니다.\n\n"
        "이런 곳에 앉아 있으면 폼 좀 나겠는데요? 물론 살아서 나갈 수 있다면 말이죠."
    ),
    initial_state={
        "hallway_inspected": False,
        "desk_searched": False,
        "bookshelf_unlocked": False,
        "shelf_inspected": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.DESK: KeywordData(type=KeywordType.ALIAS, target=KeywordId.MAHOGANY_DESK),
        # 1. 나가기 (복도 포탈) - 조사 후 이동 로직 적용
        KeywordId.HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                # 첫 번째 상호작용: 관찰 (Narrative)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '"후우... 나가기 싫다.\n\n"'
                                "문밖으로 고개를 내미니 퀴퀴한 복도 냄새가 훅 들어옵니다.\n\n"
                                "마호가니 책상과 가죽 의자가 있는 이 방이 천국이었습니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "hallway_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # 두 번째 상호작용: 이동 확인 (Confirmation)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "안락한 선장실을 뒤로하고 **[복도]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value='"안녕, 나의 짧은 부귀영화여."\n\n아쉬움을 뒤로하고 선장실을 나섭니다.',
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_0),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 덜 챙긴 게 있는지 확인해 봅니다. 가죽 의자에 한 번 더 앉아봅니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 선반 (유리병 배 퍼즐 씬으로 이동)
        KeywordId.SHELF: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                # 첫 번째 상호작용: 관찰
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="shelf_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "벽면 높이 달린 참나무 선반입니다. 먼지 하나 없이 깨끗한 유리병 배 4개가 위태롭게 놓여 있습니다.\n"
                                "자세히 보니 병마다 이름표가 붙어 있는 것 같습니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "shelf_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # 두 번째 상호작용: 이동 확인
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="shelf_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "까치발을 들고 **[선반]**을 더 자세히 살펴보시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="당신은 눈을 가늘게 뜨고 선반 위의 유리병들을 들여다봅니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_3),  # 상세 뷰로 이동
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직은 멀리서 보는 게 좋겠습니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 2. 마호가니 책상 (주기율표 파밍)
        KeywordId.MAHOGANY_DESK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="desk_searched", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "서랍 깊숙한 곳에서 꼬깃꼬깃하게 접힌 종이를 발견했습니다.\n\n"
                                "보물지도인가 싶어 설레는 마음으로 펼쳤는데... 맙소사, **[주기율표]**입니다.\n\n"
                                '"도대체 선장 책상에 이게 왜 있는 거야? 항해하다 심심하면 원소 기호라도 외우셨나?"'
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.PERIODIC_TABLE,
                                "description": (
                                    "원소 기호와 번호가 적힌 표.\n\n"
                                    '<img src="assets/chapter1/periodic_table.png" alt="주기율표" width="540">'
                                ),
                            },
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "desk_searched", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="고급스러운 책상입니다. 챙길 건 다 챙겼습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MAHOGANY_DESK, "state": KeywordState.UNSEEN},
                        ),
                    ]
                ),
            ],
        ),
        # 3. 책장 (항해일지 + 사물함)
        KeywordId.BOOKSHELF: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "항해 관련 서적들이 빼곡합니다. 그중 유독 손때가 탄 **[항해 일지]**가 눈에 띕니다.\n"
                                "책장 하단에는 잠긴 **[보관함]**이 하나 있습니다."
                            ),
                        ),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LOG_BOOK),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.BOOKSHELF_LOCKER),
                    ]
                )
            ],
        ),
        KeywordId.LOG_BOOK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "(첫 장에 휘갈겨 쓴 메모)\n\n"
                '"이 빌어먹을 나침반은 고장 났다. N, W, S는 있는데 E가 보이지 않는다.\n\n<br>'
                "[ 첫 번째 탈출 시도 ]\n\n"
                '"우리는 지도상의 북쪽 끝자락 섬에서 닻을 올렸다.\n\n'
                "바람을 등지고 서쪽으로 꼬박 이틀을 항해했다.\n\n"
                '하지만 그곳은 우리가 찾던 육지가 아니었다."\n\n<br>'
                "[ 두 번째 탈출 시도 ]\n\n"
                '"첫 번째 실패 후, 우리는 서쪽 끝에 있는 섬으로 이동했다.\n\n'
                "이번엔 거센 물살을 거슬러 북쪽으로 하루를 올라가 보았다.\n\n"
                '하지만 그곳 역시 망망대해뿐이었다."\n\n<br>'
                "[ 세 번째 탈출 시도 ]\n\n"
                '"이번이 마지막 기회다. 우리는 남쪽 항구에서 마지막 희망을 걸기로 했다.\n\n'
                "해를 등지고 서쪽으로 하루 동안 죽을힘을 다해 나아갔다.\n\n"
                '부디... 이번에는 틀리지 않았기를."'
            ),
        ),
        KeywordId.BOOKSHELF_LOCKER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bookshelf_unlocked", value=True)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="열려 있습니다. 안은 비었습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.BOOKSHELF_LOCKER, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="책장 하단에 붙박이로 설치된 목재 수납장입니다. 다섯 자리 숫자를 맞추는 구형 다이얼 자물쇠가 굳게 잠겨 있습니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.BOOKSHELF_LOCKER} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ]
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (배경/분위기) ---
        "의자": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="앉으면 엉덩이가 빨려 들어갈 것 같은 최고급 의자다. 떼어가서 내 연구실 의자로 쓰고 싶다.",
        ),
        "냄새": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="성공한 남자의 향기...는 개뿔, 폐암 걸리기 딱 좋은 냄새다. 콜록.",
        ),
        "경사": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="바닥이 삐딱하다. 여기서 컵라면을 먹으면 국물이 한쪽으로만 쏠릴 것이다. 균형 감각을 키우기엔 좋겠네.",
        ),
        "문짝": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="두께가 내 전공 서적 합친 것보다 두껍다. 이걸 뜯어서 뗏목으로 쓰면 딱인데, 경첩이 녹슬어서 꿈쩍도 안 한다.",
        ),
        "마호가니": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="원목이 아주 단단해 보인다. 이걸로 머리를 맞으면 훈장님께 회초리 맞는 것보다 10배는 아플 것이다.",
        ),
        "권위": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="눈에 보이지 않지만 공기 중에 떠다닌다. 지도 교수님 방에 들어갔을 때의 그 숨 막히는 기분과 비슷하다.",
        ),
        "벽면": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="항해 일지와 지도가 빼곡하다. 나도 연구실 벽면을 논문으로 도배했었는데... 갑자기 눈물이 난다.",
        ),
    },
    combinations=[
        # 1. 책장 보관함 + 54215 -> 조명탄
        Combination(
            type=CombinationType.PASSWORD,
            targets=["보관함", "54215"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="딸깍! 보관함이 열립니다. 안에서 시뻘건 **[조명탄]**을 발견했습니다. 불장난하기 딱 좋겠네요.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.FLARE, "description": "초고열을 내는 구조 신호용 조명탄."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "bookshelf_unlocked", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LOG_BOOK, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
    ],
)
