from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_0_DATA = SceneData(
    id=SceneID.CH1_SCENE2_0,  # 혹은 SceneID.CH1_SCENE2_0 (정의에 따라 변경)
    name="난파선 중앙 복도",
    body=(
        '"으악! 이게 무슨 냄새야? 코가 삐뚤어질 것 같네."\n\n'
        "난파선 안으로 들어오니 썩은 생선이랑 녹슨 쇠를 믹서기에 갈아 넣은 듯한 냄새가 콧구멍을 강타합니다.\n"
        "어두침침한 복도를 둘러보니 문이 몇 개 보입니다.\n\n"
        "왼쪽엔 문짝이 덜렁거리는 선원 숙소, 오른쪽엔 왠지 있어 보이는 선장실.\n"
        "저 안쪽에는 쇠사슬로 칭칭 감긴 갑판 뒷편 문이 있고, 그 옆엔 시커먼 아가리 같은 지하실 입구가 보입니다.\n\n"
        "으스스한 게 딱 귀신 나오기 좋은 분위기지만, 살려면 뭐라도 뒤져봐야겠지요.\n"
        "뒤로 나가면 나의 소중한 스위트 홈, 베이스캠프로 돌아갈 수 있습니다."
    ),
    initial_state={
        "beach_path_inspected": False,
        "crew_path_inspected": False,
        "captain_path_inspected": False,
        "deck_path_inspected": False,
        "basement_path_inspected": False,
    },
    on_enter_actions=[],
    keywords={
        # 1. 베이스캠프 - 제공해주신 코드 그대로 적용
        KeywordId.BASECAMP: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="서쪽을 보니 베이스캠프가 아지랑이 속에 보인다. 돌아가는 길도 험난해 보인다. (체력 소모 예상)",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "beach_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="beach_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": ("**[베이스캠프]**로 돌아가시겠습니까?\n\n체력이 2 소모됩니다."),
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="뜨거운 모래사장을 가로질러 베이스캠프로 복귀합니다.",
                                    ),
                                    Action(type=ActionType.MODIFY_STAMINA, value=-2),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="조금 더 조사가 필요합니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 2. 선원 숙소
        KeywordId.CREW_QUARTERS: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="crew_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='"문짝 꼬라지 하고는..."\n\n문이 반쯤 부서져 있어 안이 훤히 들여다보입니다. 퀴퀴한 곰팡이 냄새가 풀풀 풍깁니다.',
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "crew_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="crew_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[선원 숙소]**를 조사하시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="코를 막고 선원 숙소 안으로 들어갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_1),  # 연결될 씬 ID
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="다른 곳을 먼저 둘러봅니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 3. 선장실
        KeywordId.CAPTAIN_ROOM: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="captain_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="'Captain'이라고 적힌 명패가 삐딱하게 붙어 있습니다. 선장실이라면 뭔가 쓸만한 게(특히 먹을 거라던가) 있지 않을까요?",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "captain_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="captain_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[선장실]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="예의 바르게 노크...는 생략하고 문을 엽니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_2),  # 연결될 씬 ID
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="나중에 들어가 봅니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 4. 갑판 뒷편
        KeywordId.REAR_DECK: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="deck_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="철문이 아주 야무지게도 잠겨 있습니다. 녹슨 쇠사슬로 칭칭 감겨 있는데, 맨손으로는 어림도 없겠는데요.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "deck_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="deck_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[갑판 뒷편]**으로 나가보시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="문을 열고 갑판으로 나갑니다.",
                                    ),
                                    # Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE_DECK), # 연결될 씬 ID
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE, value="열쇠나 도구를 찾은 뒤에 다시 옵니다."
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 5. 지하실 입구
        KeywordId.BASEMENT_ENTRANCE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="basement_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="시커먼 어둠이 입을 벌리고 있는 계단입니다. 게다가 거대한 강철 격벽이 길을 떡하니 막고 있습니다. 보기만 해도 숨이 턱 막히네요.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "basement_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="basement_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[지하실 입구]**를 자세히 살펴보시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="격벽 앞으로 다가갑니다.",
                                    ),
                                    # Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE_BASEMENT), # 연결될 씬 ID
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="무서워서 나중에 갑니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
    },
    combinations=[],
)
