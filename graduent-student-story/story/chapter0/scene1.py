from const import ActionType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID, CombinationType
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE1_DATA = SceneData(
    id=SceneID.CH0_SCENE1,
    name="제 2 연구실",
    initial_text="문을 열자 퀴퀴한 곰팡이 냄새와 먼지가 뒤섞여 코를 찌른다. 이곳은 신성한 연구실인가, 고고학 발굴 현장인가.\n\n구석에는 정체를 알 수 없는 쓰레기통이 넘칠 듯이 차 있고, 벽 한쪽에는 굳게 닫힌 시약장과 낡은 박스들이 산더미처럼 쌓여 있다.\n먼지 쌓인 오래된 컴퓨터는 켜지기는 할지 의문이며, 바닥에는 정체불명의 의문의 액체가 흥건하다. 그 옆에 빗자루가 굴러다닌다.",
    initial_state={
        "trash_step": 0,
        "wall_inspected": False,
        "liquid_cleaned": False,
        "box_opened": False,
        "cabinet_unlocked": False,
        "computer_solved": False,
    },
    keywords={
        KeywordId.WALL_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WALL),
        KeywordId.COMPUTER_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.OLD_COMPUTER),
        KeywordId.DOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="이미 끔찍한 곳에 와있는데, 굳이 돌아갈 필요는 없어 보인다.",
        ),
        KeywordId.TRASH_CAN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="쓰레기통을 뒤적거리자, 먹다 남은 **[에너지바 껍질]**을 찾았다. 쓰레기 더미 아래에 무언가 더 있는 것 같다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.WRAPPER, "description": "눅눅하고 비어있다."},
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="`쓰레기통`을 다시 한번 입력해 보세요."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "trash_step", "value": 1}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다시 한번 쓰레기통을 뒤지자, 깊숙한 곳에서 녹슨 **[스패너]**를 발견했다. 이제 쓰레기통은 완전히 비었다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.SPANNER, "description": "녹슬었지만 쓸만해 보인다."},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "trash_step", "value": 2}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE, value="텅 빈 쓰레기통이다. 더는 아무것도 나오지 않는다."
                        )
                    ],
                ),
            ],
        ),
        KeywordId.BOX: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="box_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="안에는 아무것도 없는 빈 박스다.")],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="테이프로 칭칭 감겨 있다. 손톱으로는 뜯을 수 없을 것 같다. 날카로운 게 필요하다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="힌트: `도구 + 대상` 형태로 조합해 보세요. (예: `법인카드 + 박스`)",
                        ),
                    ]
                ),
            ],
        ),
        KeywordId.WALL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wall_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE, value="벽지를 자세히 보니, 구석에 작은 메모가 붙어있다."
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wall_inspected", "value": True}),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MEMO, "state": KeywordState.HIDDEN},
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="새롭게 눈에 띄는 것이 있는 것 같습니다."),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[시야]** 에 새로운 [?] 가 추가되었습니다. 사물의 설명 텍스트에 등장하는 단어를 직접 입력하여 조사할 수 있습니다.",
                        ),
                    ],
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="구석에 작은 메모가 붙어있다.")]),
            ],
        ),
        KeywordId.MEMO: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            silent_discovery=True,
            description="벽에 붙어있는 메모에는 '컴퓨터 비밀번호: 1에서 시작하고 8로 끝나는 여덟자리 숫자' 라고 적혀있다.",
        ),
        KeywordId.OLD_COMPUTER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="computer_solved", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="컴퓨터 화면에는 `시약장 비밀번호: 0815` 라는 메모만 띄워져 있다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="전원 버튼을 누르자, 잠시 팬이 돌다가 암호 입력창이 뜬다.",
                        ),
                        # [수정] 힌트 텍스트 변경: + 대신 : 사용
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="암호를 알아내어 `컴퓨터 : [비밀번호]` 형식으로 입력해야 할 것 같다.",
                        ),
                    ]
                ),
            ],
        ),
        KeywordId.CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cabinet_unlocked", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="시약장 안에는 잡다한 약품들이 널려있다.")],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="자물쇠가 걸려있다.",
                        ),
                        # [수정] 힌트 텍스트 변경: + 대신 : 사용
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`시약장 : [비밀번호]` 형식으로 열 수 있을 것 같다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.MYSTERY_LIQUID: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="바닥에 끈적하게 눌어붙은 액체다. 무슨 성분인지 알 수 없지만, 달콤한 향이 나는 것 같다.",
        ),
        KeywordId.FLOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="바닥 한쪽에 **[의문의 액체]**가 흥건하다. 끈적해서 밟고 싶지 않다.",
        ),
        KeywordId.BROOM: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="평범한 빗자루다. 바닥을 청소할 수 있을 것 같다.",
        ),
        KeywordId.LAB_COAT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="새하얀 랩 가운이다. 입으면 왠지 졸업에 한 발짝 다가간 기분이 든다.",
        ),
        KeywordId.ETHANOL: KeywordData(
            type=KeywordType.ITEM,
            state=KeywordState.INACTIVE,
            description="소독 및 청소용. 마시지 마시오.",
        ),
    },
    combinations=[
        # 1. 컴퓨터 비밀번호 (타입: PASSWORD)
        Combination(
            type=CombinationType.PASSWORD,  # [중요] 비밀번호 타입 지정
            targets=[KeywordId.OLD_COMPUTER, "12345678"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="암호가 맞았다! 컴퓨터 화면에 메모장 파일 하나가 띄워져 있다.\n\n`시약장 비밀번호: 내 생일 (0815)`",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "computer_solved", "value": True}),
            ],
        ),
        # 2. 시약장 비밀번호 (타입: PASSWORD)
        Combination(
            type=CombinationType.PASSWORD,  # [중요] 비밀번호 타입 지정
            targets=[KeywordId.CABINET, "0815"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="철컥, 소리와 함께 **[시약장]** 문이 열렸다. 안에서 **[에탄올]** 병을 발견했다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.ETHANOL, "description": "강력한 세정제입니다."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "cabinet_unlocked", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.BOX, KeywordId.CORP_CARD],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[법인카드]** 모서리로 테이프를 잘라냅니다. 안에서 새하얀 **[실험용 랩 가운]**을 발견했습니다!",
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.LAB_COAT, "state": KeywordState.DISCOVERED},
                ),
                Action(type=ActionType.PRINT_SYSTEM, value="**[실험용 랩 가운]**이 시야에 추가되었습니다."),
                Action(type=ActionType.UPDATE_STATE, value={"key": "box_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.BOX, "state": KeywordState.DISCOVERED},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.ETHANOL, KeywordId.MYSTERY_LIQUID],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ETHANOL)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[에탄올]**을 붓자, 끈적한 **[의문의 액체]**가 녹아내리며 바닥이 깨끗해졌다!",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ETHANOL),
                Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.MYSTERY_LIQUID),
                Action(type=ActionType.UPDATE_STATE, value={"key": "liquid_cleaned", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 **[빗자루]**로 **[바닥]**을 청소할 수 있을 것 같다."),
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True),
                Condition(type=ConditionType.STATE_IS, target="trash_step", value=2),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="깨끗해진 바닥을 **[빗자루]**로 쓸어 마무리 청소를 합니다...",
                ),
                Action(type=ActionType.MOVE_SCENE, value=SceneID.CH0_SCENE2),
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="바닥의 끈적한 **[의문의 액체]** 때문에 **[빗자루]**질을 할 수가 없다. 저걸 먼저 녹여야 한다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True),
                Condition(type=ConditionType.STATE_NOT, target="trash_step", value=2),
            ],
            actions=[
                Action(type=ActionType.PRINT_SYSTEM, value="아직 **[쓰레기통]**이 정리되지 않은 것 같다. 마저 치우자.")
            ],
        ),
    ],
)