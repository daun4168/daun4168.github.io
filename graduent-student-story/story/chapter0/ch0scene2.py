from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH0_SCENE2_DATA = SceneData(
    id=SceneID.CH0_SCENE2,
    name="제 2 연구실 (청소 완료)",
    initial_text="---\n## 제 2 연구실 (청소 완료)\n---\n",
    body=(
        "청소를 마치자마자 교수님이 땀을 뻘뻘 흘리며 거대한 고철 덩어리를 낑낑대며 들고 들어왔습니다.\n\n"
        '"자, 이게 내 역작 양자 가마솥이야. 배송비를 아껴줄 초공간 양자 전송 장치지.\n\n'
        '해외 직구 배송비가 너무 비싸서 직접 만들었어."\n\n'
        "교수님은 전선을 대충 콘센트에 꽂더니 나를 쳐다봅니다. 가마솥 안에서 밥 끓는 듯한 불안한 웅웅 소리가 납니다.\n\n"
        '"테스트하게 저기 탑승구로 들어가. 자네 몸무게가 쌀 한 가마니랑 비슷하니까 딱이야."'
    ),
    initial_state={
        "professor_called_out": False,  # 교수가 카드를 달라고 소리쳤는지 여부
        "card_returned": False,  # 카드가 반납되었는지 여부
    },
    keywords={
        KeywordId.QUANTUM: KeywordData(type=KeywordType.ALIAS, target=KeywordId.QUANTUM_CAULDRON),
        KeywordId.CAULDRON: KeywordData(type=KeywordType.ALIAS, target=KeywordId.QUANTUM_CAULDRON),
        KeywordId.PROFESSOR: KeywordData(
            type=KeywordType.NPC,
            state=KeywordState.DISCOVERED,
            interactions=[
                # 1. 기본 상태
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="어서 들어가게. 아, **[탑승구]** 경첩이 좀 헐거우니까 자네가 알아서 좀 조이고.",
                        )
                    ],
                ),
                # 2. 카드를 아직 안 줬고, 교수가 달라고 소리친 상태
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
                        Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="내 말 안 들리나? **[법인카드]** 놓고 가라고! 그게 내 목숨보다 중요한 거야!",
                        )
                    ],
                ),
                # 3. 카드를 이미 반납한 상태
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="card_returned", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="뭘 꾸물거려? 어서 **[탑승구]**로 들어가! 뜸 들이면 폭발... 아니, 전력 낭비야!",
                        )
                    ],
                ),
            ],
        ),
        # 텍스트를 '양자 가마솥'으로 변경
        KeywordId.QUANTUM_CAULDRON: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="교수님의 역작 **[양자 가마솥]**이다. 겉보기엔 영락없는 무쇠 솥단지인데, 전선들이 문어발처럼 얽혀있다.\n\n"
                            "**[탑승구]** 쪽 경첩이 덜 조여진 것처럼 덜렁거린다.",
                        )
                    ]
                ),
            ],
        ),
        KeywordId.HATCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # [네거티브 피드백] 수리하지 않고 그냥 탑승하려고 할 때
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "그냥 들어가려니 뚜껑... 아니, 문이 덜렁거려서 닫히질 않는다. \n\n"
                                "이대로 가동했다간 압력밥솥 터지듯 날아갈 것이다. 무언가로 단단히 조여야 한다."
                            ),
                        )
                    ]
                )
            ],
            description="사람 하나가 웅크리고 들어갈 만한 좁은 입구다. 경첩이 헐거워서 손으로 만지면 덜그럭거린다. 꽉 조일만한 게 필요하다.",
        ),
        # --- 배경/분위기용 UNSEEN 오브젝트 (게임 플레이에 영향 없음) ---
        "고철 덩어리": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="교수님은 '역작'이라 부르고, 나는 '산업 폐기물'이라 부른다. 고물상에 팔면 랩실 회식비 정도는 나올 것 같다.",
        ),
        "콘센트": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="벽에 꽂힌 양자 가마솥의 콘센트다. 피복이 벗겨져 있어 보기만 해도 짜릿하다. 건드리면 졸업하기 전에 요단강을 건널 것 같다.",
        ),
        "전선": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="청테이프로 대충 감아놓은 전선이다. 교수님의 공학적 감각은 일반인의 상식을 아득히 뛰어넘는다.",
        ),
        "배송비": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="고작 몇만 원의 배송비를 아끼기 위해 수억 원의 연구비를 태웠다. 이것이 바로 교수님의 '창조 경제'다.",
        ),
        "해외 직구": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="교수님의 유일한 취미다. 연구실로 택배가 올 때마다 관세청에서 전화가 올까 봐 내 심장이 덜컥거린다.",
        ),
        "초공간 양자 전송 장치": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이름은 SF 블록버스터급인데, 생김새는 시골 장터 뻥튀기 기계다.",
        ),
        "몸무게": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="최근 스트레스로 살이 좀 빠졌는데, 쌀 한 가마니(80kg)라니. 교수님 눈에는 내가 '연구원'이 아니라 '짐짝'으로 보이는 게 분명하다.",
        ),
        "쌀 한 가마니": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="내 몸무게를 쌀 단위로 환산하다니. 21세기에 걸맞은 최첨단 도량형이다.",
        ),
        "땀": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="평소 숨쉬기 운동만 하던 교수님이 육수를 뽑아내고 있다. 저 땀방울 하나하나가 다 내가 벌어온 연구비로 만들어진 것일 텐데.",
        ),
        "역작": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="프랑켄슈타인 박사도 자신의 피조물을 그렇게 불렀을 것이다. 그 소설의 결말이 파멸이었던 건 기억 못 하시는 걸까.",
        ),
        "직접": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="'수제(Handmade)'라는 단어가 이렇게 공포스럽게 다가온 적은 없었다. 장인의 숨결 대신 어설픈 납땜 냄새만 진동한다.",
        ),
        "밥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="이름이 가마솥이라서 진짜 밥 짓는 소리가 나는 건가? 취사가 완료되면 나도 갓 지은 햅쌀밥처럼 고슬고슬해지는 건 아니겠지.",
        ),
        "테스트": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="말은 좋아서 테스트지, 실상은 '임상 실험' 혹은 '마루타'다. 생명윤리위원회 승인은 받고 하는 건지 의문이다.",
        ),
    },
    combinations=[
        # [수정] 스패너로 탑승구 수리 시도 (카드를 아직 안 줬을 때 -> 방해 이벤트 발생)
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**로 **[탑승구]**의 볼트를 조이려는 찰나, 교수님이 다급하게 소리친다.\n\n"
                        '"잠깐! 자네 주머니에 **[법인카드]**! 그거 놓고 타야지! 가지고 가면 횡령이야!"'
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "professor_called_out", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.QUANTUM_CAULDRON, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "본체(솥단지)를 함부로 두들겼다간 양자 얽힘이 국수 엉키듯 꼬일 것 같다. (사실 어디를 건드려야 할지 모르겠다.)\n\n"
                        "수리가 필요한 건 본체가 아니라 덜렁거리는 **[탑승구]**다."
                    ),
                )
            ],
        ),
        # [수정] 스패너로 탑승구 수리 시도 (카드 반납됨 -> 예/아니오 확인 후 이동)
        Combination(
            targets=[KeywordId.HATCH, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.REQUEST_CONFIRMATION,
                    value={
                        "prompt": "볼트를 조이면 **[양자 가마솥]**이 즉시 가동됩니다. 수리를 마치고 탑승하시겠습니까?",
                        "confirm_actions": [
                            Action(
                                type=ActionType.PRINT_NARRATIVE,
                                value=(
                                    "**[스패너]**로 **[탑승구]**를 단단히 조이자마자, 가마솥이 요란한 소리를 내며 진동하기 시작한다!\n\n"
                                    '"좋아! 취사... 아니, 가동 시작! 좌표는... 어... 대충 거기로 설정했어! 살아서 돌아오게!"\n\n'
                                    "시야가 하얗게 점멸하고, 엄청난 압력이 몸을 짓누른다. 의식이 희미해진다..."
                                ),
                            ),
                            Action(
                                type=ActionType.MOVE_SCENE,
                                value=SceneID.CH1_SCENE0,
                            ),
                        ],
                        "cancel_actions": [
                            Action(
                                type=ActionType.PRINT_NARRATIVE,
                                value="아직 마음의 준비가 되지 않았다. 이 거대한 압력밥솥에 들어가는 건 조금 더 고민해보자.",
                            ),
                        ],
                    },
                )
            ],
        ),
        # [수정] 교수님에게 법인카드 반납 (언제든지 가능하도록 조건 완화)
        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.CORP_CARD],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.CORP_CARD),
                Condition(type=ConditionType.STATE_IS, target="card_returned", value=False),
                Condition(type=ConditionType.STATE_IS, target="professor_called_out", value=True),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "교수님께 **[법인카드]**를 건네자, 교수님은 빛보다 빠른 속도로 카드를 낚아채 주머니에 넣는다.\n\n"
                        '"그래, 이건 연구실의 자산... 아니, 내 영혼과도 같은 거지."'
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CORP_CARD),
                Action(type=ActionType.UPDATE_STATE, value={"key": "card_returned", "value": True}),
                Action(type=ActionType.PRINT_SYSTEM, value="이제 방해 없이 **[탑승구]**를 수리할 수 있습니다."),
            ],
        ),
        # [네거티브 피드백] 스패너 + 교수님
        Combination(
            targets=[KeywordId.PROFESSOR, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**[스패너]**를 들어 올리자 교수님이 기겁하며 뒤로 물러선다.\n\n"
                        '"이보게! 대학원생의 분노는 이해하지만, 폭력은 안 돼! 졸업은 해야지!"'
                    ),
                )
            ],
        ),
    ],
)
