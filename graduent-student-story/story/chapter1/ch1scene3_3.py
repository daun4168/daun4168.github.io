from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Condition, Interaction, KeywordData, SceneData

CH1_SCENE3_3_DATA = SceneData(
    id=SceneID.CH1_SCENE3_3,
    name="자료실",
    initial_text="---\n## 자료실\n---\n\n",
    body=(
        '"책 냄새... 논문 쓸 때 맡던 그 지긋지긋한 냄새다."\n\n'
        "벽면 가득 책장이 들어찬 자료실입니다. 바닥에는 읽다 만 책들이 탑처럼 쌓여 있습니다.\n\n"
        "왼쪽 책장에는 뜬금없이 악보들이 꽂혀 있고,\n"
        "오른쪽 책장에는 전문 생태학 서적들이 보입니다.\n\n"
        "중앙의 연구 책상 위에는 펼쳐진 노트가 한 권 놓여 있습니다."
    ),
    initial_state={
        "hallway_inspected": False,
        "left_shelf_inspected": False,  # 왼쪽 책장 조사 여부
        "right_shelf_inspected": False,  # 오른쪽 책장 조사 여부
        "desk_inspected": False,  # 책상 조사 여부
    },
    on_enter_actions=[],
    keywords={
        KeywordId.DESK: KeywordData(type=KeywordType.ALIAS, target=KeywordId.RESEARCH_DESK),
        # 0. 나가기 (연구동 복도)
        KeywordId.HALLWAY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="hallway_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="자료실 문밖으로 적막한 복도가 보입니다. 책 냄새가 옅어지는 곳입니다.",
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
                                "prompt": "자료실을 나가 **[연구동 중앙 복도]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="읽던 책을 내려놓고 복도로 나갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 읽어볼 자료가 있습니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # =================================================================
        # 1. 왼쪽 책장 (악보 4개 발견)
        # =================================================================
        KeywordId.LEFT_BOOKSHELF: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 첫 조사 (악보 발견)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="left_shelf_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "동요 악보집들이 꽂혀 있습니다. 낡은 악보 3개를 발견했습니다.\n\n"
                                f"① **[{KeywordId.SHEET_MUSIC_1}]**\n\n"
                                f"② **[{KeywordId.SHEET_MUSIC_2}]**\n\n"
                                f"③ **[{KeywordId.SHEET_MUSIC_3}]**\n\n"
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "left_shelf_inspected", "value": True}),
                        # 4개의 악보 키워드 발견 처리
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SHEET_MUSIC_1),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SHEET_MUSIC_2),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SHEET_MUSIC_3),
                    ],
                ),
                # Case 2: 재조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="left_shelf_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="동요 악보집이 꽂혀 있습니다. 이미 필요한 악보들은 확인했습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LEFT_BOOKSHELF, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
            ],
        ),
        # [악보 아이템들] (초기 INACTIVE -> 책장 조사 시 DISCOVERED)
        KeywordId.SHEET_MUSIC_1: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description='<img src="assets/chapter1/sheet_music1_2.png" alt="악보" width="530">\n\n'
            "<떴다 떴다 비행기> 악보입니다. 이 섬에도 비행기 한번 떠 주면 좋을텐데요.",
        ),
        KeywordId.SHEET_MUSIC_2: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description='<img src="assets/chapter1/sheet_music2.png" alt="악보" width="530">\n\n'
            "<반짝반짝 작은 별> 악보입니다. 트윙클 트윙클 리틀 스타~",
        ),
        KeywordId.SHEET_MUSIC_3: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description='<img src="assets/chapter1/sheet_music3.png" alt="악보" width="530">\n\n'
            "<곰 세 마리> 악보입니다. 아빠 곰, 엄마 곰, 아기 곰. 생각만 해도 귀엽네요.",
        ),
        # =================================================================
        # 2. 오른쪽 책장 (생태학 서적)
        # =================================================================
        KeywordId.RIGHT_BOOKSHELF: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 첫 조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="right_shelf_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "생물학 서적들이 빽빽합니다. 그중 유독 낡아서 제본이 뜯어진 책 한 권을 발견했습니다.\n\n"
                                "집어 들자마자 **[생태학 책 표지]**, **[생태학 책 목차]**, **[생태학 책 본문]**으로 분해되어 우수수 떨어집니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "right_shelf_inspected", "value": True}),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.ECOLOGY_BOOK_TITLE),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.ECOLOGY_BOOK_INDEX),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.ECOLOGY_BOOK_BODY),
                    ],
                ),
                # Case 2: 재조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="right_shelf_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=("남은 책들은 너무 전문적인 내용이라 봐도 모르겠습니다."),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RIGHT_BOOKSHELF, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.ECOLOGY_BOOK_TITLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '<img src="assets/chapter1/ecology.png" alt="ecology" width="530">\n\n'
                "표지에 'ECOLOGY: A Holistic Approach'라고 적혀 있습니다."
            ),
        ),
        KeywordId.ECOLOGY_BOOK_INDEX: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '<img src="assets/chapter1/index_of_species.png" alt="index_of_species" width="530">\n\n'
                "책을 펼치니 동물들의 학명이 나옵니다.\n\n"
            ),
        ),
        KeywordId.ECOLOGY_BOOK_BODY: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "습기에 불어 곰팡이가 슬어버린 본문 뭉치입니다.\n\n"
                "글자가 대부분 번져서 알아볼 수 없습니다.\n\n"
                "'자연은... 위대하다...' 같은 뻔한 문장 몇 개만 겨우 보입니다.\n\n"
                "정보로서의 가치는 없어 보입니다."
            ),
        ),
        # =================================================================
        # 3. 연구 책상 (조사 기록)
        # =================================================================
        KeywordId.RESEARCH_DESK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 첫 조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="desk_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="누군가가 손으로 쓴 **[생태 조사 기록]**이 펼쳐져 있습니다. 잉크가 번져 있지만 읽을 수는 있습니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "desk_inspected", "value": True}),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.SURVEY_LOG),
                    ],
                ),
                # Case 2: 재조사
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="desk_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="연구 책상 위에는 **[생태 조사 기록]**이 펼쳐져 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RESEARCH_DESK, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.SURVEY_LOG: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '"숲 가장자리 돌무더기에서 족제비가 튀어나왔지만, 곧 능선 위로 늑대의 거대한 그림자가 드리우자 황급히 몸을 숨겼습니다. '
                "최상위 포식자가 사라진 뒤에야 족제비는 다시 고개를 내밀고, 먹이를 찾아 썩은 나무 틈새로 재빠르게 이동했습니다.\n\n"
                "녀석이 파헤친 흙 속에서는 지렁이들이 묵묵히 낙엽을 분해하고 있었고, 그 위로 붉은 여우가 기회주의자처럼 가볍게 스쳐 지나갔습니다. "
                '소란스러운 포식자들의 하루가 저물어가는 물가에는, 붓꽃만이 고요히 뿌리를 내린 채 습지의 저녁을 맞이하고 있었습니다."'
            ),
        ),
        # --- UNSEEN 오브젝트 (자료실) ---
        "냄새": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="오래된 종이와 잉크, 그리고 곰팡이가 섞인 냄새. 도서관 사서들이 맡는다는 '지식의 향기'인가? 내겐 비염 유발제일 뿐이다.",
        ),
        "탑": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="바닥에 위태롭게 쌓여 있다. 젠가 고수가 쌓은 게 분명하다. 하나라도 건드리면 무너져서 압사당할지도 모른다.",
        ),
        "책장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="천장까지 닿을 듯 높다. 왼쪽, 오른쪽 책장을 각각 살펴보는게 좋겠다.",
        ),
    },
    combinations=[],
)
