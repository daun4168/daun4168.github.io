# story/chapter0/scene0_data.py
from const import SceneID, ItemID, KeywordState, ActionType, ConditionType

CH0_SCENE0_DATA = {
    "id": SceneID.CH0_SCENE0,
    "name": "교수님 오피스",
    "initial_text": '눈을 뜨자 익숙한 풍경이 보인다. 책상 위에 쌓인 논문 탑, 그리고 그 뒤에서 번뜩이는 안경알.\n\n"자네, 정신이 드나? 서서 조는 기술이 아주 일취월장했어."\n\n교수님이 혀를 차며 나를 바라본다. 10년째 듣는 잔소리다. 타격감도 없다.\n\n"연구실 제2섹터 청소나 하게. 외부 손님이 온다니까. 필요한 물건 있으면 저기 법인카드 가져가서 사고. 한도는 초과됐지만 포인트는 남았을 거야."\n\n교수님은 턱짓으로 책상을 가리켰다.\n\n"다 챙겼으면 뒤에 있는 문으로 나가. 난 사우나... 아니, 미팅 준비해야 하니까."',
    "on_enter_actions": [
        {
            "type": ActionType.PRINT_SYSTEM,
            "value": "이제부터 상호작용 방식이 바뀝니다. 본문에 등장하는 **[키워드]**를 직접 입력하여 탐색하세요.\n예를 들어, `교수님`을 입력해볼까요?",
        }
    ],
    "keywords": {
        ItemID.PROFESSOR: {
            "type": "NPC",
            "state": KeywordState.HIDDEN,
            "interactions": [
                {
                    "actions": [
                        {
                            "type": ActionType.PRINT_NARRATIVE,
                            "value": "뭘 꾸물거려? 빨리 가서 청소 안 하고! 이번 학기 졸업하기 싫나?",
                        },
                        {
                            "type": ActionType.PRINT_SYSTEM,
                            "value": "막혔을 때는 `둘러보기`를 입력하여 주변을 다시 살필 수 있습니다.",
                        },
                    ]
                }
            ],
        },
        ItemID.CORP_CARD: {
            "type": "Item",
            "state": KeywordState.HIDDEN,
            "display_name": "법인카드",
            # [추가됨] 발견 시 "시야에 추가되었습니다" 시스템 메시지 끄기
            "silent_discovery": True,
            "interactions": [
                {
                    "conditions": [{"type": ConditionType.NOT_HAS_ITEM, "target": ItemID.CORP_CARD}],
                    "actions": [
                        # 원하는 메시지 1
                        {
                            "type": ActionType.PRINT_SYSTEM,
                            "value": "**[법인카드]**를 발견하여 **주머니**에 추가합니다.",
                        },
                        # 원하는 메시지 2
                        {
                            "type": ActionType.PRINT_SYSTEM,
                            "value": "어떤 아이템은 이렇게 **주머니**에 보관할 수 있습니다.",
                        },
                        {
                            "type": ActionType.ADD_ITEM,
                            "value": {
                                "name": ItemID.CORP_CARD,
                                "description": "긁히지는 않지만 날카로워서 무기나 도구로 쓸 수 있습니다.",
                                "silent": True,  # [추가됨] "주머니에 넣었습니다" 시스템 메시지 끄기
                            },
                        },
                        {"type": ActionType.REMOVE_KEYWORD, "target": ItemID.CORP_CARD},
                    ],
                },
                {"actions": [{"type": ActionType.PRINT_SYSTEM, "value": "이미 가지고 있습니다."}]},
            ],
        },
        ItemID.DOOR_0: {
            "type": "Portal",
            "state": KeywordState.HIDDEN,
            "interactions": [
                {
                    "conditions": [{"type": ConditionType.HAS_ITEM, "target": ItemID.CORP_CARD}],
                    "actions": [
                        {
                            "type": ActionType.PRINT_SYSTEM,
                            "value": "문을 나섭니다. 새로운 장소에서는 **시야**가 초기화되지만, **주머니** 속의 물건은 유지됩니다.",
                        },
                        {"type": ActionType.MOVE_SCENE, "value": SceneID.CH0_SCENE1},
                    ],
                },
                {
                    "actions": [
                        {
                            "type": ActionType.PRINT_SYSTEM,
                            "value": "이 문으로 나갈 수 있을 것 같다. 하지만 아직 무언가 잊은 기분이 든다.",
                        }
                    ]
                },
            ],
        },
        ItemID.THESIS: {
            "type": "Object",
            "state": KeywordState.HIDDEN,
            "description": "읽어야 할 논문이 산더미처럼 쌓여있다. 보기만 해도 숨이 막힌다.",
        },
        ItemID.DESK: {
            "type": "Object",
            "state": KeywordState.HIDDEN,
            "description": "교수님의 책상이다. 각종 서류와 논문이 어지럽게 널려있다.",
        },
        ItemID.GLASSES: {
            "type": "Object",
            "state": KeywordState.HIDDEN,
            "description": "교수님의 안경알이 빛을 번뜩인다. 저 너머의 눈은 웃고 있는지, 화를 내고 있는지 알 수 없다.",
        },
    },
}
