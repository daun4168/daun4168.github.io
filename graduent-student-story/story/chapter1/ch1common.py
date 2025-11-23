from const import ActionType, ChapterID, ConditionType, KeywordId
from schemas import Action, ChapterData, Combination, Condition

CH1_COMMON_DATA = ChapterData(
    id=ChapterID.CH1,
    combinations=[
        # [공통 조합] 스패너 + 코코넛 = 섭취
        Combination(
            targets=[KeywordId.COCONUT, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 **[코코넛]**을 깨서 속의 물을 마셨다. 미지근하지만 달콤하다. 남은 **[코코넛 껍질]**은 챙겨 두자.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "속을 다 비운 코코넛 껍질이다. 잘 말리면 그릇이나 수차 날개로 쓸 수 있을 것 같다.",
                    },
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=5),
                Action(type=ActionType.PRINT_SYSTEM, value="갈증 해소! 체력 +5"),
            ],
        ),
        # [공통 조합] 소방 도끼 + 코코넛 = 섭취
        Combination(
            targets=[KeywordId.COCONUT, KeywordId.FIRE_AXE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[소방 도끼]**로 **[코코넛]**을 깨서 속의 물을 마셨다. 미지근하지만 달콤하다. 남은 **[코코넛 껍질]**은 챙겨 두자.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.COCONUT_SHELL,
                        "description": "속을 다 비운 코코넛 껍질이다. 잘 말리면 그릇이나 수차 날개로 쓸 수 있을 것 같다.",
                    },
                ),
                Action(type=ActionType.MODIFY_STAMINA, value=5),
                Action(type=ActionType.PRINT_SYSTEM, value="갈증 해소! 체력 +5"),
            ],
        ),
        # [준비용 조합] 고무 + 전선 = 절연 전선
        Combination(
            targets=[KeywordId.RUBBER, KeywordId.WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RUBBER),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WIRE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "벗겨진 전선 부분에 잘게 뜯은 고무를 감싸고, 손으로 꼭꼭 눌러 붙였다.\n"
                        "즉석에서 만든 절연층이 어느 정도는 버텨 줄 것 같다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RUBBER),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.WIRE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.INSULATED_WIRE,
                        "description": "고무로 감싼 전선이다. 맨손으로 잡고 써도 비교적 안전할 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="절연 전선을 만들었습니다.",
                ),
            ],
        ),
        # ------------------------------------------------------------------
        # 수차 / 발전기 제작 라인
        # ------------------------------------------------------------------
        # --- 1) 코팅된 코코넛 껍질 + 덩굴 줄기 → 임시 수차 로터 ---
        Combination(
            targets=[KeywordId.COATED_COCONUT_SHELL, KeywordId.VINE_STEM],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COATED_COCONUT_SHELL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코팅된 코코넛 껍질을 십자 모양으로 엇갈려 놓고, 덩굴 줄기로 단단히 묶는다.\n"
                        "중앙에는 축을 꽂을 수 있는 작은 구멍을 뚫어 두었다. 제법 그럴듯한 임시 수차 로터가 완성됐다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COATED_COCONUT_SHELL),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINE_STEM),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MAKESHIFT_ROTOR,
                        "description": "코팅된 코코넛 껍질과 덩굴 줄기로 만든 임시 수차 로터다.",
                    },
                ),
            ],
        ),
        # 잘못된 조합: 코팅된 코코넛 껍질 + 바위 고리
        Combination(
            targets=[KeywordId.COATED_COCONUT_SHELL, KeywordId.STONE_RING],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COATED_COCONUT_SHELL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_RING),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코팅된 코코넛 껍질을 바위 고리에 대 보지만, 축도 없고 묶을 방법도 마땅치 않다.\n"
                        "먼저 덩굴로 수차 모양을 만든 뒤에, 그다음에 고리와 조합하는 편이 좋겠다."
                    ),
                )
            ],
        ),
        # 잘못된 조합: 덩굴 줄기 + 바위 고리
        Combination(
            targets=[KeywordId.VINE_STEM, KeywordId.STONE_RING],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_RING),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "덩굴 줄기를 바위 고리에 아무렇게나 감아 보았지만, 그 흔한 수건 걸이 이상으로는 쓸모가 없어 보인다.\n"
                        "수차의 축을 끼우는 데 쓰는 편이 좋겠다."
                    ),
                )
            ],
        ),
        # --- 2) 임시 수차 로터 + 나무 축 → 축 달린 수차 ---
        Combination(
            targets=[KeywordId.MAKESHIFT_ROTOR, KeywordId.WOODEN_SHAFT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAKESHIFT_ROTOR),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WOODEN_SHAFT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "나무 축을 수차 로터 중앙 구멍에 끼운 뒤, 덩굴 조각과 테이프로 양쪽을 단단히 고정한다.\n"
                        "손으로 돌려 보니, 수차가 축을 중심으로 부드럽게 회전한다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.MAKESHIFT_ROTOR),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.WOODEN_SHAFT),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.SHAFTED_ROTOR,
                        "description": "나무 축이 끼워진 수차 로터다. 이제 베어링만 있으면 폭포 옆에서 쓸 수 있다.",
                    },
                ),
            ],
        ),
        # 잘못된 조합: 나무 축 + 덩굴 줄기
        Combination(
            targets=[KeywordId.WOODEN_SHAFT, KeywordId.VINE_STEM],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WOODEN_SHAFT),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "나무 축에 덩굴만 감아 보았더니, 어디서 본 듯한 막대기 모양의 무기가 하나 생겼다.\n"
                        "수차를 만들 거라면 코코넛 껍질과 같이 쓰는 편이 더 낫겠다."
                    ),
                )
            ],
        ),
        # --- 3) 축 달린 수차 + 바위 고리 → 고리에 끼운 수차 ---
        Combination(
            targets=[KeywordId.SHAFTED_ROTOR, KeywordId.STONE_RING],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SHAFTED_ROTOR),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.STONE_RING),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "바위 고리의 매끈한 구멍에 수차의 나무 축을 조심스럽게 끼워 넣는다.\n"
                        "양쪽을 조율하자, 수차가 거의 마찰 없이 매끈하게 돌아가기 시작한다. 자연산 베어링 치고는 매우 훌륭한 성능이다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.SHAFTED_ROTOR),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.STONE_RING),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.MOUNTED_ROTOR,
                        "description": "바위 고리에 축이 끼워진 수차다. 그대로 폭포 옆에 세우면 수력 발전 장치의 뼈대가 된다.",
                    },
                ),
            ],
        ),
        # 잘못된 조합: 축 달린 수차 + 절연 구리선
        Combination(
            targets=[KeywordId.SHAFTED_ROTOR, KeywordId.INSULATED_COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SHAFTED_ROTOR),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.INSULATED_COPPER_WIRE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=("축 달린 수차에 구리선을 대충 감아 보았지만, 전기보다는 엉킨 줄이 먼저 떠오른다.\n"),
                )
            ],
        ),
        # --- 4) 자철석 조각 + 절연 구리선 → 발전 코어 ---
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.INSULATED_COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.INSULATED_COPPER_WIRE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석 조각을 손에 쥐고 절연 구리선을 빽빽하게 감아 나간다.\n"
                        "여러 겹을 감은 뒤 양 끝 전선을 단자처럼 조금 남겨 꺾어 두자, 어디서 많이 본 발전 코어 모양이 완성된다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.INSULATED_COPPER_WIRE),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.MAGNETITE_CHUNK),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.DYNAMO_CORE,
                        "description": "자철석 조각에 절연 구리선을 감아 만든 발전 코어다.",
                    },
                ),
            ],
        ),
        # 잘못된 조합: 자철석 조각 + 덩굴 줄기 → 구박
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.VINE_STEM],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="자철석 조각에 덩굴을 감아 보았지만, 이것은 전기가 아니라 예술의 영역에 가까운 실패작일 뿐이다.",
                )
            ],
        ),
        # 자철석 조각 + 코코넛 껍질 -> 부정 피드백
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.COCONUT_SHELL],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="코코넛 껍질 위에 자철석 조각을 올려 보았지만, 과학이라기보다는 수상한 인테리어 소품에 가깝다.",
                )
            ],
        ),
        # --- 5) 고리에 끼운 수차 + 발전 코어 → 수력 발전 모듈 ---
        Combination(
            targets=[KeywordId.MOUNTED_ROTOR, KeywordId.DYNAMO_CORE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MOUNTED_ROTOR),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.DYNAMO_CORE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "바위 고리에 끼운 수차 한쪽 옆에 발전 코어를 단단히 묶고, 축이 도는 방향에 맞춰 코일 방향을 조정한다.\n"
                        "이제 물살만 있으면 전기를 만들어낼 수 있는 수력 발전 모듈이 준비됐다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.MOUNTED_ROTOR),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.DYNAMO_CORE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.HYDRO_DYNAMO_MODULE,
                        "description": "바위 고리 베어링과 수차, 발전 코어를 한 몸으로 묶은 수력 발전 모듈이다.",
                    },
                ),
            ],
        ),
        # 잘못된 조합: 수력 발전 모듈 + 덩굴 줄기
        Combination(
            targets=[KeywordId.HYDRO_DYNAMO_MODULE, KeywordId.VINE_STEM],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.HYDRO_DYNAMO_MODULE),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "수력 발전 모듈에 덩굴을 한 번 더 감아 보려 했지만, 이 정도면 이미 충분히 위험해 보인다.\n"
                        "불필요한 데코레이션은 과학 실험보다 집 꾸미기에 더 어울린다."
                    ),
                )
            ],
        ),
        # [부정] 코팅된 코코넛 껍질 + 나무 축: 중간 단계(로터 조립) 누락
        Combination(
            targets=[KeywordId.COATED_COCONUT_SHELL, KeywordId.WOODEN_SHAFT],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COATED_COCONUT_SHELL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.WOODEN_SHAFT),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코팅된 코코넛 껍질 하나에 나무 축을 대 보았다. 중심을 잡을 수도 없고, 회전력을 만들 날개도 부족하다.\n"
                        "먼저 껍질들을 엮어서 '로터' 형태를 만든 뒤에 축을 끼워야 할 것 같다."
                    ),
                )
            ],
        ),
        # [부정] 자철석 조각 + 스패너: 자성 실험(?)
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.SPANNER],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.SPANNER),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석 조각을 스패너에 갖다 대자 '탁' 하고 달라붙는다. 자성은 확인했지만 그뿐이다.\n"
                        "스패너를 자석으로 만든다고 해서 탈출에 도움이 될 것 같지는 않다."
                    ),
                )
            ],
        ),
        # [부정] 코코넛 껍질 + 덩굴 줄기: 코팅(방수) 필요성 암시
        Combination(
            targets=[KeywordId.COCONUT_SHELL, KeywordId.VINE_STEM],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT_SHELL),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINE_STEM),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "코코넛 껍질을 덩굴로 엮어 보았지만, 표면이 거칠고 금방이라도 물을 먹어 무거워질 것 같다.\n"
                        "거센 물살을 버티려면 껍질 표면에 **끈적하고 물을 튕겨내는 무언가**를 발라 코팅 처리를 먼저 해야 한다."
                    ),
                )
            ],
        ),
        # [부정] 자철석 조각 + 구리선: 절연 필요성 암시
        Combination(
            targets=[KeywordId.MAGNETITE_CHUNK, KeywordId.COPPER_WIRE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.MAGNETITE_CHUNK),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COPPER_WIRE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "자철석에 맨 구리선을 바로 감으려다 멈칫했다. 피복 없는 전선끼리 닿으면 **쇼트(단락)**가 나서 전기를 모을 수 없다.\n"
                        "구리선 표면을 **전기가 통하지 않는 물질**로 감싸서 절연 처리를 한 뒤에 감아야 한다."
                    ),
                )
            ],
        ),
    ],
)
