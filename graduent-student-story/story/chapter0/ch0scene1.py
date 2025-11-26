from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE1_DATA = SceneData(
    id=SceneID.CH0_SCENE1,
    name="제 2 연구실",
    body=(
        "문을 여는 순간, 콧속으로 숙성된 곰팡이의 향기가 훅 끼쳐온다.\n\n"
        "이곳은 제 2 연구실인가, 아니면 엔트로피가 극대화된 쓰레기장인가.\n\n"
        "구석에는 쓰레기통이 토해내듯 넘쳐흐르고 있고,\n\n"
        "벽면의 시약장은 봉인된 판도라의 상자처럼 굳게 닫혀 있다.\n\n"
        "그 옆에는 주인을 잃은 박스들이 위태롭게 탑을 쌓고 있다.\n\n"
        "책상 위 오래된 컴퓨터는 팬 돌아가는 소리조차 버거워 보이며,\n\n"
        "바닥에는 정체불명의 의문의 액체가 슬라임처럼 퍼져 있다.\n\n"
        "벽에 기댄 청소도구함만이 이 혼돈을 수습할 유일한 구원자처럼 보인다.\n\n"
    ),
    initial_state={
        "trash_step": 0,
        "wall_inspected": False,
        "liquid_cleaned": False,
        "box_opened": False,
        "cabinet_unlocked": False,
        "computer_solved": False,
        "key_found": False,
        "cleaning_cabinet_opened": False,
    },
    on_enter_actions=[
        Action(
            type=ActionType.PRINT_SYSTEM,
            value=(
                "연구실 생존을 위한 **새로운 조작법**을 알려드립니다.\n\n<br>"
                "**1. 명령어 기록 (History)**\n\n"
                "키보드 **[↑ / ↓]** 방향키를 눌러보세요. 이전에 입력했던 명령어들을 다시 불러올 수 있습니다.\n\n<br>"
                "**2. 화면 스크롤 (Scroll)**\n\n"
                "**[Shift] + [↑ / ↓]** 키를 누르면 마우스 없이도 지나간 텍스트를 위아래로 훑어볼 수 있습니다.\n\n<br>"
                "**3. 자동완성 (Auto Complete)**\n\n"
                "긴 단어를 다 치기 귀찮다면, 앞글자만 입력하고 **[Tab]** 키를 눌러보세요. 알아서 완성해줍니다.\n\n"
                "`둘`, `둘러`, `ㄷ`, `ㄷㄹ` 등을 입력하고 **[Tab]** 키를 눌러보세요.\n\n<br>"
                "이제 본문에 등장하는 **[키워드]**를 입력하여 조사를 시작하세요.\n\n"
                "내용이 기억나지 않으면 언제든 `둘러보기`를 입력하면 됩니다."
            ),
        )
    ],
    keywords={
        # --- 기존 핵심 오브젝트 (퍼즐용) ---
        KeywordId.COMPUTER_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.OLD_COMPUTER),
        # --- 1. 쓰레기통 조사 ---
        KeywordId.TRASH_CAN: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # [Step 0] 첫 번째 시도: 꽝 (쓰레기만 나옴)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "쓰레기통을 뒤적거려 보았다. 코를 찌르는 냄새와 함께 구겨진 논문 초안, 다 먹은 컵라면 용기, 코 푼 휴지 뭉치만 딸려 나온다.\n"
                                "손을 털고 일어서려는데, 쓰레기 더미 깊은 곳에서 무언가 '달그락'거리는 소리가 났다.\n"
                                "비위가 상하지만, 조금 더 깊이 파보면 쓸만한 게 나올지도 모른다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[쓰레기통]** 깊은 곳에 무언가 있는 것 같습니다. 다시 조사해 보세요.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "trash_step", "value": 1}),
                    ],
                ),
                # [Step 1] 두 번째 시도: 먼지 제거제 발견
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "숨을 참으며 쓰레기통을 더 깊숙이 뒤적거리자, 잡동사니 사이에서 **[먼지 제거제]** 캔이 손에 잡혔다.\n"
                                "가스는 다 빠져서 바람은 안 나오지만, 흔들어보니 찰랑거리는 액체 소리가 난다.\n\n"
                                '"학부생 녀석들, 액체 냉매가 절반이나 남았는데 이걸 그냥 버려? 연구비가 썩어나지?"\n\n'
                                "당신은 혀를 차며 캔을 주머니에 챙겼다.\n\n"
                                "쓰레기 더미 아래에 무언가 더 있는 것 같다."
                            ),
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.AIR_DUSTER,
                                "description": (
                                    "컴퓨터 청소용 에어 스프레이. 측면에 '절대 기울여 사용하지 마시오'라는 붉은 경고 문구가 있다.\n\n"
                                    "하지만 이공계생의 상식으로 볼 때, 이 문구는 **'뒤집어서 뿌리면 영하 50도의 급속 냉각기가 됨'**이라는 뜻과 같다.\n"
                                ),
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="**[쓰레기통]** 바닥에 아직 무언가 남아있는 것 같습니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "trash_step", "value": 2}),
                    ],
                ),
                # [Step 2] 세 번째 시도: 스패너 발견
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=2)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="다시 한번 바닥까지 싹싹 긁어 뒤지자, 제일 밑바닥에서 녹슨 **[스패너]**를 발견했다. 이제 쓰레기통은 완전히 비었다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.SPANNER,
                                "description": "녹슬었지만 묵직하다. 무언가를 강제로 열거나 부술 때 쓸만해 보인다.",
                            },
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "trash_step", "value": 3}),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.TRASH_CAN, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # [Step 3] 완료: 텅 빔
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=3)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="텅 빈 쓰레기통이다. 국물 자국과 절망만이 남아있다. 더 뒤져봤자 손만 더러워질 뿐이다.",
                        ),
                    ],
                ),
            ],
        ),
        KeywordId.BOX: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 아직 열지 않은 경우
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="box_opened", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "누군가 꼼꼼하게 포장해 둔 박스다. 테이프로 칭칭 감겨 있어 손톱으로는 뜯을 수 없다.\n"
                                "하지만 들어보니 **묵직한 무게감**이 느껴진다. 안에는 분명 **중요한 물건**이 들어있다.\n"
                                "테이프를 자를 만한 **날카로운 도구**가 필요하다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=(
                                "💡 **조합 시스템 가이드**\n\n"
                                "두 가지 요소를 **더하기(+)** 기호로 연결하여 새로운 결과를 만들어낼 수 있습니다.\n\n<br>"
                                "✅ **조합 가능:**\n\n"
                                "· `[주머니의 물건] + [주머니의 물건]` (아이템 결합)\n\n"
                                "· `[주머니의 물건] + [시야의 사물]` (아이템 사용)\n\n"
                                "· 예시: `법인카드 + 박스`\n\n<br>"
                                "🚫 **조합 불가능:**\n\n"
                                "· 단순한 배경 묘사나 환경 요소(예: 곰팡이, 엔트로피, 팬 등)는 조합의 대상이 아닙니다."
                            ),
                        ),
                    ],
                ),
                # Case 2: 이미 열어본 경우
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="box_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="이미 내용물을 꺼내고 남은 빈 박스다. 바닥에 뒹구는 테이프 조각들이 왠지 처량해 보인다.",
                        )
                    ],
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
                            type=ActionType.PRINT_NARRATIVE,
                            value="얼룩덜룩한 벽지를 자세히 보니, 구석에 꼬질꼬질한 **[메모]**가 하나 붙어있다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wall_inspected", "value": True}),
                        Action(
                            type=ActionType.DISCOVER_KEYWORD,
                            value=KeywordId.MEMO,
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.BOX, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="구석에 꼬질꼬질한 포스트잇 메모가 붙어있다.")
                    ]
                ),
            ],
        ),
        KeywordId.MEMO: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            silent_discovery=True,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_IMAGE,
                            value={
                                "src": "assets/chapter0/computer_memo.png",
                                "alt": "메모",
                                "width": "400",  # 이미지 크기 조절
                            },
                        ),
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "커피 얼룩이 묻은 낡은 포스트잇이다.\n"
                                "알 수 없는 기하학적인 그림이 그려져 있다. 암호인가? 아니면 그냥 낙서인가?\n"
                                "빨간색 화살표가 시작(START)과 끝(END)을 가리키고 있다."
                            ),
                        ),
                    ]
                )
            ],
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
                            value="컴퓨터 화면에는 `시약장 비밀번호: 0815` 라는 메모장 파일만 덩그러니 띄워져 있다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "전원 버튼을 누르자, 이륙하는 비행기 같은 소음을 내며 팬이 돌아간다.\n"
                                "키보드는 글자가 다 지워졌지만, **오른쪽 숫자 패드(Number Pad)**만큼은 손때가 타서 반질거린다.\n"
                                "Num Lock 키에 초록불이 깜빡이며 암호 입력창이 떴다."
                            ),
                        ),
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
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="시약장 문이 열려있다. 안에는 위험해 보이는(하지만 청소에는 유용한) 약품들이 널려있다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="굳게 닫힌 시약장이다. 4자리 숫자 자물쇠가 걸려있다. 보통 이런 건 생일이나 기념일로 해두던데.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`시약장 : [비밀번호]` 형식으로 열 수 있을 것 같다.",
                        ),
                    ]
                ),
            ],
        ),
        KeywordId.MYSTERY_LIQUID: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="손을 대보려다 말았다. 맨손으로 만졌다간 내 손도 바닥과 한 몸이 될 것 같다. 물리적인 방법보다는 화학적으로 해결해야 한다.",
                        )
                    ]
                )
            ],
        ),
        KeywordId.FLOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="끈적한 액체는 말끔히 사라졌다. 이제야 좀 사람 사는 곳의 바닥 같다.\n마무리로 **[빗자루]**질을 하면 완벽할 것이다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="바닥 한쪽에 **[의문의 액체]**가 흥건하다. 밟으면 신발 밑창이 녹을 것 같다. 저 흉물스러운 것을 먼저 처리해야 한다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.LAB_COAT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="key_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="가운 주머니를 뒤적거리자 짤그랑 소리가 난다. 주머니 속에서 작은 **[열쇠]**를 발견했다! 역시 가운은 입으라고 있는 게 아니라 수납하라고 있는 것이다.",
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.KEY,
                                "description": "작은 은색 열쇠. '청소'라고 적힌 라벨이 붙어있다.",
                            },
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "key_found", "value": True}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="새하얀 랩 가운이다. 더 이상 주머니에 든 것은 없다. 이제 이걸 입으면 나도 어엿한 연구 노예다.",
                        )
                    ]
                ),
            ],
            description="새하얀 랩 가운이다. 입으면 왠지 졸업에 한 발짝 다가간 기분...이 들 리가 없지.",
        ),
        KeywordId.CLEANING_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cleaning_cabinet_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="이미 열려있다. 안은 텅 비었다.")],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="녹슨 철제 캐비닛이다. 자물쇠로 단단히 잠겨있다. '청소도구함'이라고 매직으로 휘갈겨 써있다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="잠겨있습니다. 열 수 있는 도구가 필요합니다.",
                        ),
                    ]
                ),
            ],
        ),
        # --- 배경/분위기용 UNSEEN 오브젝트 (게임 플레이에 영향 없음) ---
        "문": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="철문에는 '관계자 외 출입금지'라고 적혀있다. 내가 바로 그 '관계자'라는 사실이 슬플 뿐이다. 도망칠 곳은 없다.",
        ),
        "곰팡이": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="벽지 무늬인 줄 알았는데 아니었다. 내 학위 논문보다 더 빠르게 증식하고 있는 생명체다.",
        ),
        "엔트로피": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="무질서도. 이 연구실에서 유일하게 꾸준히 증가하고 있는 수치다.",
        ),
        "제 2 연구실": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="나의 집이자, 감옥이자, 무덤이다. 월세는 내지 않지만 청춘을 지불하고 있다.",
        ),
        "쓰레기장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="정정한다. 쓰레기장은 주기적으로 비워지기라도 하지. 여긴 그보다 못하다.",
        ),
        "판도라의 상자": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="신화에서는 상자 바닥에 '희망'이 남았다지만, 이 시약장 바닥에는 '유통기한 지난 시약'만 남아있을 게 분명하다.",
        ),
        "탑": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="박스들이 위태롭게 쌓여 있다. 내 학점의 무게중심보다 훨씬 불안정해 보인다. 건드리면 와르르 무너질 것이다.",
        ),
        "팬": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="끼릭- 끼릭- 하고 비명을 지르고 있다. 죽여달라는 신호일까, 살려달라는 신호일까.",
        ),
        "슬라임": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="RPG 게임의 1레벨 몬스터가 아니다. 닿으면 체력(HP) 대신 피부를 깎아먹는 맹독성 슬라임이다.",
        ),
        "구원자": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="녹슨 청소도구함이 구원자라니. 내 인생의 구원자가 로또가 아니라 빗자루라는 사실을 받아들여야 한다.",
        ),
    },
    combinations=[
        Combination(
            targets=[KeywordId.BOX, KeywordId.CORP_CARD],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[법인카드]**의 날카로운 모서리로 테이프를 찢었다. (한도 초과된 카드라 마음이 덜 아프다.)\n박스를 열자 지저분한 **[실험용 랩 가운]**이 나왔다!",
                ),
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LAB_COAT),
                Action(type=ActionType.UPDATE_STATE, value={"key": "box_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.BOX, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # ... (기존 조합 유지 + 키패드 비밀번호 수정) ...
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.OLD_COMPUTER, "12365478"],  # [기획 반영] 키패드 패턴 'ㄹ' 뒤집은 모양
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="띠리링- 경쾌한음과 함께 잠금이 해제되었다!\n바탕화면 한구석에 `시약장 비밀번호: 내 생일 (0815)` 라는 메모 파일이 보인다.\n교수님 생일이 광복절이라니, 그래서 우리에게 광복은 언제 오는 걸까.",
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "computer_solved", "value": True}),
            ],
        ),
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.CABINET, "0815"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="철컥, 소리와 함께 **[시약장]** 문이 열렸다.\n안쪽 깊숙한 곳에서 공업용 **[에탄올]** 병을 발견했다. 알코올 냄새가 진동을 한다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ETHANOL,
                        "description": "순도 99% 공업용 에탄올. 마시면 실명, 뿌리면 소독. 명심하자.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "cabinet_unlocked", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.CLEANING_CABINET, KeywordId.KEY],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.KEY)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[열쇠]**를 꽂고 돌리자 경쾌한 '딸깍' 소리가 난다. 문을 열자 안에서 **[빗자루]**가 내 몸쪽으로 쓰러졌다.",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.BROOM,
                        "description": "다소 낡았지만 튼튼해 보이는 빗자루. 이걸로 바닥을 쓸면 내 마음의 번뇌도 쓸려나갈까.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "cleaning_cabinet_opened", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.KEY),
            ],
        ),
        # [네거티브 피드백] 스패너로 청소도구함 강제 개방 시도
        Combination(
            targets=[KeywordId.CLEANING_CABINET, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 자물쇠를 힘껏 내리쳐 보았다. 캉! 하는 소리만 요란하고 자물쇠는 멀쩡하다.\n내 손목만 아프다. 힘보다는 머리(혹은 열쇠)를 써야 할 때다.",
                )
            ],
        ),
        # [네거티브 피드백] 먼지 제거제(냉매)로 의문의 액체 얼리기 시도
        Combination(
            targets=[KeywordId.AIR_DUSTER, KeywordId.MYSTERY_LIQUID],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.AIR_DUSTER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[먼지 제거제]**를 뒤집어 액체 질소처럼 뿌려보았다.\n치익- 소리와 함께 액체가 하얗게 얼어붙었지만, 3초 뒤 다시 녹아 끈적해졌다.\n단순한 물리적 냉각으로는 해결되지 않는다. 화학적인 중화제가 필요하다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.ETHANOL, KeywordId.MYSTERY_LIQUID],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ETHANOL)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[에탄올]**을 들이붓자, 치이익 소리와 함께 끈적한 **[의문의 액체]**가 거품처럼 녹아내렸다!\n잠시 후, 바닥이 뽀득뽀득해졌다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ETHANOL),
                Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.MYSTERY_LIQUID),
                Action(type=ActionType.UPDATE_STATE, value={"key": "liquid_cleaned", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 **[바닥]**을 빗자루로 청소할 수 있을 것 같습니다."),
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=False),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BROOM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="바닥의 끈적한 **[의문의 액체]** 때문에 **[빗자루]**가 쩍쩍 달라붙는다. 억지로 쓸다간 빗자루 털이 다 빠질 것 같다. 액체부터 없애야 한다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True),
                Condition(type=ConditionType.STATE_NOT, target="trash_step", value=2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BROOM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="바닥은 깨끗해졌지만, 아직 **[쓰레기통]**이 넘쳐흐르고 있다. 쓰레기부터 마저 치워야 완벽한 청소가 될 것 같다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True),
                Condition(type=ConditionType.STATE_IS, target="trash_step", value=2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.BROOM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="마지막으로 **[빗자루]**를 들어 바닥의 먼지를 쓸어냈다.\n"
                    "창고 같던 연구실이 이제야 좀 사람 사는 곳처럼 보인다.\n"
                    "이마의 땀을 닦으며 허리를 펴는 순간, 복도에서 발소리가 들린다...",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BROOM),
                Action(type=ActionType.MOVE_SCENE, value=SceneID.CH0_SCENE2),
            ],
        ),
    ],
)
