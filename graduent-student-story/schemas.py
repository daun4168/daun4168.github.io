from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from const import SceneID, KeywordType, KeywordState, ConditionType, ActionType

# --- 하위 모델 정의 ---

class Condition(BaseModel):
    type: ConditionType
    target: str
    value: Any = None

class Action(BaseModel):
    type: ActionType
    value: Any = None

class Interaction(BaseModel):
    conditions: List[Condition] = Field(default_factory=list)
    actions: List[Action]

class KeywordData(BaseModel):
    type: KeywordType = KeywordType.OBJECT
    state: KeywordState = KeywordState.HIDDEN
    display_name: Optional[str] = None
    description: Optional[str] = None
    interactions: List[Interaction] = Field(default_factory=list)
    silent_discovery: bool = False
    target: Optional[str] = None  # Alias일 경우 원본 타겟

class Combination(BaseModel):
    targets: List[str]
    conditions: List[Condition] = Field(default_factory=list)
    actions: List[Action]

# --- 메인 씬 데이터 모델 ---

class SceneData(BaseModel):
    id: SceneID
    name: str
    initial_text: str
    initial_state: Dict[str, Any] = Field(default_factory=dict)
    keywords: Dict[str, KeywordData] = Field(default_factory=dict)
    combinations: List[Combination] = Field(default_factory=list)
    on_enter_actions: List[Action] = Field(default_factory=list)