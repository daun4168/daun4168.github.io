from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE2_3_DATA = SceneData(
    id=SceneID.CH1_SCENE2_3,
    name="선장실 선반",
    body=(
        "당신은 까치발을 들고 선반 위의 유리병들을 코앞에서 들여다봅니다.\n\n"
        "먼지 하나 없는 투명한 유리병 속에 정교하게 만들어진 배 모형들이 들어 있습니다.\n\n"
        '<img src="assets/chapter1/boats.png" alt="배" width="540">\n\n'
        "왼쪽부터 순서대로 **[붉은 용]**, **[하얀 백조]**, **[검은 유령]**, 그리고 **[황금 독수리]**입니다.\n\n"
        "선원 숙소에서 얻은 단서들을 조합해 진짜 배를 찾아내야 합니다.\n\n"
        "유리가 매우 두꺼워 보여서, 깨뜨리려면 무겁고 단단한 도구를 사용해야 합니다.\n\n"
        "뒤로 물러나면 다시 **[선장실]**로 돌아갑니다."
    ),
    initial_state={
        "room_inspected": False,
        "ship_red_broken": False,
        "ship_white_broken": False,
        "ship_black_broken": False,
        "ship_yellow_broken": False,
        "deck_key_found": False,
    },
    on_enter_actions=[],
    keywords={
        # 0. 나가기 (선장실로 복귀) - 확인 로직 적용
        KeywordId.CAPTAIN_ROOM: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                # 첫 번째 상호작용: 관찰
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="room_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="고개를 돌려보니 중후한 선장실의 풍경이 보입니다. 계속 까치발을 들고 있자니 종아리가 당겨옵니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "room_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                # 두 번째 상호작용: 이동 확인
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="room_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "선반에서 눈을 떼고 **[선장실]**로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="발뒤꿈치를 바닥에 붙이고 선반에서 물러납니다. 휴, 이제 좀 살 것 같네요.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE2_2),
                                ],
                                "cancel_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="아직 해결해야 할 퍼즐이 남았습니다. 다시 유리병을 노려봅니다.",
                                    ),
                                ],
                            },
                        ),
                    ],
                ),
            ],
        ),
        # 1. 붉은 용 (함정)
        KeywordId.SHIP_RED: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ship_red_broken", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="깨진 유리 조각과 붉은 돛 조각이 널려 있습니다. 매캐한 냄새가 납니다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[붉은 용]**\n"
                                "3개의 돛대를 가진 웅장한 배입니다. 핏빛처럼 붉은 돛을 달고 있으며, 돛에는 용이 그려져 있습니다.\n\n"
                                "배 밑바닥에 붉은 액체가 보입니다.\n\n"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 2. 하얀 백조 (정답)
        KeywordId.SHIP_WHITE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ship_white_broken", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="산산조각 난 유리 파편 속에 배 모형이 부서져 있습니다.",
                        )
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[하얀 백조]**\n"
                                "3개의 돛대를 가진 날렵한 배입니다. 순백색 돛을 달고 있으며, 선수상으로 여신상이 조각되어 있습니다.\n\n"
                                "레진 속에 이질적인 금속 광택이 비칩니다.\n\n"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 3. 검은 유령 (오답)
        KeywordId.SHIP_BLACK: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ship_black_broken", value=True)],
                    actions=[Action(type=ActionType.PRINT_NARRATIVE, value="검은 돛조각들만 흩날리고 있습니다.")],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[검은 유령]**\n"
                                "3개의 돛대를 가진 으스스한 배입니다. 찢어진 검은 돛과 해골 깃발이 특징입니다.\n\n"
                                "내부가 그을려 있어 잘 보이지 않습니다.\n\n"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # 4. 황금 독수리 (오답)
        KeywordId.SHIP_YELLOW: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ship_yellow_broken", value=True)],
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="금박이 벗겨진 초라한 배 모형이 굴러다닙니다.")
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "**[황금 독수리]**\n"
                                "1개의 돛대를 가진 작은 배입니다. 선수상으로 황금빛 독수리가 보입니다.\n\n"
                                "황금색 돛을 달았지만 자세히 보니 싸구려 금박입니다.\n\n"
                            ),
                        )
                    ]
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (배경/분위기) ---
        "까치발": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="종아리가 터질 것 같다. 선장은 키가 2미터쯤 됐나 보다. 루저의 비애가 느껴진다.",
        ),
        "먼지": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="눈을 씻고 찾아봐도 없다. 배가 가라앉는 와중에도 이것만 닦고 있었던 게 분명하다. 광기가 느껴진다.",
        ),
        "유리병": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="볼록렌즈처럼 내 얼굴을 흉측하게 비춘다. 며칠 못 씻어서 꼬질꼬질한 게 영락없는 조난자 꼴이다.",
        ),
        "배 모형": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="침몰한 배 안에서 배 모형을 구경하고 있다니. 상황이 참 아이러니하다. 일종의 블랙 코미디인가?",
        ),
        "코르크": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="입구가 꽉 막혀 있다. 마치 졸업이 보이지 않는 내 대학원 생활을 보는 것 같아 가슴이 답답하다.",
        ),
        "라벨": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="흘림체로 멋지게 쓰여 있다. 악필인 항해 일지와 딴판이다. 역시 사람은 자기가 좋아하는 걸 할 때만 정성을 쏟나 보다.",
        ),
        "레진": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="병 바닥에 굳어버린 가짜 파도다. 아이러니하게도 이 난파선에서 나를 익사시키지 않을 유일한 '안전한 바다'다.",
        ),
        "두께": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="어항 유리보다 훨씬 두껍다. 이 정도면 방탄 유리 아닌가? 고작 장난감 보호하는 데 목숨을 걸었다.",
        ),
        "본드 자국": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="자세히 보니 접착제 자국이 미세하게 보인다. 완벽해 보였는데 인간미가 느껴진다. 내 논문에서 오타를 찾은 기분이다.",
        ),
        "공기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="병 안은 멸균 상태일까? 저 안에 갇힌 선원 모형들은 숨이 막히겠지. 졸업이 막힌 내 처지와 다를 게 없다.",
        ),
        "코앞": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="초근접 접사 촬영 모드다. 내 시력이 2.0은 아니지만, 먼지 한 톨 없는 건 확실히 알겠다.",
        ),
        "도구": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="가방에 든 스패너가 무겁게 느껴진다. 교수님이 '도구는 손의 연장'이라고 하셨는데, 지금은 '파괴의 연장'이 될 것 같다.",
        ),
        "뒤": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="돌아갈 곳이 있다는 건 안도감을 주지만, 빈손으로 돌아가는 건 패배감을 준다. 뭐라도 건져야 한다.",
        ),
        "배 밑바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="붉은 액체가 찰랑거린다. 피일까? 와인일까? 아니면 그냥 색소 탄 물일까? 굳이 찍어 먹어보고 싶진 않다.",
        ),
        "금속 광택": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="인공적인 빛 반사다. 자연에서는 볼 수 없는 날카로운 빛. 저게 내가 찾는 열쇠이길 간절히 바란다.",
        ),
        "해골": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="전형적인 해적 깃발이다. '나 위험해요'라고 광고하는 꼴이다. 오히려 너무 뻔해서 함정 같기도 하다.",
        ),
        "금박": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="손톱으로 긁으면 벗겨질 것 같은 싸구려다. 겉만 번지르르한 게 딱 내 졸업 논문 초안 같다.",
        ),
        "정교": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="장인의 손길이 느껴진다. 이 배를 만든 사람은 분명 대학원생이었을 것이다. 그렇지 않고서야 이런 디테일에 집착할 리가 없다.",
        ),
    },
    combinations=[
        # ==========================================================
        # 1. 하얀 백조 (정답) + 스패너
        # ==========================================================
        Combination(
            targets=[KeywordId.SHIP_WHITE, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_1),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_3),
                Condition(type=ConditionType.STATE_IS, target="ship_white_broken", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "모든 단서가 이 배를 가리키고 있습니다. 당신은 망설임 없이 스패너를 휘둘렀습니다.\n\n"
                        "**와장창!**\n\n"
                        "유리병이 박살 나고, 깨진 바다 모형 속에서 녹슨 **[갑판 열쇠]**가 튀어나왔습니다! 정답입니다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.DECK_KEY,
                        "description": (
                            '<img src="assets/chapter1/3817_key.png" alt="갑판 열쇠" width="540">\n\n'
                            "갑판 뒷편으로 가는 녹슨 열쇠. 모양이 신기하다."
                        ),
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "ship_white_broken", "value": True}),
                Action(type=ActionType.UPDATE_STATE, value={"key": "deck_key_found", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.NOTE_1),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.NOTE_2),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.NOTE_3),
            ],
        ),
        # (단서 부족 시)
        Combination(
            targets=[KeywordId.SHIP_WHITE, KeywordId.SPANNER],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너를 들었지만 손이 떨립니다. 아직 어떤 배가 진짜인지 확신할 수 없습니다.\n\n"
                        "선원 숙소에서 쪽지를 모두 모아 알리바이를 확인한 뒤에 시도하십시오."
                    ),
                )
            ],
        ),
        # ==========================================================
        # 2. 붉은 용 (함정) + 스패너 -> 체력 -8
        # ==========================================================
        Combination(
            targets=[KeywordId.SHIP_RED, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_1),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_3),
                Condition(type=ConditionType.STATE_IS, target="ship_red_broken", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "확신을 가지고 스패너를 내리쳤습니다.\n\n"
                        "**콰광!**\n\n"
                        "병이 깨지자마자 내부에 압축되어 있던 붉은 가루가 폭발했습니다!\n\n"
                        "엄청난 충격과 함께 온몸이 불타는 듯한 고통이 밀려옵니다. 치명상입니다!\n\n"
                    ),
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-8),
                Action(type=ActionType.UPDATE_STATE, value={"key": "ship_red_broken", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.SHIP_RED, KeywordId.SPANNER],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="아직 단서가 부족합니다. 무고한 배를 깼다간 돌이킬 수 없습니다.",
                )
            ],
        ),
        # ==========================================================
        # 3. 검은 유령 (오답) + 스패너 -> 체력 -5
        # ==========================================================
        Combination(
            targets=[KeywordId.SHIP_BLACK, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_1),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_3),
                Condition(type=ConditionType.STATE_IS, target="ship_black_broken", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**챙그랑!**\n\n"
                        "병을 깨뜨리는 순간, 날카로운 유리 파편이 얼굴과 팔로 튀었습니다!\n\n"
                        "빈 껍데기뿐인 가짜였습니다. 피가 흐릅니다."
                    ),
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-5),
                Action(type=ActionType.UPDATE_STATE, value={"key": "ship_black_broken", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.SHIP_BLACK, KeywordId.SPANNER],
            actions=[Action(type=ActionType.PRINT_NARRATIVE, value="아직 단서가 부족합니다. 쪽지들을 더 찾아보세요.")],
        ),
        # ==========================================================
        # 4. 황금 독수리 (오답) + 스패너 -> 체력 -7
        # ==========================================================
        Combination(
            targets=[KeywordId.SHIP_YELLOW, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_1),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_2),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NOTE_3),
                Condition(type=ConditionType.STATE_IS, target="ship_yellow_broken", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "**퍽!**\n\n"
                        "병이 깨지자 황금 도료 가루가 폐 속 깊숙이 들어왔습니다.\n\n"
                        "쿨럭! 켁! 숨을 쉴 수가 없습니다. 유독성 가루입니다!"
                    ),
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=-7),
                Action(type=ActionType.UPDATE_STATE, value={"key": "ship_yellow_broken", "value": True}),
            ],
        ),
        Combination(
            targets=[KeywordId.SHIP_YELLOW, KeywordId.SPANNER],
            actions=[Action(type=ActionType.PRINT_NARRATIVE, value="아직 단서가 부족합니다. 신중해야 합니다.")],
        ),
    ],
)
