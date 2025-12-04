from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE4_0_DATA = SceneData(
    id=SceneID.CH1_SCENE4_0,
    name="정글 입구",
    body=(
        '"여긴 습도가 장난이 아니네... 찜질방 수준이야."\n\n'
        "울창한 숲을 지나자 끈적한 습기가 느껴지는 정글 입구가 나타났습니다.\n\n"
        "앞에는 늪지대가 흐르고 있는데, 물살이 빠르고 깊어 보여서 그냥은 건널 수 없습니다.\n"
        "설상가상으로 늪지대 한가운데에 악어 한 마리가 입을 쩍 벌리고 길을 막고 있습니다.\n\n"
        "주변에는 특이하게 생긴 Y자 나무가 서 있고, 그 아래에는 불개미집이 보입니다."
    ),
    initial_state={
        "slingshot_base_made": False,  # 새총틀 제작 여부
        "crocodile_gone": False,  # 악어 퇴치 여부
        "bridge_built": False,  # 다리 건설 여부
        "swamp_inspected": False,  # 늪지대 조사 여부
        "forest_path_inspected": False,  # 돌아가는 길 조사 여부
        "ant_collected": False,  # 개미 채집 여부
        "ant_touch_count": 0,  # 불개미집 터치 횟수 (0: 경고, 1이상: 데미지)
    },
    on_enter_actions=[],
    keywords={
        KeywordId.TREE: KeywordData(type=KeywordType.ALIAS, target=KeywordId.Y_TREE),
        # =================================================================
        # 1. 포탈 및 이동
        # =================================================================
        # 되돌아가기 (생태 관측소)
        KeywordId.ECO_OBSERVATORY: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="forest_path_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="뒤를 돌아보니 관측소 쪽으로 이어지는 숲길이 보입니다.",
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "forest_path_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="forest_path_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "정글을 빠져나와 **[생태 관측소]** 쪽으로 돌아가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value="축축한 정글을 벗어나 관측소로 돌아갑니다.",
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_0),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 해결해야 할 문제가 있습니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 전진 (늪지대 건너기) -> 동굴로 진입
        KeywordId.SWAMP_RIVER: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                # 다리 없음 + 악어 있음
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
                        Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=False),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/swampland_0.png" alt="늪지대" width="540">\n\n'
                                "검은 물이 흐르는 늪지대입니다. 깊이를 알 수 없습니다.\n\n"
                                "건너편으로 가야 하는데 악어가 눈을 번뜩이며 지키고 있어 물가에 다가갈 수도 없습니다.\n\n"
                                "먼저 악어부터 어떻게 처리해야 합니다."
                            ),
                        ),
                    ],
                ),
                # 다리 없음 + 악어 없음
                Interaction(
                    conditions=[
                        Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
                        Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=True),
                    ],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/swampland_2.png" alt="늪지대" width="540">\n\n'
                                "악어가 사라져서 물가까지 갈 수 있습니다.\n\n"
                                "하지만 강폭이 꽤 넓고 물살이 있어 수영해서 건너기는 위험해 보입니다.\n\n"
                                "다리를 만들어야 건널 수 있을 것 같습니다."
                            ),
                        ),
                    ],
                ),
                # 다리 있음 (건너기 가능)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="bridge_built", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "러버덕 다리를 밟고 늪지대를 건너 **[동굴]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE,
                                        value=(
                                            "러버덕 다리를 조심스럽게 밟고 지나갑니다.\n\n"
                                            "**삑- 삑- 삑-**\n\n"
                                            "걸을 때마다 노란 오리들의 비명 소리가 늪지대에 울려 퍼집니다.\n"
                                            "시끄럽지만 안전하게 늪을 건너, 어두운 동굴 안으로 들어갑니다."
                                        ),
                                    ),
                                    # CH1_SCENE5 (죽음의 늪/동굴)로 이동
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE5_0),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 준비가 덜 되었습니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # =================================================================
        # 2. 오브젝트
        # =================================================================
        # Y자 나무 (새총 베이스)
        KeywordId.Y_TREE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="slingshot_base_made", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/tree_y_1.png" alt="나무" width="540">\n\n'
                                "Y자 나무 가지에 덩굴 줄기가 팽팽하게 묶여 있습니다.\n\n"
                                "거대한 새총이 완성되어 있습니다. 강력한 탄환만 있다면 무엇이든 날려버릴 수 있을 겁니다."
                            ),
                        ),
                    ],
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="slingshot_base_made", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/tree_y_0.png" alt="나무" width="540">\n\n'
                                "가지가 Y자 모양으로 튼튼하게 뻗은 나무입니다.\n\n"
                                "양쪽 가지에 탄력 있는 줄을 매달면 뭔가 쏘아 보낼 수 있을 것 같이 생겼습니다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # 불개미집 (데미지 기믹 추가)
        KeywordId.FIRE_ANT_HILL: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 채집 완료 상태 (이 경우는 아래 Combination 액션으로 UNSEEN 처리되므로 여기 올 일은 거의 없음)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ant_collected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='<img src="assets/chapter1/ants2.png" alt="불개미집" width="540">\n\n'
                            "개미집이 파헤쳐져 있습니다.",
                        ),
                    ],
                ),
                # 1단계: 경고 (첫 터치)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ant_touch_count", value=0)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/ants.png" alt="불개미집" width="540">\n\n'
                                "붉은 흙이 솟아오른 개미집입니다. 사나운 **불개미**들이 우글거립니다.\n\n"
                                "저기에 물리면 엄청나게 아플 겁니다. 맨손으로는 건드리지 않는 게 좋겠습니다.\n\n"
                                "개미들을 담을만한 오목한 그릇 같은 게 있다면 퍼갈 수 있을지도 모릅니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "ant_touch_count", "value": 1}),
                    ],
                ),
                # 2단계: 데미지 (두 번째 이상 터치)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="ant_touch_count", value=1)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "앗 따거!!\n\n"
                                "호기심을 못 참고 손을 댔다가 불개미에게 물렸습니다.\n\n"
                                "살점이 떨어져 나갈 듯이 아픕니다."
                            ),
                        ),
                        Action(type=ActionType.MODIFY_STAMINA, value=-2),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value="[경고] 체력이 2 감소했습니다. 맨손으로 건드리지 마세요.",
                        ),
                    ],
                ),
            ],
        ),
        # 악어 (장애물)
        KeywordId.CROCODILE: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/crocodile.png" alt="나무" width="540">\n\n'
                                "집채만한 악어가 늪지대 길목을 떡하니 막고 있습니다.\n\n"
                                "가죽이 바위처럼 단단해 보여서 때려도 소용없을 것 같습니다.\n\n"
                                "녀석이 싫어할 만한 강력한 한 방을 먹여서 쫓아내야 합니다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (정글 입구) ---
        "습도": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="공기 중 수증기 포화도가 99%는 되는 것 같다. 아가미가 있다면 물 밖에서도 호흡할 수 있을 수준이다.",
        ),
        "찜질방": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="공짜 불가마 사우나다. 식혜와 맥반석 계란 대신, 내 살을 노리는 악어와 불개미가 있다는 점만 빼면 완벽하다.",
        ),
        "습기": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="끈적하다. 피부에 달라붙어 불쾌지수를 한계까지 끌어올린다.",
        ),
        "물살": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="빠르고 깊어 보인다. 맨몸으로 뛰어드는 건 자살 행위나 다름없다.",
        ),
        "입": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="악어가 쩍 벌리고 있는 입이다. 저건 생물학적 턱이라기보단, 유압 프레스기처럼 보인다.",
        ),
        "길": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="악어 한 마리가 막고 있다. 물리적으로 통과가 불가능해 보인다.",
        ),
    },
    # =================================================================
    # 3. 조합 (퍼즐 해결)
    # =================================================================
    combinations=[
        # 1. 새총 만들기: Y자 나무 + 덩굴 줄기
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.VINE_STEM],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/tree_y_1.png" alt="나무" width="540">\n\n'
                        "질긴 덩굴 줄기를 Y자 나무 양쪽 가지에 단단히 묶었습니다.\n\n"
                        "탄력이 훌륭합니다. 거대한 새총이 완성되었습니다!"
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "slingshot_base_made", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINE_STEM),
            ],
        ),
        # 2. 개미 채집: 코코넛 껍질 + 불개미집
        # 채집 후 불개미집은 UNSEEN 처리
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.FIRE_ANT_HILL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
                Condition(type=ConditionType.STATE_IS, target="ant_collected", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/ants2.png" alt="불개미집" width="540">\n\n'
                        "코코넛 껍질을 이용해 불개미들을 한가득 퍼담았습니다.\n\n"
                        "개미들이 껍질 안에서 바글거립니다. 쏟아지기 전에 입구를 막아야 합니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "ant_collected", "value": True}),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT_SHELL),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL_WITH_ANTS,
                        "description": '<img src="assets/chapter1/coconut_ant.png" alt="코코넛" width="540">\n\n'
                        "불개미가 가득 든 코코넛 껍질. 위험하다.",
                    },
                ),
                # 불개미집 UNSEEN 처리
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.FIRE_ANT_HILL, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # 3. 개미 폭탄 제조: 개미 든 껍질 + 청테이프
        Combination(
            targets=[KeywordId.COCONUT_SHELL_WITH_ANTS, KeywordId.DUCT_TAPE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL_WITH_ANTS),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DUCT_TAPE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "청테이프로 코코넛 껍질 입구를 칭칭 감아 밀봉했습니다.\n"
                        "안에서 개미들이 나가려고 발버둥 치는 소리가 들립니다.\n"
                        "강력한 **[개미 폭탄]**이 완성되었습니다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT_SHELL_WITH_ANTS),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.DUCT_TAPE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SEALED_ANT_BOMB,
                        "description": '<img src="assets/chapter1/coconut_bomb.png" alt="코코넛" width="540">\n\n'
                        "청테이프로 밀봉된 불개미 폭탄. 던지면 터지면서 개미들이 쏟아져 나올 것이다.",
                    },
                ),
            ],
        ),
        # 4. 악어 퇴치: 새총(Y자 나무) + 개미 폭탄
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.SEALED_ANT_BOMB],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="slingshot_base_made", value=True),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SEALED_ANT_BOMB),
                Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "개미 폭탄을 덩굴 줄기에 걸고, 있는 힘껏 당겼다가 놓았습니다.\n\n"
                        "**휘이익- 퍽!**\n\n"
                        '<img src="assets/chapter1/swampland_1.png" alt="늪지대" width="540">\n\n'
                        "폭탄이 악어의 등판에 정확히 명중했습니다! 껍질이 깨지며 성난 불개미 떼가 악어의 눈과 콧구멍으로 쏟아집니다.\n"
                        "악어는 고통스러워하며 물보라를 일으키더니, 늪지대 깊은 곳으로 도망쳤습니다."
                    ),
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "crocodile_gone", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.CROCODILE, "state": KeywordState.INACTIVE}
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SEALED_ANT_BOMB),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={"keyword": KeywordId.Y_TREE, "state": KeywordState.UNSEEN},
                ),
            ],
        ),
        # 5. 다리 재료 준비: 러버덕 + 그물망
        Combination(
            targets=[KeywordId.RUBBER_DUCK, KeywordId.NET],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NET),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "그물망 안에 커다란 러버덕 인형을 넣고 단단히 묶었습니다.\n"
                        "물에 둥둥 뜨는 훌륭한 **[러버덕 뭉치]**가 되었습니다. 밟을 때마다 소리가 날 것 같습니다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUBBER_DUCK),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.NET),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.RUBBER_DUCK_BRIDGE,
                        "description": '<img src="assets/chapter1/rubber_duck_bridge.png" alt="러버덕" width="540">\n\n'
                        "그물로 묶은 러버덕 뭉치.",
                    },
                ),
            ],
        ),
        # 6. 다리 건설: 러버덕 다리 + 늪지대
        Combination(
            targets=[KeywordId.SWAMP_RIVER, KeywordId.RUBBER_DUCK_BRIDGE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK_BRIDGE),
                Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=True),
                Condition(type=ConditionType.STATE_IS, target="bridge_built", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/swampland_3.png" alt="늪지대" width="540">\n\n'
                        "러버덕 뭉치를 늪지대에 길게 띄웠습니다.\n"
                        "노란 오리들이 둥실둥실 떠오르며 건너편으로 갈 수 있는 길을 열어줍니다.\n"
                        "이제 늪을 건너 동굴로 갈 수 있습니다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUBBER_DUCK_BRIDGE),
                Action(type=ActionType.UPDATE_STATE, value={"key": "bridge_built", "value": True}),
            ],
        ),
        # 실패 케이스: 악어가 있을 때 다리 놓기
        Combination(
            targets=[KeywordId.SWAMP_RIVER, KeywordId.RUBBER_DUCK_BRIDGE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK_BRIDGE),
                Condition(type=ConditionType.STATE_IS, target="crocodile_gone", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="지금 다리를 놨다가는 저 악어가 장난감처럼 씹어먹을 겁니다. 먼저 악어를 쫓아내야 합니다.",
                ),
            ],
        ),
        # ... (기존 성공 조합들 뒤에 이어 붙이기)
        # =================================================================
        # Negative Feedback (실패 조합) - 필수 요청 사항
        # =================================================================
        # 1. Y자 나무 + 청테이프 (새총 줄 대신 테이프 사용 시도)
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.DUCT_TAPE],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DUCT_TAPE)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="청테이프를 나무에 감아봤자 끈적거리기만 할 뿐, 탄력이 없습니다.\n\n뭔가 쫙쫙 늘어나는 줄이 필요합니다.",
                ),
            ],
        ),
        # 2. 늪지대 + 러버덕 (그물 없이 그냥 러버덕만 띄우기)
        Combination(
            targets=[KeywordId.SWAMP_RIVER, KeywordId.RUBBER_DUCK],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="러버덕 하나를 물에 띄워봤습니다. 둥실둥실 잘 떠내려가는군요."
                    "\n\n하지만 저 자그마한 오리 하나 밟고 건너다간 늪에 빠질 게 뻔합니다."
                    "\n\n뭔가 덩어리로 묶어야 발판 역할을 할 수 있을 것 같습니다.",
                ),
            ],
        ),
        # 3. 악어 + 소방 도끼 (직접 공격)
        Combination(
            targets=[KeywordId.CROCODILE, KeywordId.FIRE_AXE],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="미친 짓입니다! 도끼를 휘두르려면 악어 코앞까지 가야 합니다.\n\n"
                    "녀석의 가죽은 도끼날이 튕겨 나갈 정도로 두꺼워 보이고, 무엇보다 제가 먼저 잡아먹힐 겁니다.\n\n"
                    "원거리에서 공격할 방법이 필요합니다.",
                ),
            ],
        ),
        # 4. Y자 나무 + 개미 든 코코넛 껍질 (밀봉하지 않고 발사 시도)
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.COCONUT_SHELL_WITH_ANTS],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="slingshot_base_made", value=True),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL_WITH_ANTS),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="지금 상태로 쏘면 원심력 때문에 불개미들이 제 머리 위로 쏟아질 겁니다!\n\n"
                    "자살 행위나 마찬가지입니다. 쏘기 전에 내용물이 쏟아지지 않게 밀봉해야 합니다.",
                ),
            ],
        ),
        # =================================================================
        # Negative Feedback (실패 조합) - 추가 제안
        # =================================================================
        # 5. 악어 + 청테이프 (입을 막으려는 시도)
        Combination(
            targets=[KeywordId.CROCODILE, KeywordId.DUCT_TAPE],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DUCT_TAPE)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="악어의 주둥이를 테이프로 감아버리면 좋겠지만, 영화를 너무 많이 보셨군요.\n\n"
                    "가까이 갔다간 테이프를 붙이기도 전에 손목이 날아갈 겁니다.",
                ),
            ],
        ),
        # 6. 악어 + 그물망 (포획 시도)
        Combination(
            targets=[KeywordId.CROCODILE, KeywordId.NET],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NET)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="이 얇은 그물망으로는 저 괴물을 잡을 수 없습니다.\n\n"
                    "던지는 순간 찢어발겨져서 쓰레기만 늘어날 겁니다.",
                ),
            ],
        ),
        # 7. 악어 + 러버덕 (시선 끌기 시도)
        Combination(
            targets=[KeywordId.CROCODILE, KeywordId.RUBBER_DUCK],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="러버덕을 던져 시선을 끌어볼까요?\n\n"
                    "(삑-)\n\n"
                    "악어가 쳐다보지도 않습니다. 녀석은 고기를 원하지, 고무를 원하는 게 아닙니다.",
                ),
            ],
        ),
        # 8. Y자 나무 + 소방 도끼 (나무 베기)
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.FIRE_AXE],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="이 나무는 가지의 각도가 아주 절묘합니다. 베어버리기엔 너무 아깝습니다.\n\n"
                    "뭔가 발사대를 만들기에 딱 좋은 형태입니다.",
                ),
            ],
        ),
        # 9. Y자 나무 + 텅 빈 코코넛 껍질 (빈 껍질 발사)
        Combination(
            targets=[KeywordId.Y_TREE, KeywordId.COCONUT_SHELL],
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="slingshot_base_made", value=True),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="빈 껍질을 쏴봤자 악어에게는 마사지 수준도 안 될 겁니다.\n\n"
                    "껍질 안에 치명적인 무언가를 채워서 쏘아 보내야 합니다.",
                ),
            ],
        ),
        # ... (이전 코드에 이어서 추가)
        # =================================================================
        # Negative Feedback (추가 아이디어 2탄)
        # =================================================================
        # 10. 개미 폭탄 + 늪지대/악어 (새총 없이 그냥 손으로 던지기)
        # 설명: 플레이어는 폭탄을 만들었으니 그냥 던지면 된다고 생각할 수 있습니다. 왜 새총이 필요한지 정당성을 부여해야 합니다.
        Combination(
            targets=[KeywordId.SEALED_ANT_BOMB, KeywordId.CROCODILE],  # 혹은 SWAMP_RIVER
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SEALED_ANT_BOMB)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="팔 힘으로 던지기엔 악어와의 거리가 너무 멉니다.\n\n"
                    "자칫하다가 폭탄이 악어 앞 물가에 퐁당 빠지면 아까운 기회만 날리게 됩니다.\n\n"
                    "확실하고 강력하게, 직선으로 꽂아 넣을 발사 장치가 필요합니다.",
                ),
            ],
        ),
        # 11. 그물망 + 불개미집 (채집 시도)
        # 설명: 코코넛 대신 그물로 퍼보려는 시도입니다.
        Combination(
            targets=[KeywordId.NET, KeywordId.FIRE_ANT_HILL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.NET),
                Condition(type=ConditionType.STATE_IS, target="ant_collected", value=False),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="그물망을 개미집에 덮어봤지만, 구멍이 너무 큽니다.\n\n"
                    "개미들이 그물코 사이로 숭숭 빠져나오고, 심지어 그물을 타고 손으로 기어오르려 합니다!\n\n"
                    "개미를 담으려면 구멍이 없는 단단한 용기가 필요합니다.",
                ),
            ],
        ),
        # 12. 소방 도끼 + 불개미집 (화풀이/파괴 시도)
        # 설명: 개미에게 물린 후 화가 나서 부수려는 행동입니다.
        Combination(
            targets=[KeywordId.FIRE_AXE, KeywordId.FIRE_ANT_HILL],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FIRE_AXE)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="도끼로 개미집을 내려쳤다간 안에 있던 수천 마리의 불개미가 폭발하듯 쏟아져 나올 겁니다.\n\n"
                    "온몸이 개미로 뒤덮이고 싶지 않다면 그만두는 게 좋습니다.",
                ),
            ],
        ),
        # 13. 덩굴 줄기 + 악어 (올가미/포박 시도)
        # 설명: 밧줄로 악어를 묶거나 당기려는 시도입니다.
        Combination(
            targets=[KeywordId.VINE_STEM, KeywordId.CROCODILE],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="덩굴로 올가미를 만들어 던져볼까요?\n\n"
                    "운 좋게 목에 건다고 해도, 제 힘으로는 저 거대한 파충류를 1센티미터도 끌어당길 수 없습니다.\n\n"
                    "오히려 제가 물속으로 끌려들어 갈 겁니다.",
                ),
            ],
        ),
        # 14. 러버덕 + 불개미집 (이상한 조합)
        # 설명: 오리 안에 개미를 넣으려 하거나 장난치는 경우입니다.
        Combination(
            targets=[KeywordId.RUBBER_DUCK, KeywordId.FIRE_ANT_HILL],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER_DUCK)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="러버덕을 개미집 근처에 뒀더니 개미들이 오리를 공격합니다.\n\n"
                    "다행히 고무라서 물리진 않지만, 오리 몸에 개미들이 달라붙어 털어내느라 고생했습니다.\n\n"
                    "별로 좋은 생각은 아닙니다.",
                ),
            ],
        ),
    ],
)
