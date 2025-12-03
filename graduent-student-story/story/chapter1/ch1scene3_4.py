from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE3_4_DATA = SceneData(
    id=SceneID.CH1_SCENE3_4,
    name="통제실",
    body=(
        "모니터 불빛 하나 없는 어두운 통제실입니다.\n\n"
        "중앙에 컴퓨터가 놓여 있고, 모니터 귀퉁이에는 노란색 접착 메모가 붙어 있습니다.\n\n"
        "이곳의 시스템을 복구해야 연구소의 비밀을 풀 수 있을 것 같습니다."
    ),
    initial_state={
        "computer_unlocked": False,
        "hallway_inspected": False,
        "file_discovered": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.MEMO: KeywordData(type=KeywordType.ALIAS, target=KeywordId.STICKY_NOTE),
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
                            value="육중한 철문입니다. 밖으로 나가면 다시 중앙 복도로 이어집니다.",
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
                                "prompt": "통제실을 나가 **[연구동 중앙 복도]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="철문을 밀고 복도로 나갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_1),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 시스템을 점검해야 합니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 접착 메모 (암호 힌트)
        KeywordId.STICKY_NOTE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "모니터에 붙은 메모입니다. 의미를 알 수 없는 문자열이 적혀 있습니다.\n\n"
                '"Password Hint: XRVY-N4DF-6HFD-467GTYUI"'
            ),
        ),
        # 2. 메인 컴퓨터
        KeywordId.COMPUTER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 전력이 들어오지 않음 (Observatory Power Restored 확인)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="observatory_power_restored", value=False)
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="전원 버튼을 눌러봤지만 반응이 없습니다. 외부 배전반에서 전력을 먼저 복구해야 합니다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="observatory_power_restored", value=True),
                        Condition(type=ConditionType.STATE_IS, target="computer_unlocked", value=True),
                        Condition(type=ConditionType.STATE_IS, target="file_discovered", value=False),
                    ],
                    actions=[
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.FILE_MUSIC),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.FILE_DNA),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.FILE_TEMP),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "file_discovered", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # Case 2: 전력 ON, 잠금 해제됨
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="observatory_power_restored", value=True),
                        Condition(type=ConditionType.STATE_IS, target="computer_unlocked", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "바탕화면이 보입니다. 파일 여러 개가 있습니다.\n\n"
                                f"① **[{KeywordId.FILE_MUSIC}]**\n\n"
                                f"② **[{KeywordId.FILE_DNA}]**\n\n"
                                f"③ **[{KeywordId.FILE_TEMP}]**\n\n"
                            ),
                        ),
                    ],
                ),
                # Case 3: 전력 ON, 잠겨 있음 (비밀번호 입력 유도)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.CHAPTER_STATE_IS, target="observatory_power_restored", value=True),
                        Condition(type=ConditionType.STATE_IS, target="computer_unlocked", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "팬 돌아가는 소리와 함께 부팅 화면이 떴습니다.\n\n[ SYSTEM LOCKED ]\nEnter Password:\n\n"
                                '<img src="assets/chapter1/keyboard.png" alt="키보드" width="530">\n\n'
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.COMPUTER} : [비밀번호 4자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
            ],
        ),
        # 3. 파일들
        KeywordId.FILE_MUSIC: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=('<img src="assets/chapter1/CDEFGAB.png" alt="계이름 표기법" width="530">\n\n'),
        ),
        KeywordId.FILE_DNA: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=('<img src="assets/chapter1/DNA.png" alt="DNA" width="530">\n\n'),
        ),
        KeywordId.FILE_TEMP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "< 실험체 303 반응 임계점 로그 >\n\n"
                "가상의 4분할 지점에서 도출된 최적의 반응 온도를 기록함.\n\n"
                "온도 조절기 오차 수정 완료.\n\n"
                "**Phase 1 (동면/침묵): 5℃**\n"
                " - 생체 활동 정지. 완전한 고요.\n\n"
                "**Phase 2 (각성/단음): 20℃**\n"
                " - 활동 개시. 간헐적 신호 발생.\n\n"
                "**Phase 3 (활동/장음): 30℃**\n"
                " - 정상 활동 범위. 지속적 신호 발생.\n\n"
                "**Phase 4 (폭주/광란): 35℃**\n"
                " - 임계점 초과. 비선형적 패턴 발생."
            ),
        ),
        # --- UNSEEN 오브젝트 (통제실) ---
        "모니터": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="꺼진 화면은 검은 거울 같다. 꾀죄죄한 내 얼굴이 비쳐서 깜짝 놀랐다. 귀신인 줄 알았네.",
        ),
        "비밀": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이 컴퓨터 안에 모든 진실이 잠들어 있다. 판도라의 상자다. 열면 희망이 나올까, 아니면 또 다른 절망이 나올까?",
        ),
    },
    combinations=[
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.COMPUTER, "3571"],
            conditions=[
                Condition(type=ConditionType.CHAPTER_STATE_IS, target="observatory_power_restored", value=True)
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="띠리릭! 액세스 승인.\n\n잠금이 해제되고 바탕화면 아이콘들이 나타납니다.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "computer_unlocked", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.STICKY_NOTE, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.RESEARCH_LOG,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_2,
                    },
                ),
            ],
        ),
    ],
)
