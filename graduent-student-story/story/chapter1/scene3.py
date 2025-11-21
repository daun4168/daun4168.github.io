from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE3_DATA = SceneData(
    id=SceneID.CH1_SCENE3,
    name="난파선 화물칸 (위험물 적재소)",
    initial_text=(
        "배가 기울어져 걷기 힘든 화물칸 내부입니다. 코를 찌르는 매캐한 화학 약품 냄새가 진동합니다.\n"
        "통로 중앙에는 터진 드럼통에서 흘러나온 치명적인 산성 웅덩이가 길을 막고 있습니다. "
        "건너편에는 작업대와 전자 금고, 그리고 벽에 고정된 소방 도끼가 보이지만 접근할 수 없습니다.\n\n"
        "발밑에는 터진 포대에서 나온 하얀 가루와 흩어진 보급품들이 널려 있습니다.\n"
        "뒤쪽에는 들어왔던 난파선 입구가 보입니다."
    ),
    initial_state={
        "acid_neutralized": False,  # 중화 여부
        "acid_collected": False,  # 샘플 채취 여부
        "safe_powered": False, # [신규] 금고 전원 상태
        "safe_opened": False,  # 금고 개방 여부
        "axe_obtained": False,  # 도끼 획득 여부
        "batteries_found": False,  # 건전지 파밍 여부
        "entrance_inspected": False,  # 입구 조사 여부
        "workbench_inspected": False,  # [신규] 작업대 조사 여부
    },
    keywords={
        # --- [Alias 정의] ---
        KeywordId.ACID_PUDDLE_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.ACID_PUDDLE),
        KeywordId.WHITE_POWDER_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WHITE_POWDER),
        KeywordId.SAFE_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SAFE),
        KeywordId.RUSTY_CLAMP_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.RUSTY_CLAMP),
        KeywordId.MEMO: KeywordData(type=KeywordType.ALIAS, target=KeywordId.MEMO_VOLTAGE),
        KeywordId.SCATTERED_SUPPLIES_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SCATTERED_SUPPLIES),
        KeywordId.NOTE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.PUZZLE_NOTE),
        # --- [돌아가는 길] ---
        KeywordId.SHIPWRECK_ENTRANCE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="entrance_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="들어왔던 입구다. 밖으로 나가면 난파선 통로로 이어진다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM, value="다시 한번 **[난파선 입구]**를 입력하면 이동합니다."
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "entrance_inspected", "value": True}),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="entrance_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "**[난파선 입구]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE, value="화물칸을 빠져나와 통로로 돌아갑니다."
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2),  # 통로로 이동
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 할 일이 남았습니다."),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # --- [환경 오브젝트 (모두 HIDDEN으로 시작)] ---
        # 1. 산성 웅덩이
        KeywordId.ACID_PUDDLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="황산이 흘러나와 만든 치명적인 웅덩이입니다. 밟으면 녹아내립니다. 염기성 물질로 중화시켜야 합니다.",
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="가성소다로 중화되어 안전한 소금물이 되었습니다. 밟고 지나갈 수 있습니다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="접근 불가. 강산성 용액입니다. 함부로 건널 수 없습니다.",
                        ),
                    ]
                ),
            ],
        ),
        # 2. 하얀 가루 (오브젝트)
        KeywordId.WHITE_POWDER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="터진 포대에 쌓인 하얀 가루입니다. 강한 염기성 냄새가 납니다. 가성소다(NaOH)인 것 같습니다.\n맨손으로 만지면 위험하니 담을 용기가 필요합니다.",
        ),
        # 3. 작업대 (접근 제한 및 멀티미터/메모 발견 로직 추가)
        KeywordId.WORKBENCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="각종 공구가 있던 책상입니다. 고정된 **[멀티미터]**와 기름에 찌든 **[정비 메모]**, 그리고 벽에 **[주기율표]**가 붙어 있습니다.",
            interactions=[
                # Case 1: 산성 웅덩이 미해결
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산성 웅덩이가 길을 막고 있어 작업대에 접근할 수 없습니다.",
                        )
                    ],
                ),
                # Case 2: 산성 웅덩이 해결 + 첫 방문 (멀티미터/메모/주기율표 발견)
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=True),
                        Condition(type=ConditionType.STATE_IS, target="workbench_inspected", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="작업대에 가까이 다가갔습니다. 고정된 계측기, 메모, 그리고 벽에 붙은 도표가 보입니다.",
                        ),
                        Action(type=ActionType.PRINT_SYSTEM, value="새로운 상호작용 대상이 여러 개 발견되었습니다."),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MULTIMETER, "state": KeywordState.DISCOVERED},
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.MEMO_VOLTAGE, "state": KeywordState.DISCOVERED},
                        ),
                        # [신규] 주기율표 발견
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.PERIODIC_TABLE, "state": KeywordState.DISCOVERED},
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "workbench_inspected", "value": True}),
                    ],
                ),
                # Case 3: 재방문
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="각종 공구가 있던 책상입니다. 멀티미터와 메모, 주기율표가 있습니다.",
                        )
                    ],
                ),
            ],
        ),
        # 4. 멀티미터 (초기 INACTIVE)
        KeywordId.MULTIMETER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="작동하는 아날로그 멀티미터입니다. 리드봉을 건전지에 대면 전압을 측정할 수 있습니다.",
        ),
        # 5. 전자 금고 (접근 제한 추가)
        KeywordId.SAFE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 산성 웅덩이 미해결 시 접근 불가
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산성 웅덩이가 길을 막고 있어 금고에 접근할 수 없습니다.",
                        )
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="금고가 열려 있습니다.")],
                ),
                # [신규] 전원 켜짐 상태 (쪽지 힌트 제공)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="전원이 켜져 있습니다. 비밀번호 입력 대기 중입니다. 문짝에 **[수수께끼 쪽지]**가 붙어 있습니다.",
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="`전자 금고 : [비밀번호]` 형태로 입력하세요.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.PUZZLE_NOTE, "state": KeywordState.DISCOVERED}),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="전원이 꺼져 있는 금고입니다. 전원 케이블 끝에 배터리를 연결해야 할 것 같습니다.",
                        ),
                    ]
                ),
            ],
        ),
        # 6. 소방 도끼 (오브젝트 - 벽에 붙어있는 상태)
        KeywordId.FIRE_AXE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="벽면에 단단히 고정된 붉은색 소방 도끼입니다.",
            interactions=[
                # 산성 웅덩이 미해결 시 접근 불가
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="acid_neutralized", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="치명적인 산성 웅덩이가 가로막고 있어 도끼에 접근할 수 없습니다. 먼저 웅덩이부터 치워야 합니다.",
                        )
                    ],
                ),
                # 웅덩이 해결 후 접근 -> 클램프 발견
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="도끼를 꺼내려 했지만, **[녹슨 클램프]**가 꽉 물고 있어 꿈쩍도 하지 않습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RUSTY_CLAMP, "state": KeywordState.DISCOVERED},
                        ),
                    ]
                ),
            ],
        ),
        # 7. 녹슨 클램프 (초기 HIDDEN -> 도끼 조사 시 발견)
        KeywordId.RUSTY_CLAMP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description="**[소방 도끼]**를 꽉 물고 있는 고정 장치입니다. 붉은 녹이 슬어 꿈쩍도 안 합니다.\n화학적으로 녹을 제거해야 합니다. 산성 용액이 좋겠지만, 그냥 부으면 흘러내릴 겁니다.",
        ),
        # 8. 정비 메모 (초기 INACTIVE)
        KeywordId.MEMO_VOLTAGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                '"경고: 정격 전압 **19V**를 엄수할 것.\n'
                "회로 보호를 위해 전압은 반드시 **높은 곳에서 낮은 곳으로(High -> Low)** 흐르도록 배열하시오.\n"
                '순서가 틀리거나 전압이 맞지 않으면 역전류로 인해 감전될 수 있음."'
            ),
        ),
        # [신규] 9. 수수께끼 쪽지 (금고 조사 시 발견)
        KeywordId.PUZZLE_NOTE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "\"가장 탐욕스러운 자들이 사랑하는 세 가지 금속이 이 안에 잠들어 있다.\n"
                "첫 번째는 녹슬지 않는 영원한 태양의 왕.\n"
                "두 번째는 늑대 인간을 죽이는 창백한 달의 눈물.\n"
                "세 번째는 전기를 가장 사랑하는 붉은 핏줄.\n"
                "그들의 **영혼의 번호(Atomic Number)**를 순서대로 나열하라.\""
            ),
        ),
        # [신규] 10. 주기율표 (작업대 조사 시 발견)
        KeywordId.PERIODIC_TABLE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            description=(
                "벽에 붙어 있던 주기율표 포스터입니다. 불에 타서 가장자리는 검게 그을렸지만, 중앙 부분은 아직 알아볼 수 있습니다.\n\n"
                "| 1 H 수소| 2 He 헬륨 | 3 Li 리튬 |\n"
                "| :---: | :---: | :---: |\n"
                "| 10 Ne 네온 | 11 Na 나트륨 | 12 Mg 마그네슘 |\n"
                "| 28 Ni 니켈 | 29 Cu 구리 | 30 Zn 아연 |\n"
                "| 46 Pd 팔라듐 | 47 Ag 은 | 48 Cd 카드뮴 |\n"
                "| 78 Pt 백금 | 79 Au 금 | 80 Hg 수은 |"
            )
        ),
        # --- [파밍 아이템] ---
        # 흩어진 보급품
        KeywordId.SCATTERED_SUPPLIES: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="batteries_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="주변을 샅샅이 뒤졌습니다.\n상자들 사이에서 **[전분 가루]**, **[건전지]** 5개, **[배터리 케이스]**를 찾아냈습니다.",
                        ),
                        # 아이템 획득
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.STARCH,
                                "description": "요리용 전분 가루. 액체를 걸쭉하게 만든다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={
                                "name": KeywordId.BATTERY_CASE,
                                "description": "3구 직렬 배터리 홀더. `배터리 케이스 : 123` 처럼 번호를 입력해 조립한다.",
                            },
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_1, "description": "전압을 알 수 없는 낡은 건전지."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_2, "description": "전압을 알 수 없는 낡은 건전지."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_3, "description": "전압을 알 수 없는 낡은 건전지."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_4, "description": "전압을 알 수 없는 낡은 건전지."},
                        ),
                        Action(
                            type=ActionType.ADD_ITEM,
                            value={"name": KeywordId.BATTERY_5, "description": "전압을 알 수 없는 낡은 건전지."},
                        ),
                        # 상태 업데이트
                        Action(type=ActionType.UPDATE_STATE, value={"key": "batteries_found", "value": True}),
                    ],
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="더 이상 쓸만한 건 없습니다.")]),
            ],
        ),
    },
    combinations=[
        # --- [퍼즐 1] 용기 선택 및 중화 ---
        # 1-1. 페트병 + 하얀 가루 (실패)
        Combination(
            targets=[KeywordId.EMPTY_BOTTLE, KeywordId.WHITE_POWDER],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="페트병 입구가 너무 좁습니다. 가루를 담으려다 다 흘릴 것 같습니다. 입구가 넓은 용기가 필요합니다.",
                )
            ],
        ),
        # 1-2. 양동이 + 하얀 가루 (성공)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.WHITE_POWDER],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="양동이로 하얀 가루(가성소다)를 듬뿍 퍼담았습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUSTY_BUCKET),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.CAUSTIC_SODA_BUCKET, "description": "가성소다가 가득 담긴 양동이."},
                ),
            ],
        ),
        # 1-3. 양동이 + 산성 웅덩이 (실패 - 부상)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.ACID_PUDDLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="으악! 양동이가 너무 커서 액체가 출렁거렸습니다. 손등에 산성 용액이 튀었습니다!",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),  # 체력 감소
                Action(
                    type=ActionType.PRINT_SYSTEM, value="화상을 입었습니다. 좀 더 다루기 쉬운 작은 용기가 필요합니다."
                ),
            ],
        ),
        # 1-4. 페트병 + 산성 웅덩이 (성공 - 샘플 채취)
        Combination(
            targets=[KeywordId.EMPTY_BOTTLE, KeywordId.ACID_PUDDLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="페트병을 조심스럽게 기울여 황산 용액을 채웠습니다. 뚜껑을 닫아 안전하게 확보했습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.EMPTY_BOTTLE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.ACID_BOTTLE, "description": "치명적인 황산이 담긴 페트병."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_collected", "value": True}),
            ],
        ),
        # [신규] 녹슨 클램프 + 산성 용액 (실패 & 부상)
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_BOTTLE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value='녹슨 클램프에 산성 용액을 그대로 부었습니다.\n예상대로 용액은 주르륵 흘러내려 바닥으로 떨어졌고, 그중 일부가 당신의 손등에 튀었습니다!\n\n"으악! 타는 것 같아!"',
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-5),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="[경고] 화상을 입어 체력이 감소했습니다. 용액이 흘러내리지 않게 점성을 높여야 합니다.",
                ),
            ],
        ),
        # [추가된 상호작용] 산성 웅덩이 + 전분 가루 (힌트)
        Combination(
            targets=[KeywordId.ACID_PUDDLE, KeywordId.STARCH],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="전분 가루를 웅덩이에 뿌려봤자 조금 걸쭉해질 뿐, 산성이 중화되지는 않습니다.\n강산성을 무력화시키려면 염기성 성분의 다른 가루가 필요합니다.",
                )
            ],
        ),
        # 1-5. 중화 시도 (샘플 채취 전 - 차단)
        Combination(
            targets=[KeywordId.CAUSTIC_SODA_BUCKET, KeywordId.ACID_PUDDLE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="잠깐, 이 웅덩이를 지금 다 중화시켜 버리면 나중에 산성 물질이 필요할 때 구할 곳이 없어집니다.\n어딘가에 샘플을 좀 떠둔 뒤에 붓는 게 좋겠습니다.",
                )
            ],
        ),
        # 1-6. 중화 시도 (샘플 채취 후 - 성공)
        Combination(
            targets=[KeywordId.CAUSTIC_SODA_BUCKET, KeywordId.ACID_PUDDLE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="가성소다를 웅덩이에 들이부었습니다. 격렬한 반응 끝에 액체가 투명해졌습니다. 이제 안전하게 건너갈 수 있습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CAUSTIC_SODA_BUCKET),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_neutralized", "value": True}),
            ],
        ),
        # --- [퍼즐 2] 녹 제거 (화학 젤) ---
        # 2-1. 산성 젤 제조
        Combination(
            targets=[KeywordId.ACID_BOTTLE, KeywordId.STARCH],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="황산 용액에 전분 가루를 섞어 걸쭉하게 만들었습니다. **[산성 젤]**이 완성되었습니다. 이제 흘러내리지 않습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_BOTTLE),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STARCH),
                Action(
                    type=ActionType.ADD_ITEM, value={"name": KeywordId.ACID_GEL, "description": "끈적한 산성 반죽."}
                ),
            ],
        ),
        # 2-2. 도끼 획득 (오브젝트 제거 -> 아이템 획득)
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_GEL],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="녹슨 클램프에 젤을 발랐습니다. 붉은 녹이 녹아내리며 장치가 풀렸습니다. 벽에 붙어있던 **[소방 도끼]**를 떼어냈습니다!",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_GEL),
                # [수정] 키워드(벽의 도끼) 먼저 제거
                Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.FIRE_AXE),
                # [수정] 아이템 획득
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.FIRE_AXE, "description": "정글을 뚫을 수 있는 도구."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "axe_obtained", "value": True}),
            ],
        ),
        # --- [퍼즐 3] 배터리 전압 (멀티미터) ---
        # 1: 9V, 2: 6V, 3: 5V, 4: 4V, 5: 2V
        # 정답: 19V (9+6+4) -> ID 1, 2, 4
        # Action: UPDATE_ITEM_DATA 이름(extra_name)만 변경
        # 3-1. 측정 (속성 업데이트 로직)
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_1],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **9V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_1, "field": "extra_name", "value": "(9V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_1, "field": "description", "value": "측정된 전압은 9V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_2],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **6V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_2, "field": "extra_name", "value": "(6V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_2, "field": "description", "value": "측정된 전압은 6V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_3],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **5V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_3, "field": "extra_name", "value": "(5V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_3, "field": "description", "value": "측정된 전압은 5V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_4],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **4V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_4, "field": "extra_name", "value": "(4V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_4, "field": "description", "value": "측정된 전압은 4V입니다."},
                ),
            ],
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_5],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **2V**"),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_5, "field": "extra_name", "value": "(2V)"},
                ),
                Action(
                    type=ActionType.UPDATE_ITEM_DATA,
                    value={"keyword": KeywordId.BATTERY_5, "field": "description", "value": "측정된 전압은 2V입니다."},
                ),
            ],
        ),
        # 3-2. 조립 (정답: 19V, 순서 9->6->4 / ID 1, 2, 4)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "124"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="건전지를 순서대로(9V -> 6V -> 4V) 끼웠습니다.\n합계 19V. 완벽합니다! **[배터리 팩]**이 완성되었습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_CASE),
                # 건전지 아이템 소모 처리 (조립했으므로 제거)
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_1),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_2),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_3),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_4),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_5),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.BATTERY_PACK, "description": "안정적인 19V 전원."},
                ),
            ],
        ),
        # 3-3. 오답 (전압 틀림 예시: 9+6+5=20V -> ID 123)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "123"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="지지직! 전압 합계가 20V입니다. 19V를 맞춰야 합니다. 스파크가 튀어 손을 데었습니다.",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),
            ],
        ),
        # 3-4. 오답 (순서 틀림 예시: 4+6+9=19V -> ID 421)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "421"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="퍽! 합계는 19V지만, 낮은 전압을 먼저 연결하자 역전류가 발생했습니다. '높은 곳에서 낮은 곳으로' 연결해야 합니다.",
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),
            ],
        ),
        # [신규] 빈 배터리 케이스 + 금고 (힌트)
        Combination(
            targets=[KeywordId.SAFE, KeywordId.BATTERY_CASE],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="빈 케이스만 연결해서는 작동하지 않습니다. 건전지를 채워 넣어야 합니다.",
                )
            ],
        ),
        # 3-5. 금고 전원 켜기
        Combination(
            targets=[KeywordId.SAFE, KeywordId.BATTERY_PACK],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="배터리 팩을 연결하자 '삑' 소리와 함께 금고의 LCD 화면이 켜졌습니다.\n비밀번호 입력 대기 상태입니다. 문짝에는 **[수수께끼 쪽지]**가 붙어 있습니다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_PACK),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_powered", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.PUZZLE_NOTE, "state": KeywordState.DISCOVERED},
                ),
            ],
        ),
        # [신규] 3-6. 금고 비밀번호 입력 (Au=79, Ag=47, Cu=29 -> 794729)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.SAFE, "794729"],
            conditions=[Condition(type=ConditionType.STATE_IS, target="safe_powered", value=True)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="*띠리릭- 철컥!*\n정답입니다. 금고 문이 열렸습니다. 안에서 묵직한 **[산업용 배터리]**를 발견했습니다!",
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={"name": KeywordId.HEAVY_BATTERY, "description": "MK-II를 위한 대용량 배터리."},
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_opened", "value": True}),
            ],
        ),
    ],
)