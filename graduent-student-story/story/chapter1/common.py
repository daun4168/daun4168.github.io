from const import ActionType, ConditionType, KeywordId, ChapterID, CombinationType
from schemas import Action, Combination, Condition, ChapterData

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
                Action(type=ActionType.PRINT_NARRATIVE, value="**[스패너]**로 **[코코넛]**을 깨서 마셨다. 미지근하지만 달콤하다."),
                Action(type=ActionType.REMOVE_ITEM, value=KeywordId.COCONUT),
                Action(type=ActionType.MODIFY_STAMINA, value=15),
                Action(type=ActionType.PRINT_SYSTEM, value="갈증 해소! 체력 +15"),
            ]
        )
    ]
)