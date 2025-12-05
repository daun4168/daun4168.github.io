from const import ActionType, CombinationType, ConditionType, KeywordId, KeywordState, KeywordType, SceneID
from schemas import Action, Combination, Condition, Interaction, KeywordData, SceneData

CH1_SCENE3_1_DATA = SceneData(
    id=SceneID.CH1_SCENE3_1,
    name="연구동 중앙 복도",
    initial_text="---\n## 연구동 중앙 복도\n---\n\n",
    body=(
        '"먼지 쌓인 복도... 발자국 소리가 너무 크게 울려."\n\n'
        "연구소 내부 복도입니다. 벽을 따라 캐비닛들이 늘어서 있고, 각기 다른 방으로 향하는 문들이 보입니다.\n\n"
        "왼쪽에는 배양실로 가는 문, 오른쪽에는 자료실 문, 정면 끝에는 통제실 문이 있습니다.\n\n"
        "뒤쪽에는 부서진 나무 문이 덜렁거리고 있습니다.\n\n"
        "배양실 문 옆 벽면 아래쪽에는 덮개가 뜯겨 나간 배관 점검구가 보입니다."
    ),
    initial_state={
        "valve_found": False,
        "cabinets_inspected": False,  # 캐비닛 그룹 조사 여부
        "wooden_door_inspected": False,  # 나무 문 조사 여부
        "incubation_inspected": False,  # 배양실 문 조사 여부
        "reference_inspected": False,  # 자료실 문 조사 여부
        "control_inspected": False,  # 통제실 문 조사 여부
        "green_opened": False,
        "red_opened": False,
        "yellow_opened": False,
    },
    on_enter_actions=[],
    keywords={
        KeywordId.ACCESS_PANEL: KeywordData(type=KeywordType.ALIAS, target=KeywordId.PLUMBING_HATCH),
        KeywordId.INCUBATION_ROOM_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.INCUBATION_ROOM),
        KeywordId.REFERENCE_ROOM_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.REFERENCE_ROOM),
        KeywordId.CONTROL_ROOM_DOOR: KeywordData(type=KeywordType.ALIAS, target=KeywordId.CONTROL_ROOM),
        # =================================================================
        # 0. 포탈 (관찰 -> 이동 확인 패턴 적용)
        # =================================================================
        # 1) 외부로 나가기 (나무 문)
        KeywordId.WOODEN_DOOR: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wooden_door_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "도끼로 부숴버린 문짝이 흉물스럽게 매달려 있습니다.\n\n"
                                "틈새로 숲의 습한 공기가 들어옵니다. 밖은 여전히 고요합니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "wooden_door_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="wooden_door_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "너덜너덜해진 문을 지나 **[생태 관측소 외부]**로 나가시겠습니까?",
                                "confirm_actions": [
                                    Action(
                                        type=ActionType.PRINT_NARRATIVE, value="숲의 공기를 마시러 밖으로 나갑니다."
                                    ),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_0),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="아직 내부 조사가 끝나지 않았습니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 2) 배양실 이동
        KeywordId.INCUBATION_ROOM: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="incubation_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "문틈으로 서늘한 냉기가 흘러나와 발목을 스칩니다.\n\n"
                                "안에서 웅웅거리는 기계 소리가 희미하게 들립니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "incubation_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="incubation_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "냉기가 감도는 **[배양실]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="옷깃을 여미며 배양실로 들어갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_2),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="추운 건 질색입니다. 나중에 갑니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 3) 자료실 이동
        KeywordId.REFERENCE_ROOM: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="reference_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "반쯤 열린 문 사이로 오래된 종이 냄새와 잉크 냄새가 납니다.\n"
                                "책장이 빼곡하게 들어찬 것이 보입니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "reference_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="reference_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "책 냄새가 나는 **[자료실]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="자료실 안으로 들어갑니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_3),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="머리 아픈 글자는 나중에 읽겠습니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # 4) 통제실 이동
        KeywordId.CONTROL_ROOM: KeywordData(
            type=KeywordType.PORTAL,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="control_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "육중한 철문입니다. '관계자 외 출입 금지' 팻말이 붙어 있습니다.\n"
                                "문 너머로는 죽은 듯한 적막만 흐릅니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "control_inspected", "value": True}),
                    ],
                    continue_matching=True,
                ),
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="control_inspected", value=True)],
                    actions=[
                        Action(
                            type=ActionType.REQUEST_CONFIRMATION,
                            value={
                                "prompt": "가장 중요한 **[통제실]**로 들어가시겠습니까?",
                                "confirm_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="긴장감을 안고 통제실 문을 엽니다."),
                                    Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE3_4),
                                ],
                                "cancel_actions": [
                                    Action(type=ActionType.PRINT_NARRATIVE, value="마음의 준비가 필요합니다.")
                                ],
                            },
                        )
                    ],
                ),
            ],
        ),
        # =================================================================
        # 1. 오브젝트 (캐비닛 및 파밍)
        # =================================================================
        # [신규] 통합 캐비닛 키워드 (조사 시 개별 캐비닛 발견)
        KeywordId.CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="cabinets_inspected", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "복도 벽면을 따라 색색의 철제 캐비닛들이 나란히 놓여 있습니다.\n\n"
                                "왼쪽부터 **[초록색 캐비닛]**, **[빨간색 캐비닛]**, **[노란색 캐비닛]**입니다."
                            ),
                        ),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "cabinets_inspected", "value": True}),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.GREEN_CABINET),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.RED_CABINET),
                        Action(type=ActionType.DISCOVER_KEYWORD, value=KeywordId.YELLOW_CABINET),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="색색의 캐비닛들이 나란히 서 있습니다. 각각 확인해볼 수 있습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ]
                ),
            ],
        ),
        # =================================================================
        # 2. 개별 캐비닛 (INACTIVE -> DISCOVERED)
        # =================================================================
        # 2-1. 초록색 캐비닛 (매미 퍼즐)
        KeywordId.GREEN_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="green_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='<img src="assets/chapter1/cabinet_green_open.png" alt="초록 캐비닛" width="500">\n\n'
                            "초록색 캐비닛이 열려 있습니다. 청테이프를 챙겼습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.GREEN_CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/cabinet_green.png" alt="초록 캐비닛" width="500">\n\n'
                                "매미와 마이크가 그려진 초록색 캐비닛입니다.\n\n"
                                "하단에는 **4자리 숫자 자물쇠**가 굳게 잠겨 있습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.GREEN_CABINET} : [비밀번호 4자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
            ],
        ),
        # 2-2. 빨간색 캐비닛 (생태학/로마자 퍼즐)
        KeywordId.RED_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="red_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='<img src="assets/chapter1/cabinet_red_open.png" alt="빨강 캐비닛" width="500">\n\n'
                            "빨간색 캐비닛이 열려 있습니다. 그물망을 챙겼습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.RED_CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/cabinet_red.png" alt="빨강 캐비닛" width="500">\n\n'
                                "동물과 식물, 그리고 콜로세움이 그려진 빨간색 캐비닛입니다.\n\n"
                                "하단에는 **4자리 숫자 자물쇠**가 굳게 잠겨 있습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.RED_CABINET} : [비밀번호 4자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
            ],
        ),
        # 2-3. 노란색 캐비닛 (음악/DNA/색깔 퍼즐)
        KeywordId.YELLOW_CABINET: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.INACTIVE,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="yellow_opened", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value='<img src="assets/chapter1/cabinet_yellow_open.png" alt="노랑 캐비닛" width="500">\n\n'
                            "노란색 캐비닛이 열려 있습니다. 러버덕을 챙겼습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.YELLOW_CABINET, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                Interaction(
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                '<img src="assets/chapter1/cabinet_yellow.png" alt="노랑 캐비닛" width="500">\n\n'
                                "정체를 알 수 없는 다양한 그림이 그려진 노란색 캐비닛입니다.\n\n"
                                "하단에는 **4자리 숫자 자물쇠**가 굳게 잠겨 있습니다."
                            ),
                        ),
                        Action(
                            type=ActionType.PRINT_SYSTEM,
                            value=f"암호를 알아내어 `{KeywordId.YELLOW_CABINET} : [비밀번호 4자리]` 형식으로 입력해 보세요.",
                        ),
                    ],
                ),
            ],
        ),
        # [배관 점검구] (밸브 파밍 장소)
        # [수정된 배관 점검구] (단순 조사로는 획득 불가, 힌트만 제공)
        KeywordId.PLUMBING_HATCH: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            interactions=[
                # 이미 찾음
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="valve_found", value=True)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value="밸브가 빠진 파이프에서 물이 한 방울씩 떨어지고 있습니다. 더 볼일은 없습니다.",
                        ),
                        Action(
                            type=ActionType.UPDATE_STATE,
                            value={"keyword": KeywordId.PLUMBING_HATCH, "state": KeywordState.UNSEEN},
                        ),
                    ],
                ),
                # 첫 조사 (획득 실패 -> 도구 필요 암시)
                Interaction(
                    conditions=[Condition(type=ConditionType.STATE_IS, target="valve_found", value=False)],
                    actions=[
                        Action(
                            type=ActionType.PRINT_NARRATIVE,
                            value=(
                                "벽면 아래쪽의 점검구 덮개가 뜯겨져 나가 있습니다.\n\n"
                                "안쪽 배관에 멀쩡해 보이는 밸브가 하나 붙어 있습니다.\n\n"
                                "손으로 돌려보려 했지만 녹이 슬어 꿈쩍도 하지 않습니다. 꽉 물려서 돌릴만한 도구가 필요합니다."
                            ),
                        ),
                    ],
                ),
            ],
        ),
        # --- UNSEEN 오브젝트 (연구동 중앙 복도) ---
        "먼지": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="회색 눈이 내린 것처럼 소복하다. 내 폐가 공기청정기 역할을 하고 있는 것 같아 기분이 나쁘다.",
        ),
        "발자국": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="내 발자국이 선명하게 찍혔다. 범죄 현장에 증거를 남기는 기분이라 영 찜찜하다.",
        ),
        "천장": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="군데군데 텍스이 뜯겨져 나갔다. 저 어두운 구멍 안에서 누군가 날 내려다보고 있을 것만 같다.",
        ),
        "바닥": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="싸구려 리놀륨 바닥이다. 걸을 때마다 쩍쩍 달라붙는 소리가 복도를 울린다.",
        ),
        "조명": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="대부분 깨지거나 나갔다. 간신히 살아있는 형광등 하나가 '살려줘'라고 신호를 보내듯 깜빡거린다.",
        ),
        "벽": KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.UNSEEN,
            description="페인트가 피부병처럼 일어나 있다. 무심코 기대었다가는 옷 버리기 딱 좋다.",
        ),
    },
    combinations=[
        # 점검구 + 스패너 = 밸브 획득
        Combination(
            targets=[KeywordId.PLUMBING_HATCH, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.STATE_IS, target="valve_found", value=False)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "스패너를 밸브 너트에 정확히 물리고 체중을 실어 돌렸습니다.\n\n"
                        "**끼이익- 툭!**\n\n"
                        "녹슨 나사가 비명을 지르며 풀리고, **[황동 밸브]**가 바닥으로 떨어집니다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.BRASS_VALVE,
                        "description": "묵직한 황동 재질의 밸브 손잡이. 톱니 모양의 홈이 있어 파이프에 끼울 수 있다.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "valve_found", "value": True}),
            ],
        ),
        # 3-1. 초록 캐비닛 해제 (암호 예시: 3311 - 매미 소리 패턴)
        Combination(
            type=CombinationType.PASSWORD,
            conditions=[Condition(type=ConditionType.STATE_IS, target="green_opened", value=False)],
            targets=[KeywordId.GREEN_CABINET, "0317"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/cabinet_green_open.png" alt="초록 캐비닛" width="500">\n\n'
                        "철컥! 매미 소리의 리듬을 맞추자 자물쇠가 풀립니다.\n\n"
                        "초록색 캐비닛 안에는 **[청테이프]**가 산더미처럼 쌓여 있습니다.\n\n"
                        "'모든 것은 테이프로 해결된다'는 공대생의 영혼이 느껴집니다. 하나 챙겨두면 쓸모가 있을 겁니다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.DUCT_TAPE,
                        "description": "강력한 접착력을 가진 초록색 테이프. 뭐든지 붙일 수 있을 것 같다.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "green_opened", "value": True}),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FILE_TEMP,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.THERMOSTAT,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_2,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.CICADA_CAGE,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_2,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_CHAPTER_STATE,
                    value={
                        "key": "green_cabinet_opened",
                        "value": True,
                    },
                ),
                # Action(type=ActionType.ADD_ITEM, value={...}), # 보상 아이템 추가 필요
            ],
        ),
        # 3-2. 빨강 캐비닛 해제 (암호 예시: 1156 - MCLVI 로마자 변환 합산)
        Combination(
            type=CombinationType.PASSWORD,
            conditions=[Condition(type=ConditionType.STATE_IS, target="red_opened", value=False)],
            targets=[KeywordId.RED_CABINET, "1956"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/cabinet_red_open.png" alt="빨강 캐비닛" width="500">\n\n'
                        "달그락! 생물들의 이름 속에 숨겨진 로마 숫자가 정답이었습니다.\n\n"
                        "빨간색 캐비닛이 열리자 촘촘하게 짜인 **[그물망]**이 쏟아져 나옵니다.\n\n"
                        "야생 동물 포획용으로 쓰던 것 같습니다. 꽤 튼튼해 보입니다."
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.NET,
                        "description": "질기고 튼튼한 그물망. 물건을 묶기에 좋다.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "red_opened", "value": True}),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SURVEY_LOG,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.ECOLOGY_BOOK_TITLE,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.ECOLOGY_BOOK_INDEX,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.ECOLOGY_BOOK_BODY,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_CHAPTER_STATE,
                    value={
                        "key": "red_cabinet_opened",
                        "value": True,
                    },
                ),
                # Action(type=ActionType.ADD_ITEM, value={...}), # 보상 아이템 추가 필요
            ],
        ),
        # 3-3. 노랑 캐비닛 해제 (암호 예시: 2320 - 악보->로마자->상보결합->숫자)
        Combination(
            type=CombinationType.PASSWORD,
            conditions=[Condition(type=ConditionType.STATE_IS, target="yellow_opened", value=False)],
            targets=[KeywordId.YELLOW_CABINET, "2320"],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        '<img src="assets/chapter1/cabinet_yellow_open.png" alt="노랑 캐비닛" width="500">\n\n'
                        "띠리릭! 별의 노래와 DNA의 결합 법칙이 맞아떨어졌습니다.\n\n"
                        "노란색 캐비닛 문을 열자마자 노란색 파도가 밀려옵니다. **[러버덕]**입니다!\n\n"
                        "한두 마리가 아니라 수백 마리가 와르르 쏟아져 내 발등을 덮칩니다.\n\n"
                        "'삑- 삑-'\n\n"
                        "바닥에 떨어진 오리들이 비명을 지르는 것 같습니다.\n"
                        "여기 있던 과학자는 오리 군단으로 세계 정복이라도 꿈꿨던 걸까요?\n\n"
                    ),
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.RUBBER_DUCK,
                        "description": "귀여운 노란색 오리 인형. 물에 아주 잘 뜬다.",
                    },
                ),
                Action(type=ActionType.UPDATE_STATE, value={"key": "yellow_opened", "value": True}),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FILE_MUSIC,
                ),
                Action(
                    type=ActionType.REMOVE_ITEM,
                    value=KeywordId.FILE_DNA,
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SHEET_MUSIC_1,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SHEET_MUSIC_1,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SHEET_MUSIC_2,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_STATE,
                    value={
                        "keyword": KeywordId.SHEET_MUSIC_3,
                        "state": KeywordState.UNSEEN,
                        "scene_id": SceneID.CH1_SCENE3_3,
                    },
                ),
                Action(
                    type=ActionType.UPDATE_CHAPTER_STATE,
                    value={
                        "key": "yellow_cabinet_opened",
                        "value": True,
                    },
                ),
            ],
        ),
        # (기존 배관 점검구 + 스패너 조합 등은 유지)
    ],
)
