from typing import Any

from const import ActionType, ConditionType, KeywordState, KeywordType, SceneID
from pydantic import BaseModel, Field

# --- 하위 모델 정의 ---


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


class KeywordData(BaseModel):
    type: KeywordType = KeywordType.OBJECT
    state: KeywordState = KeywordState.HIDDEN
    display_name: str | None = None
    description: str | None = None
    interactions: list[Interaction] = Field(default_factory=list)
    silent_discovery: bool = False
    target: str | None = None  # Alias일 경우 원본 타겟


class Combination(BaseModel):
    targets: list[str]
    conditions: list[Condition] = Field(default_factory=list)
    actions: list[Action]


# --- 메인 씬 데이터 모델 ---


class SceneData(BaseModel):
    id: SceneID
    name: str
    initial_text: str
    initial_state: dict[str, Any] = Field(default_factory=dict)
    keywords: dict[str, KeywordData] = Field(default_factory=dict)
    combinations: list[Combination] = Field(default_factory=list)
    on_enter_actions: list[Action] = Field(default_factory=list)
