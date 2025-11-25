from typing import Any

from const import ActionType, ChapterID, CombinationType, ConditionType, KeywordState, KeywordType, SceneID
from pydantic import BaseModel, Field


# --- 하위 모델 정의 ---
# (기존 Condition, Action, Interaction, KeywordData, Combination 유지)
class Condition(BaseModel):
    type: ConditionType
    target: str
    value: Any = None


class Action(BaseModel):
    type: ActionType
    value: Any = None


class Interaction(BaseModel):
    conditions: list[Condition] = Field(default_factory=list)
    actions: list[Action]
    continue_matching: bool = False


class KeywordData(BaseModel):
    type: KeywordType = KeywordType.OBJECT
    state: KeywordState = KeywordState.HIDDEN
    display_name: str | None = None
    description: str | None = None
    interactions: list[Interaction] = Field(default_factory=list)
    silent_discovery: bool = False
    target: str | None = None


class Combination(BaseModel):
    type: CombinationType = CombinationType.DEFAULT
    targets: list[str]
    conditions: list[Condition] = Field(default_factory=list)
    actions: list[Action]


# --- 메인 씬 데이터 모델 ---


# [추가] 챕터 공통 데이터를 위한 모델
class ChapterData(BaseModel):
    id: ChapterID
    combinations: list[Combination] = Field(default_factory=list)


class SceneData(BaseModel):
    id: SceneID
    name: str
    body: str
    initial_text: str | None = None
    initial_state: dict[str, Any] = Field(default_factory=dict)
    keywords: dict[str, KeywordData] = Field(default_factory=dict)
    combinations: list[Combination] = Field(default_factory=list)
    on_enter_actions: list[Action] = Field(default_factory=list)
