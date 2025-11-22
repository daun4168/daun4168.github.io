from const import ActionType, ChapterID, ConditionType, KeywordId
from schemas import Action, ChapterData, Combination, Condition

# 챕터 1 전체에서 공통으로 사용될 데이터
CH1_COMMON_DATA = ChapterData(
    id=ChapterID.CH1,
    combinations=[
        # [공통 조합] 스패너 + 코코넛 = 섭취
        # 어떤 씬에서든 코코넛과 스패너가 있다면 먹을 수 있음
        Combination(
            targets=[KeywordId.COCONUT, KeywordId.SPANNER],
            conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.COCONUT)],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value="**[스패너]**로 **[코코넛]**을 깨서 마셨다. 미지근하지만 달콤하다.",
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT),
                Action(type=ActionType.MODIFY_STAMINA, value=15),
                Action(type=ActionType.PRINT_SYSTEM, value="갈증 해소! 체력 +15"),
            ],
        ),
        # [준비용 조합 1] 라텍스 + 식초(풀) → 고무 + 반쯤 남은 식초
        Combination(
            targets=[KeywordId.LATEX, KeywordId.VINEGAR],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LATEX),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "라텍스를 용기에 담고 식초를 조금씩 떨어뜨렸다.\n"
                        "흐물흐물하던 액체가 점점 덩어리 지더니, 탄력 있는 고무 덩어리로 굳어 간다.\n"
                        "식초는 절반쯤만 줄어든 것 같아, 나머지는 다른 용도로도 쓸 수 있을 것 같다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.LATEX),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINEGAR),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.RUBBER,
                        "description": "질긴 고무 덩어리다. 전선을 감싸거나 틈을 막는 데 쓸 수 있을 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.VINEGAR_HALF,
                        "description": "반쯤 남은 식초다. 아직 한 번 정도는 더 쓸 수 있을 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="라텍스가 고무로 응고되었습니다. 식초는 반쯤 남았습니다.",
                ),
            ],
        ),
        # [준비용 조합 2] 라텍스 + 반쯤 남은 식초 → 고무 (식초 완전 소진)
        Combination(
            targets=[KeywordId.LATEX, KeywordId.VINEGAR_HALF],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.LATEX),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.VINEGAR_HALF),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "남아 있던 식초를 전부 라텍스에 부었다.\n"
                        "금세 라텍스가 덩어리 지며 고무로 굳어 버리고, 통 안에는 아무것도 남지 않는다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.LATEX),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.VINEGAR_HALF),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.RUBBER,
                        "description": "질긴 고무 덩어리다. 전선을 감싸거나 틈을 막는 데 쓸 수 있을 것 같다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="라텍스가 고무로 응고되었습니다. 식초는 전부 사용되었습니다.",
                ),
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
        # [준비용 조합] 송진 + 조명탄 = 방수 부츠
        Combination(
            targets=[KeywordId.RESIN, KeywordId.FLARE],
            conditions=[
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.RESIN),
                Condition(type=ConditionType.HAS_ITEM, target=KeywordId.FLARE),
            ],
            actions=[
                Action(
                    type=ActionType.PRINT_NARRATIVE,
                    value=(
                        "조명탄을 피워 그 위에 송진을 올려두었다.\n"
                        "끈적한 송진이 녹아 흐르기 시작하자, 신발 바닥과 옆면에 두껍게 발라 코팅했다.\n"
                        "이 정도면 웬만한 물과 진흙쯤은 버텨 줄 것 같다."
                    ),
                ),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.RESIN),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.FLARE),
                Action(
                    type=ActionType.ADD_ITEM,
                    value={
                        "name": KeywordId.WATERPROOF_BOOTS,
                        "description": "거칠게 송진 코팅을 한 방수 부츠다. 늪지대나 젖은 지형을 걸을 때 도움이 된다.",
                    },
                ),
                Action(
                    type=ActionType.PRINT_SYSTEM,
                    value="신발에 송진 코팅을 해 방수 부츠를 만들었습니다.",
                ),
            ],
        ),
    ],
)
