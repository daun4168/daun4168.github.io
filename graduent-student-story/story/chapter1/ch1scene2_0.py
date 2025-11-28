from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Condition, Interaction, KeywordData, SceneData
from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData


CH1_SCENE2_0_DATA = SceneData(
    id=SceneID.CH1_SCENE2_0,  # 혹은 SceneID.CH1_SCENE2_0 (정의에 따라 변경)
    name="난파선 중앙 복도",
    body=(
        '"으악! 이게 무슨 냄새야? 코가 삐뚤어질 것 같네."\n\n'
        "난파선 안으로 들어오니 썩은 생선이랑 녹슨 쇠를 믹서기에 갈아 넣은 듯한 냄새가 콧구멍을 강타합니다.\n"
        "어두침침한 복도를 둘러보니 문이 몇 개 보입니다.\n\n"
        "왼쪽엔 문짝이 덜렁거리는 선원 숙소, 오른쪽엔 왠지 있어 보이는 선장실.\n"
        "저 안쪽에는 쇠사슬로 칭칭 감긴 갑판 뒷편 문이 있고, 그 옆엔 아래로 내려가는 길을 육중하게 가로막은 강철 격벽이 보입니다.\n\n"
        "으스스한 게 딱 귀신 나오기 좋은 분위기지만, 살려면 뭐라도 뒤져봐야겠지요.\n"
        "뒤로 나가면 나의 소중한 스위트 홈, 베이스캠프로 돌아갈 수 있습니다."
    ),
    initial_state={
        "beach_path_inspected": False,
        "crew_path_inspected": False,
        "captain_path_inspected": False,
        "deck_path_inspected": False,
        "basement_path_inspected": False,
        "deck_unlocked": False,
        "door_heated": False,
        "door_frozen": False,
        "door_opened": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.DECK: KeywordData(type=KeywordType.ALIAS, target=KeywordId.REAR_DECK),
        KeywordId.REAR_DECK_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.REAR_DECK),
        KeywordId.BULKHEAD: KeywordData(type=KeywordType.ALIAS, target=KeywordId.IRON_DOOR),
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
            state=KeywordState.DISCOVERED,
            interactions=[
                # Case 1: 잠금 해제됨 (이동 가능)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="deck_unlocked", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[갑판 뒷편]**으로 나가보시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="문을 열고 시원한(혹은 비린내 나는) 바닷바람을 맞으러 갑판으로 나갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_4),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 준비가 안 됐습니다."),
                                ],
                            },
                        ),
                    ],
                ),
                # Case 2: 잠김 + 열쇠 보유 (열쇠 구멍 없음 -> 비밀번호 유도)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="deck_unlocked", value=False),
                        Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DECK_KEY),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "당당하게 주머니에서 **[갑판 열쇠]**를 꺼냈습니다. 그런데... 어라?\n\n"
                                "자물쇠에 열쇠 구멍이 없습니다. 대신 낡은 번호키만 덩그러니 달려 있네요.\n\n"
                                '"뭐야, 이 열쇠는 장식인가?"'
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.REAR_DECK} : [비밀번호]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                # Case 3: 잠김 + 열쇠 없음 (기본 조사)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="deck_unlocked", value=False),
                        Condition(type=ConditionType.NOT_HAS_ITEM, target=KeywordId.DECK_KEY),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "철문이 아주 야무지게도 잠겨 있습니다. 녹슨 쇠사슬로 칭칭 감겨 있는데, 맨손으로는 어림도 없겠는데요.\n\n"
                                "어딘가에 이 사슬을 풀 열쇠가 있을 겁니다. 선장실 같은 곳을 뒤져봐야겠습니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "deck_path_inspected", "value": True}),
                    ],
                ),
            ],
        ),
        # 5. 지하실 입구
        KeywordId.BASEMENT_ENTRANCE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.INACTIVE,
            interactions=[
                # 1. 전력 복구 안 됨 (Still Dark)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="basement_power_restored", value=False)
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "강철 격벽은 산산조각 나 문은 열려 있지만, 계단 아래는 칠흑 같은 어둠입니다.\n\n"
                                "이렇게 어두운 곳에서는 한 발짝도 움직일 수 없습니다. 추락할 위험이 있습니다.\n\n"
                                "지하실의 전력을 복구해야 합니다."
                            ),
                        ),
                    ],
                ),
                # 2. 전력 복구됨 (Lights ON - 진입 가능)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="basement_power_restored", value=True)
                    ],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "지하실에 불이 들어왔습니다. **[지하실]**로 내려가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="어둠이 걷히자 눅눅한 계단이 보입니다. 지하실로 내려갑니다...",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3),  # 다음 씬 ID로 이동
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="일단 복도로 돌아와 다른 곳을 마저 확인합니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 6. 강화 격벽 (메인 퍼즐)
        KeywordId.IRON_DOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="군용 수송선급의 두꺼운 격벽입니다. 잠금 휠은 녹슬어 본체와 한 몸이 되었습니다. 물리적인 힘으로 여는 건 불가능해 보입니다. 재질은 고장력강(High Tensile Steel). 열역학적으로 접근해야 할 것 같습니다.",
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="잠금장치가 산산조각 나 문이 열려 있습니다. 어두운 **[지하실 입구]**가 보입니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.IRON_DOOR, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_frozen", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="하얗게 성에가 낀 문에서 '쩡, 쩡' 하는 금속 비명 소리가 들립니다. 미세한 균열이 보입니다. 지금이라면 충격을 주어 깰 수 있을 것 같습니다.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="시뻘겋게 달아올라 엄청난 열기를 내뿜고 있습니다. 금속이 팽창해 터질 듯합니다. 지금 식혀야 합니다... 아주 급격하게.",
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="급속 냉각 수단이 필요합니다."),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="꿈쩍도 안 합니다. 틈새가 없어 지렛대도 들어가지 않습니다. 금속의 성질을 변화시켜야 합니다.",
                        ),
                    ]
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (난파선 복도) ---
        "믹서기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이 악취는 천재 화학자가 아니라면 만들 수 없다. 내 전공 지식을 총동원해도 이런 끔찍한 조합은 불가능하다.",
        ),
        "썩은 생선": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="모든 악취의 근원. 혹시 이걸 먹으면 힘이 날까? (미친 생각이다. 그냥 굶어 죽자.)",
        ),
        "녹슨 쇠": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="만지는 순간 파상풍에 걸릴 것 같다. 이 쇳가루가 모두 금가루였으면 얼마나 좋았을까.",
        ),
        "쇠사슬": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="굵기가 내 팔뚝만 하다. 이걸 끊으려면 염산이나 이 배의 주인이 가진 비밀번호가 필요할 것이다.",
        ),
        "귀신": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="보이지 않지만 분명 존재할 것이다. 이 배의 선장이나 기관사가 '왜 나만 죽었냐?'며 뒤를 따라다니고 있을 것이다.",
        ),
        "스위트 홈": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="야자수 그늘 아래의 찌그러진 가마솥이 전부다. 하지만 이 썩은 배보다는 백배 천배 낫다. 나의 안식처다.",
        ),
        "코": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="코는 두 개인데 냄새는 백만 가지가 난다. 이대로 코를 떼어버리고 싶다.",
        ),
        "어둠": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="곰팡이 냄새와 썩은 물이 뒤섞인 액체화된 어둠 같다. 마시는 순간 질식할 것 같은 압력이 느껴진다.",
        ),
        "본능": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="뒤져야 살 수 있다는 원초적인 생존 본능이다. 가만히 있다가는 여기서 굶어 죽는다.",
        ),
        "문짝": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="덜렁거린다. 경첩이 녹슬어 금방이라도 떨어질 것 같다. 내 학위 논문 심사 때의 멘탈처럼 위태롭다.",
        ),
        "복도": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="길이가 길어 보인다. 누가 뒤에서 쫓아오면 죽어라 달려도 도망 못 갈 것 같다.",
        ),
    },
    combinations=[
        # 갑판 잠금 해제 (갑판 열쇠 : 3817)
        # 3817이라는 비밀번호는 갑판 열쇠 아이템이나 쪽지에서 힌트로 얻었다고 가정
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.REAR_DECK, "3817"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "철컥!\n\n"
                        "자물쇠가 풀리면서 쇠사슬이 요란한 소리를 내며 바닥으로 떨어집니다.\n"
                        "이제 문을 열고 밖으로 나갈 수 있습니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "deck_unlocked", "value": True}),
            ],
        ),
        # 1. 가열: 조명탄 + 격벽
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.FLARE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="치익! 조명탄을 터뜨려 문 손잡이 틈새에 꽂아 넣었습니다.\n\n눈부신 백색 섬광과 함께 강철이 시뻘겋게 달아오르며 팽창하기 시작합니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FLARE),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_heated", "value": True}),
            ],
        ),
        # 2. 급랭: 먼지제거제 + 격벽
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="먼지제거제를 거꾸로 뒤집어 잡고, 달궈진 문고리를 향해 액체 냉매를 발사했습니다.\n\n**콰아아-!**\n\n2,000도의 열기와 영하 50도의 냉기가 충돌했습니다. 엄청난 수증기와 함께 금속 표면에 거미줄 같은 균열이 발생합니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.AIR_DUSTER),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_frozen", "value": True}),
            ],
        ),
        # 2-1. 힌트 제공
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.AIR_DUSTER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_heated", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="차가운 강철에 냉매를 뿌려봐야 소용없습니다. '열충격'을 주려면 먼저 금속을 뜨겁게 달궈야 합니다.",
                )
            ],
        ),
        # 3. 파괴: 스패너 + 격벽 (지하 통로 등장)
        Combination(
            targets=[KeywordId.IRON_DOOR, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="door_frozen", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="스패너로 하얗게 얼어붙은 잠금장치를 가볍게 내리쳤습니다.\n\n**채앵-그랑!**\n\n유리가 깨지듯 잠금장치가 산산조각 나 바닥으로 쏟아집니다. 육중한 격벽이 끼이익 소리를 내며 열립니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "door_opened", "value": True}),
                # [핵심] 지하 통로 키워드 활성화 (INACTIVE -> DISCOVERED)
                Action(
                    type=ActionType.DISCOVER_KEYWORD,
                    value=KeywordId.BASEMENT_ENTRANCE,
                ),
            ],
        ),
    ],
)
