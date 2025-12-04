from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE1_DATA = SceneData(
    id=SceneID.CH0_SCENE1,
    name="제 2 연구실",
    initial_text="---\n## 제 2 연구실\n---\n",
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
        KeywordId.WALL_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WALL),
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
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="trash_step", value=3)],
                    actions=[
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.TRASH_CAN, "state": KeywordState.UNSEEN},
                        ),
                    ],
                    continue_matching=True,
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
        # --- 2. 박스 조사, 박스 개봉 ---
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
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.BOX, "state": KeywordState.UNSEEN},
                        ),
                    ],
                    continue_matching=True,
                ),
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
        # --- 3. 실험용 랩 가운 조사, 열쇠 획득 ---
        KeywordId.LAB_COAT: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="key_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "가운 주머니를 뒤적거리자 짤그랑 소리가 난다.\n\n"
                                "주머니 속에서 작은 **[열쇠]**를 발견했다!\n\n"
                                "역시 가운은 입으라고 있는 게 아니라 수납하라고 있는 것이다."
                            ),
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
                    conditions=[Condition(type=ConditionType.STATE_IS, target="key_found", value=True)],
                    actions=[
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.LAB_COAT, "state": KeywordState.UNSEEN},
                        ),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="key_found", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="새하얀 랩 가운이다. 더 이상 주머니에 든 것은 없다. 이제 이걸 입으면 나도 어엿한 연구 노예다.",
                        ),
                    ],
                ),
            ],
        ),
        # --- 4. 청소도구함 + 열쇠, 빗자루 획득 ---
        KeywordId.CLEANING_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cleaning_cabinet_opened", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="녹슨 철제 캐비닛이다. 자물쇠로 단단히 잠겨있다. '청소도구함'이라고 매직으로 휘갈겨 써있다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="잠겨있습니다. 열 수 있는 도구가 필요합니다.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cleaning_cabinet_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.CLEANING_CABINET, "state": KeywordState.UNSEEN},
                            continue_matching=True,
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cleaning_cabinet_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="이미 열려있다. 안은 텅 비었다.")],
                ),
            ],
        ),
        # --- 5. 벽에서 메모 발견 ---
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
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wall_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.WALL, "state": KeywordState.UNSEEN},
                        ),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wall_inspected", value=True)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="구석에 꼬질꼬질한 포스트잇 메모가 붙어있다.")
                    ],
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
                                "커피 얼룩이 묻은 낡은 포스트잇이다.\n\n"
                                "알 수 없는 기하학적인 그림이 그려져 있다. 암호인가? 아니면 그냥 낙서인가?"
                            ),
                        ),
                    ]
                )
            ],
        ),
        # --- 6. 컴퓨터 비밀번호 잠금 해제, 주문 내역 획득 ---
        KeywordId.COMPUTER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="computer_solved", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "전원 버튼을 누르자, 이륙하는 비행기 같은 소음을 내며 팬이 돌아간다.\n"
                                "키보드는 글자가 다 지워졌지만, 오른쪽 **숫자 패드**만큼은 손때가 타서 반질거린다.\n\n"
                                '<img src="assets/chapter0/computer_keypad.png" alt="키패드" width="300">\n\n'
                                "Num Lock 키에 초록불이 깜빡이며 암호 입력창이 떴다.\n\n"
                                "이런 복잡한 암호를 맨정신으로 외우고 다닐 리가 없다.\n"
                                "분명 주변 어딘가, 눈에 잘 띄는 **벽** 같은 곳에 **메모**를 해뒀을 것이다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.COMPUTER} : [비밀번호 6자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="computer_solved", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "화면에 **[주문내역]** 페이지가 떠 있다.\n\n"
                                "브라우저 창 옆 바탕화면에는 `시약장_비번_주문수량_제발까먹지마.txt` 라는 처절한 이름의 텍스트 파일이 보인다."
                            ),
                        )
                    ],
                ),
            ],
        ),
        KeywordId.ORDER_LIST: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,  # 처음엔 숨겨져 있음
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "웹 브라우저에 '랩-마켓(Lab-Market)' 최근 주문 내역이 띄워져 있다.\n"
                                "배송 상태가 **배송 완료**로 되어 있는 최근 4건의 목록이다.\n\n"
                                "· [실험] 공업용 에탄올 (99%) ------- **2** Box\n\n"
                                "· [기자재] 백금 코팅 비커 세트 ------ **0** Set (주문 취소됨: 사유-예산 초과)\n\n"
                                "· [소모품] 대용량 킴와이프 --------- **1** Box\n\n"
                                "· [식비] 얼큰한 매운맛 컵라면 ------ **9** Box\n\n<br>"
                                "스크롤을 내려보니 '연구 책임자(교수) 승인 완료' 도장이 찍혀 있다."
                            ),
                        ),
                    ]
                )
            ],
        ),
        # --- 7. 시약장 비밀번호 잠금 해제, 에탄올 획득 ---
        KeywordId.REAGENT_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # Case 1: 잠겨 있음 (라벨 힌트 제공)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cabinet_unlocked", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "유리문으로 된 견고한 시약장이다. 4자리 숫자 자물쇠로 잠겨 있다.\n\n"
                                "유리문에는 보관 품목을 표시하는 라벨이 왼쪽부터 오른쪽 순서대로 붙어있다.\n\n"
                                "🏷️ **킴와이프** - **비커** - **에탄올** - **컵라면**\n\n"
                                "시약장에 컵라면을 넣는 건 명백한 안전 수칙 위반이지만, 대학원생에게는 밥이 더 중요한 모양이다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="암호를 알아내어 `시약장 : [비밀번호 4자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
                # Case 2: 잠금 해제됨
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cabinet_unlocked", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="시약장 문이 열려있다. 안에는 위험해 보이는 약품들과 컵라면이 위태롭게 공존하고 있다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.REAGENT_CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
            ],
        ),
        # -- 8. 의문의 액체 제거, 빗자루질 ---
        KeywordId.FLOOR: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="바닥 한쪽에 **의문의 액체**가 흥건하다. 손을 대보려다 말았다.\n\n물리적인 방법보다는 화학적으로 해결해야 할 것 같다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="끈적한 액체는 말끔히 사라졌다. 이제야 좀 사람 사는 곳의 바닥 같다.\n\n마무리로 **[빗자루]**질을 하면 완벽할 것이다.",
                        )
                    ],
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
        "향기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="향기라니, 당치도 않다. 이건 묵은 먼지, 곰팡이, 그리고 식어버린 컵라면 국물이 섞인 '절망'의 냄새다. 샤넬 No.5 대신 'Lab No.2' 향수를 런칭해도 되겠다.",
        ),
        "콧속": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="비염이 도질 것 같다. 이곳의 공기 청정도는 '매우 나쁨'이 확실하다. 마스크를 쓰고 들어올 걸 그랬다.",
        ),
        "구석": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="어둠이 내려앉은 공간이다. 먼지 뭉치들이 자기들끼리 문명을 이룩하고 있다. 저 깊은 곳에 잃어버린 내 USB가 있을지도 모른다.",
        ),
        "벽면": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="원래 무슨 색이었는지 짐작조차 가지 않는다. 곳곳에 테이프 자국과 정체모를 얼룩이 추상화처럼 그려져 있다.",
        ),
        "봉인": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="부적으로 봉인한 게 아니다. 귀차니즘과 공포로 봉인된 것이다. 저걸 여는 순간 무슨 일이 벌어질지 아무도 책임지고 싶어 하지 않는다.",
        ),
        "주인": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이 짐들을 두고 떠난 선배는 과연 무사히 졸업했을까? 아니면 야반도주했을까? 전자이길 간절히 바랄 뿐이다.",
        ),
        "소리": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="'끼루룩... 위이잉...' 하드디스크가 비명을 지르고 있다. 제발 백업은 해뒀기를.",
        ),
        "정체": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="알려고 하지 마라. 화학식이 복잡할수록, 혹은 유통기한이 오래 지날수록 정신 건강에 해롭다. 그냥 '치워야 할 무언가'로 정의하는 편이 낫다.",
        ),
        "혼돈": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="엔트로피 증가 법칙을 눈으로 확인하고 싶다면 이곳이 최적의 장소다. 무질서가 지배하는 세상, 그게 바로 여기다.",
        ),
    },
    combinations=[
        Combination(
            targets=[KeywordId.BOX, KeywordId.CORP_CARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD),
                Condition(type=ConditionType.STATE_IS, target="box_opened", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[법인카드]**의 날카로운 모서리로 테이프를 찢었다. (한도 초과된 카드라 마음이 덜 아프다.)\n박스를 열자 지저분한 **[실험용 랩 가운]**이 나왔다!",
                ),
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.LAB_COAT),
                Action(type=ActionType.UPDATE_STATE, value={"key": "box_opened", "value": True}),
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
        Combination(
            type=CombinationType.PASSWORD,
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="computer_solved", value=False),
            ],
            targets=[KeywordId.COMPUTER, "136478"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "띠리링- 경쾌한음과 함께 잠금이 해제되었다!\n\n"
                        "바탕화면이 뜰 줄 알았는데, 켜놓고 끄지 않은 **[주문 내역]** 웹페이지가 바로 나타났다.\n\n"
                        "그리고 브라우저 창 바로 옆에, **`시약장_비번_주문수량_제발까먹지마.txt`** 라는 눈물겨운 이름의 파일이 보인다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "computer_solved", "value": True}),
                Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.ORDER_LIST),
                Action(type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.MEMO, "state": KeywordState.UNSEEN}),
            ],
        ),
        Combination(
            type=CombinationType.PASSWORD,
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="cabinet_unlocked", value=False),
            ],
            targets=[KeywordId.REAGENT_CABINET, "1029"],  # 킴와이프(1)-비커(0)-에탄올(2)-컵라면(9)
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자물쇠를 맞추자 '철컥' 소리와 함께 **[시약장]** 문이 열렸다.\n\n"
                        "라벨에 적힌 대로 물건들이 정렬되어... 있지는 않고 엉망진창이지만,\n\n"
                        "구석에서 굴러다니던 공업용 **[에탄올]** 병 하나는 건질 수 있었다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.ETHANOL,
                        "description": "순도 99% 공업용 에탄올. 마시면 실명, 뿌리면 소독. 명심하자.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "cabinet_unlocked", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.COMPUTER, "state": KeywordState.UNSEEN}
                ),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.ORDER_LIST, "state": KeywordState.UNSEEN}
                ),
            ],
        ),
        # [수정] 네거티브 피드백: 먼지 제거제(냉매)로 바닥(액체) 얼리기 시도
        Combination(
            targets=[KeywordId.AIR_DUSTER, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.AIR_DUSTER),
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[먼지 제거제]**를 뒤집어 액체 질소처럼 뿌려보았다.\n치익- 소리와 함께 액체가 하얗게 얼어붙었지만, 3초 뒤 다시 녹아 끈적해졌다.\n단순한 물리적 냉각으로는 해결되지 않는다. 화학적인 중화제가 필요하다.",
                )
            ],
        ),
        # [수정] 에탄올 + 바닥 -> 성공
        Combination(
            targets=[KeywordId.ETHANOL, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.ETHANOL),
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[에탄올]**을 들이붓자, 치이익 소리와 함께 끈적한 **의문의 액체**가 거품처럼 녹아내렸다!\n\n잠시 후, 바닥이 뽀득뽀득해졌다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ETHANOL),
                Action(type=ActionType.UPDATE_STATE, value={"key": "liquid_cleaned", "value": True}),
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
                    value="바닥의 끈적한 **의문의 액체** 때문에 **[빗자루]**가 쩍쩍 달라붙는다. 억지로 쓸다간 빗자루 털이 다 빠질 것 같다. 액체부터 없애야 한다.",
                )
            ],
        ),
        Combination(
            targets=[KeywordId.BROOM, KeywordId.FLOOR],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="liquid_cleaned", value=True),
                Condition(type=ConditionType.STATE_NOT, target="trash_step", value=3),
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
                Condition(type=ConditionType.STATE_IS, target="trash_step", value=3),
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
