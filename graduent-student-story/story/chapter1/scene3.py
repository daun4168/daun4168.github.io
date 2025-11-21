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
        "safe_opened": False,  # 금고 개방 여부
        "axe_obtained": False,  # 도끼 획득 여부
        "batteries_found": False,  # 건전지 파밍 여부
        "entrance_inspected": False,  # 입구 조사 여부
    },
    keywords={
        # --- [Alias 정의] ---
        KeywordId.ACID_PUDDLE_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.ACID_PUDDLE),
        KeywordId.WHITE_POWDER_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.WHITE_POWDER),
        KeywordId.SAFE_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SAFE),
        KeywordId.RUSTY_CLAMP_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.RUSTY_CLAMP),
        KeywordId.MEMO: KeywordData(type=KeywordType.ALIAS, target=KeywordId.MEMO_VOLTAGE),
        KeywordId.SCATTERED_SUPPLIES_ALIAS: KeywordData(type=KeywordType.ALIAS, target=KeywordId.SCATTERED_SUPPLIES),

        # --- [돌아가는 길] ---
        KeywordId.SHIPWRECK_ENTRANCE: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="entrance_inspected", value=False)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="들어왔던 입구다. 밖으로 나가면 난파선 통로로 이어진다."),
                        Action(type=ActionType.PRINT_SYSTEM, value="다시 한번 **[난파선 입구]**를 입력하면 이동합니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "entrance_inspected", "value": True})
                    ]
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="entrance_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": ("**[난파선 입구]**로 나가시겠습니까?"),
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="화물칸을 빠져나와 통로로 돌아갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2),  # 통로로 이동
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 할 일이 남았습니다."),
                                ],
                            },
                        ),
                    ]
                )
            ]
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
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="가성소다로 중화되어 안전한 소금물이 되었습니다. 밟고 지나갈 수 있습니다.")]
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="접근 불가. 강산성 용액입니다. 함부로 건널 수 없습니다."),
                        Action(type=ActionType.PRINT_SYSTEM, value="적절한 용기로 용액을 뜨거나, 중화제를 뿌려야 합니다.")
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

        # 3. 작업대
        KeywordId.WORKBENCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="각종 공구가 있던 책상입니다. 고정된 **[멀티미터]**와 기름에 찌든 **[정비 메모]**가 보입니다.",
        ),

        # 4. 멀티미터
        KeywordId.MULTIMETER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="작동하는 아날로그 멀티미터입니다. 리드봉을 건전지에 대면 전압을 측정할 수 있습니다.",
        ),

        # 5. 전자 금고
        KeywordId.SAFE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="safe_opened", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="금고가 열려 있습니다.")]
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE,
                               value="전원이 꺼져 있는 금고입니다. 전원 케이블 끝에 **[배터리 케이스]**를 연결해야 할 것 같습니다."),
                    ]
                )
            ]
        ),

        # 6. 녹슨 클램프
        KeywordId.RUSTY_CLAMP: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="**[소방 도끼]**를 꽉 물고 있는 고정 장치입니다. 붉은 녹이 슬어 꿈쩍도 안 합니다.\n화학적으로 녹을 제거해야 합니다. 산성 용액이 좋겠지만, 그냥 부으면 흘러내릴 겁니다.",
        ),

        # 7. 정비 메모
        KeywordId.MEMO_VOLTAGE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description=(
                "\"경고: 정격 전압 **19V**를 엄수할 것.\n"
                "회로 보호를 위해 전압은 반드시 **높은 곳에서 낮은 곳으로(High -> Low)** 흐르도록 배열하시오.\n"
                "순서가 틀리거나 전압이 맞지 않으면 역전류로 인해 감전될 수 있음.\""
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
                        Action(type=ActionType.PRINT_NARRATIVE,
                               value="주변을 샅샅이 뒤졌습니다.\n상자들 사이에서 **[전분 가루]**, **[건전지]** 5개, **[배터리 케이스]**를 찾아냈습니다.",
                               ),

                        # 아이템 획득
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.STARCH, "description": "요리용 전분 가루. 액체를 걸쭉하게 만든다."}),
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_CASE,
                                                                "description": "3구 직렬 배터리 홀더. `배터리 케이스 : 123` 처럼 번호를 입력해 조립한다."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_1, "description": "전압을 알 수 없는 낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_2, "description": "전압을 알 수 없는 낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_3, "description": "전압을 알 수 없는 낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_4, "description": "전압을 알 수 없는 낡은 건전지."}),
                        Action(type=ActionType.ADD_ITEM,
                               value={"name": KeywordId.BATTERY_5, "description": "전압을 알 수 없는 낡은 건전지."}),

                        # 상태 업데이트
                        Action(type=ActionType.UPDATE_STATE, value={"key": "batteries_found", "value": True}),
                    ]
                ),
                Interaction(actions=[Action(type=ActionType.PRINT_NARRATIVE, value="더 이상 쓸만한 건 없습니다.")])
            ]
        ),
    },

    combinations=[
        # --- [퍼즐 1] 용기 선택 및 중화 ---

        # 1-1. 페트병 + 하얀 가루 (실패)
        Combination(
            targets=[KeywordId.EMPTY_BOTTLE, KeywordId.WHITE_POWDER],
            actions=[Action(type=ActionType.PRINT_NARRATIVE,
                            value="페트병 입구가 너무 좁습니다. 가루를 담으려다 다 흘릴 것 같습니다. 입구가 넓은 용기가 필요합니다.")]
        ),
        # 1-2. 양동이 + 하얀 가루 (성공)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.WHITE_POWDER],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="양동이로 하얀 가루(가성소다)를 듬뿍 퍼담았습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUSTY_BUCKET),
                Action(type=ActionType.ADD_ITEM,
                       value={"name": KeywordId.CAUSTIC_SODA_BUCKET, "description": "가성소다가 가득 담긴 양동이."}),
            ]
        ),

        # 1-3. 양동이 + 산성 웅덩이 (실패 - 부상)
        Combination(
            targets=[KeywordId.RUSTY_BUCKET, KeywordId.ACID_PUDDLE],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="으악! 양동이가 너무 커서 액체가 출렁거렸습니다. 손등에 산성 용액이 튀었습니다!"),
                Action(type=ActionType.MODIFY_STAMINA, value=-1),  # 체력 감소
                Action(type=ActionType.PRINT_SYSTEM, value="화상을 입었습니다. 좀 더 다루기 쉬운 작은 용기가 필요합니다.")
            ]
        ),
        # 1-4. 페트병 + 산성 웅덩이 (성공 - 샘플 채취)
        Combination(
            targets=[KeywordId.EMPTY_BOTTLE, KeywordId.ACID_PUDDLE],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="페트병을 조심스럽게 기울여 황산 용액을 채웠습니다. 뚜껑을 닫아 안전하게 확보했습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.EMPTY_BOTTLE),
                Action(type=ActionType.ADD_ITEM,
                       value={"name": KeywordId.ACID_BOTTLE, "description": "치명적인 황산이 담긴 페트병."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_collected", "value": True}),
            ]
        ),

        # [추가된 상호작용] 산성 웅덩이 + 전분 가루 (힌트)
        Combination(
            targets=[KeywordId.ACID_PUDDLE, KeywordId.STARCH],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="전분 가루를 웅덩이에 뿌려봤자 조금 걸쭉해질 뿐, 산성이 중화되지는 않습니다.\n강산성을 무력화시키려면 염기성 성분의 다른 가루가 필요합니다."
                )
            ]
        ),

        # 1-5. 중화 시도 (샘플 채취 전 - 차단)
        Combination(
            targets=[KeywordId.CAUSTIC_SODA_BUCKET, KeywordId.ACID_PUDDLE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=False)],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="잠깐, 이 웅덩이를 지금 다 중화시켜 버리면 나중에 산성 물질이 필요할 때 구할 곳이 없어집니다.\n어딘가에 샘플을 좀 떠둔 뒤에 붓는 게 좋겠습니다.")
            ]
        ),
        # 1-6. 중화 시도 (샘플 채취 후 - 성공)
        Combination(
            targets=[KeywordId.CAUSTIC_SODA_BUCKET, KeywordId.ACID_PUDDLE],
            conditions=[Condition(type=ConditionType.STATE_IS, target="acid_collected", value=True)],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="가성소다를 웅덩이에 들이부었습니다. 격렬한 반응 끝에 액체가 투명해졌습니다. 이제 안전하게 건너갈 수 있습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.CAUSTIC_SODA_BUCKET),
                Action(type=ActionType.UPDATE_STATE, value={"key": "acid_neutralized", "value": True}),
            ]
        ),

        # --- [퍼즐 2] 녹 제거 (화학 젤) ---

        # 2-1. 산성 젤 제조
        Combination(
            targets=[KeywordId.ACID_BOTTLE, KeywordId.STARCH],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="황산 용액에 전분 가루를 섞어 걸쭉하게 만들었습니다. **[산성 젤]**이 완성되었습니다. 이제 흘러내리지 않습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_BOTTLE),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STARCH),
                Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.ACID_GEL, "description": "끈적한 산성 반죽."}),
            ]
        ),
        # 2-2. 도끼 획득
        Combination(
            targets=[KeywordId.RUSTY_CLAMP, KeywordId.ACID_GEL],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="녹슨 클램프에 젤을 발랐습니다. 붉은 녹이 녹아내리며 장치가 풀렸습니다. **[소방 도끼]**를 획득했습니다!"),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.ACID_GEL),
                Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.FIRE_AXE, "description": "정글을 뚫을 수 있는 도구."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "axe_obtained", "value": True}),
            ]
        ),

        # --- [퍼즐 3] 배터리 전압 (멀티미터) ---
        # 1: 9V, 2: 6V, 3: 5V, 4: 4V, 5: 2V
        # 정답: 19V (9+6+4) -> ID 1, 2, 4
        # Action: UPDATE_KEYWORD_DATA로 이름(display_name)만 변경

        # 3-1. 측정 (속성 업데이트 로직)
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_1],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **9V**"),
                Action(type=ActionType.UPDATE_KEYWORD_DATA,
                       value={"keyword": KeywordId.BATTERY_1, "field": "display_name", "value": "건전지 1 (9V)"})
            ]
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_2],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **6V**"),
                Action(type=ActionType.UPDATE_KEYWORD_DATA,
                       value={"keyword": KeywordId.BATTERY_2, "field": "display_name", "value": "건전지 2 (6V)"})
            ]
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_3],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **5V**"),
                Action(type=ActionType.UPDATE_KEYWORD_DATA,
                       value={"keyword": KeywordId.BATTERY_3, "field": "display_name", "value": "건전지 3 (5V)"})
            ]
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_4],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **4V**"),
                Action(type=ActionType.UPDATE_KEYWORD_DATA,
                       value={"keyword": KeywordId.BATTERY_4, "field": "display_name", "value": "건전지 4 (4V)"})
            ]
        ),
        Combination(
            targets=[KeywordId.MULTIMETER, KeywordId.BATTERY_5],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="측정 결과: **2V**"),
                Action(type=ActionType.UPDATE_KEYWORD_DATA,
                       value={"keyword": KeywordId.BATTERY_5, "field": "display_name", "value": "건전지 5 (2V)"})
            ]
        ),

        # 3-2. 조립 (정답: 19V, 순서 9->6->4 / ID 1, 2, 4)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "124"],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="건전지를 순서대로(9V -> 6V -> 4V) 끼웠습니다.\n합계 19V. 완벽합니다! **[배터리 팩]**이 완성되었습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_CASE),
                # 건전지 아이템 소모 처리 (조립했으므로 제거)
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_1),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_2),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_4),
                Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.BATTERY_PACK, "description": "안정적인 19V 전원."}),
            ]
        ),

        # 3-3. 오답 (전압 틀림 예시: 9+6+5=20V -> ID 123)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "123"],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="지지직! 전압 합계가 20V입니다. 19V를 맞춰야 합니다. 스파크가 튀어 손을 데었습니다."),
                Action(type=ActionType.MODIFY_STAMINA, value=-1)
            ]
        ),
        # 3-4. 오답 (순서 틀림 예시: 4+6+9=19V -> ID 421)
        Combination(
            type=CombinationType.PASSWORD,
            targets=[KeywordId.BATTERY_CASE, "421"],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE,
                       value="퍽! 합계는 19V지만, 낮은 전압을 먼저 연결하자 역전류가 발생했습니다. '높은 곳에서 낮은 곳으로' 연결해야 합니다."),
                Action(type=ActionType.MODIFY_STAMINA, value=-1)
            ]
        ),

        # 3-5. 금고 개방
        Combination(
            targets=[KeywordId.SAFE, KeywordId.BATTERY_PACK],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="전원을 연결하자 금고가 열렸습니다. **[산업용 배터리]**를 확보했습니다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.BATTERY_PACK),
                Action(type=ActionType.ADD_ITEM,
                       value={"name": KeywordId.HEAVY_BATTERY, "description": "MK-II 수리용 부품."}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "safe_opened", "value": True}),
            ]
        ),
    ]
)