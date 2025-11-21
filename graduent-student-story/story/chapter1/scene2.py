from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_DATA = SceneData(
    id=SceneID.CH1_SCENE2,
    name="난파선 잔해 (자원 채취장)",
    initial_text=(
        "반쯤 모래에 파묻힌 거대한 난파선 잔해 앞입니다. 썩은 나무와 쇠 냄새가 진동합니다. 이곳저곳에 오래된 백골도 보입니다. "
        "파상풍 주사를 언제 맞았는지 기억이 나질 않습니다. 긁히지 않게 조심해야겠습니다.\n\n"
        "선체 안쪽 화물 칸에는 정체를 알 수 없는 잡동사니들이 쏟아져 나와 있습니다. "
        "바닥에는 녹슨 철판들이 널려 있어 걷기 위험합니다.\n"
        "서쪽으로 돌아가면 안전한 해변 베이스캠프입니다."
    ),
    initial_state={
        "beach_path_inspected": False,
        "searched_cargo": False,
    },
    keywords={
        KeywordId.BASECAMP: KeywordData(type=KeywordType.ALIAS, target=KeywordId.BEACH),
        # 1. 해변 (돌아가는 길)
        KeywordId.BEACH: KeywordData(
            type=KeywordType.PORTAL, state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="서쪽을 보니 베이스캠프가 아지랑이 속에 보인다. 돌아가는 길도 험난해 보인다. (체력 소모 예상)"),
                        Action(type=ActionType.PRINT_SYSTEM, value="다시 한번 **[해변]**을 입력하면 이동 여부를 결정합니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "beach_path_inspected", "value": True})
                    ]
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": (
                                    "**[해변]**으로 돌아가시겠습니까?\n"
                                    "역시 **체력이 2 소모**됩니다. 진행하시겠습니까?"
                                ),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="뜨거운 모래사장을 가로질러 베이스캠프로 복귀합니다.",
                                    ),
                                    Action(type=ActionType.MODIFY_STAMINA, value=-2),  # 체력 소모
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="조금 더 파밍을 해보는 게 좋겠습니다.",
                                    ),
                                ],
                            },
                        ),
                    ]
                )
            ]
        ),

        # 2. 오브젝트 (파밍)
        KeywordId.CARGO_HOLD: KeywordData(
            type=KeywordType.OBJECT, state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="searched_cargo", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="무너진 화물 칸을 뒤집니다. 날카로운 파편에 베이지 않게 조심해야 합니다. (체력 -3)"),
                        Action(type=ActionType.PRINT_NARRATIVE, value="쓸만한 물건들을 찾았습니다!\n**[녹슨 양동이]**, **[더러운 머그컵]**, **[전선 뭉치]**를 획득했습니다."),
                        Action(type=ActionType.MODIFY_STAMINA, value=-3),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BUCKET, "description": "바닥이 조금 찌그러진 양동이."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.CUP, "description": "I LOVE NY 로고가 박힌 머그컵."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.WIRE_BUNDLE, "description": "피복이 약간 벗겨진 전선 뭉치."}),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "searched_cargo", "value": True}),
                    ]
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="이미 샅샅이 뒤졌습니다. 더 이상 쓸만한 건 없어 보입니다.")])
            ]
        ),
        KeywordId.RUSTY_IRON: KeywordData(
            type=KeywordType.OBJECT, state=KeywordState.HIDDEN,
            description="선체에서 떨어져 나온 녹슨 철판이다. 가장자리가 거칠어서 잘만 갈면 **칼**처럼 쓸 수 있을 것 같다. 지금은 맨손이라 뜯어낼 수 없다."
        ),
        KeywordId.SKELETON: KeywordData(
            type=KeywordType.OBJECT, state=KeywordState.HIDDEN,
            description="구석에 하얀 뼈가 보인다... 건드리지 말자. 나도 저렇게 되고 싶진 않다."
        ),
    }
)