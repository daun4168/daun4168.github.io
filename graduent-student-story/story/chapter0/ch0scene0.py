from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Condition, Interaction, KeywordData, SceneData

UNSEEN_INSPECTED_INTERACTIONS = [
    Interaction(
        conditions=[Condition(type=ConditionType.STATE_IS, target="unseen_inspected", value=False)],
        actions=[
            Action(
                type=ActionType.PRINT_SYSTEM,
                value=(
                    "어떤 **[키워드]**는 시야에 추가되지 않습니다.\n\n"
                    "이러한 키워드는 이야기의 흐름을 바꾸지는 않지만, \n\n"
                    "이야기를 더 깊이 이해하고 느낄 수 있도록 해줍니다."
                ),
            ),
            Action(
                type=ActionType.UPDATE_STATE,
                value={"key": "unseen_inspected", "value": True},
            ),
        ],
        continue_matching=True,
    )
]

CH0_SCENE0_DATA = SceneData(
    id=SceneID.CH0_SCENE0,
    name="교수님 오피스",
    initial_text=(
        "---\n"
        "# Chapter 0\n"
        "## 위기의 대학원생: 서막\n"
        "---\n"
    ),
    body=(
        "눈을 뜨자 익숙한 풍경이 보인다. 책상 위에 쌓인 논문 탑, 그리고 그 뒤에서 번뜩이는 안경알.\n\n"
        '"자네, 정신이 드나? 서서 조는 기술이 아주 일취월장했어."\n\n'
        "교수님이 혀를 차며 나를 바라본다. 10년째 듣는 잔소리다. 타격감도 없다.\n\n"
        '"연구실 제2섹터 청소나 하게. 외부 손님이 온다니까. '
        '필요한 물건 있으면 저기 법인카드 가져가서 사고. 한도는 초과됐지만 포인트는 남았을 거야."\n\n'
        "교수님은 턱짓으로 책상을 가리켰다.\n\n"
        '"다 챙겼으면 뒤에 있는 문으로 나가. 난 사우나... 아니, 미팅 준비해야 하니까."'
    ),
    initial_state={
        "professor_inspected": False,
        "unseen_inspected": False,
    },
    on_enter_actions=[
        Action(
            type=ActionType.PRINT_SYSTEM,
            value=(
                "이제부터 상호작용 방식을 알려드리겠습니다.\n\n"
                "본문에 등장하는 **[키워드]**를 직접 입력하여 탐색하세요.\n\n"
                "예를 들어, `교수님`을 입력해볼까요?"
            ),
        )
    ],
    keywords={
        KeywordId.PROFESSOR: KeywordData(
            type=KeywordType.NPC,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="professor_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="뭘 꾸물거려? 빨리 가서 청소 안 하고! 이번 학기 졸업하기 싫나?",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=(
                                "좋습니다! 이런식으로 본문에 나온 **[키워드]**를 찾으면, 시야의 **[?]**가 찾아낸 키워드로 바뀝니다.\n\n"
                                "모든 **[키워드]**는 항상 본문 안에 숨어 있습니다. \n\n"
                                "띄어쓰기가 포함된 경우도 있으니, 다양하게 입력해서 찾아보세요.\n\n"
                                "시야에 **[?]**로 표시된 모든 **[키워드]**를 찾아보세요."
                            ),
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"key": "professor_inspected", "value": True},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="professor_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="당장 법인카드 챙겨서 저 문으로 나가라고! 그렇게 몸이 굼떠서 논문은 제대로 쓰겠어?",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.CORP_CARD: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.HIDDEN,
            display_name="법인카드",
            silent_discovery=True,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.CORP_CARD)],
                    actions=[
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.CORP_CARD,
                                "description": "긁히지는 않지만 날카로워서 무기나 도구로 쓸 수 있습니다.",
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM, value="어떤 **[키워드]**는 발견해서 **주머니**에 보관할 수 있습니다."
                        ),
                        Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.CORP_CARD),
                    ],
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_SYSTEM, value="이미 가지고 있습니다.")]),
            ],
        ),
        KeywordId.DOOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "문 밖으로 나가 연구실 청소를 하러 가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_SYSTEM,
                                        value="문을 나섭니다. 새로운 장소에서는 **시야**가 초기화되지만, **주머니** 속의 물건은 유지됩니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH0_SCENE1),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="교수님 오피스에서 더 머물도록 합니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="이 문으로 나갈 수 있을 것 같다. 하지만 아직 무언가 잊은 기분이 든다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.THESIS: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            interactions=UNSEEN_INSPECTED_INTERACTIONS,
            description="읽어야 할 논문이 산더미처럼 쌓여있다. 보기만 해도 숨이 막힌다.",
        ),
        KeywordId.DESK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            interactions=UNSEEN_INSPECTED_INTERACTIONS,
            description="교수님의 책상이다. 각종 서류와 논문이 어지럽게 널려있다.",
        ),
        KeywordId.GLASSES: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            interactions=UNSEEN_INSPECTED_INTERACTIONS,
            description="교수님의 안경알이 빛을 번뜩인다. 저 너머의 눈은 웃고 있는지, 화를 내고 있는지 알 수 없다.",
        ),
    },
)
