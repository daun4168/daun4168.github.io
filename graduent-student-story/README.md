# Graduent Student Story: 게임 데이터 추가 가이드

이 문서는 게임의 새로운 챕터나 장면 데이터를 추가하려는 기획자분들을 위해 작성되었습니다. 게임의 로직은 `Python` 코드로 구현되어 있지만, 스토리와 관련된 대부분의 데이터는 구조화된 형태로 정의되어 있어 코드 수정 없이 데이터 파일만으로 새로운 내용을 추가할 수 있습니다.

## 1. 게임 데이터 구조 이해하기

게임의 모든 스토리 및 상호작용 데이터는 `schemas.py`에 정의된 Pydantic 모델을 따릅니다. 주요 모델은 다음과 같습니다.

*   **`SceneData`**: 하나의 장면(Scene)을 정의하는 최상위 데이터 구조입니다.
*   **`KeywordData`**: 장면 내에서 플레이어가 상호작용할 수 있는 키워드(사물, NPC, 아이템 등)를 정의합니다.
*   **`Interaction`**: 특정 키워드에 대한 상호작용 방식을 정의합니다. 조건(`conditions`)과 액션(`actions`)으로 구성됩니다.
*   **`Condition`**: 특정 `Interaction`이나 `Combination`이 실행되기 위한 조건을 정의합니다.
*   **`Action`**: `Interaction`이나 `Combination`이 실행될 때 발생하는 결과를 정의합니다.
*   **`Combination`**: 두 키워드(예: 아이템 + 사물)를 조합했을 때 발생하는 상호작용을 정의합니다.

또한, `const.py` 파일에는 게임 전반에 사용되는 상수(장면 ID, 키워드 타입, 액션 타입 등)가 정의되어 있습니다.

## 2. 새로운 장면 데이터 추가 단계

새로운 장면을 추가하는 과정은 크게 세 단계로 나뉩니다.

### 단계 1: 새로운 장면 데이터 파일 생성

`story/chapterX/` 디렉토리 아래에 새로운 Python 파일을 생성합니다. (예: `story/chapter1/scene0.py`)

이 파일 내에서 `SceneData` 객체를 생성하고, 해당 장면의 모든 스토리 및 상호작용 데이터를 정의합니다.

**예시: `story/chapter1/scene0.py`**

```python
from const import SceneID, KeywordId, KeywordState, ActionType, ConditionType, KeywordType
from schemas import SceneData, KeywordData, Interaction, Condition, Action, Combination

# 새로운 장면의 고유 ID를 정의합니다. (const.py에 먼저 추가해야 합니다!)
CH1_SCENE0_DATA = SceneData(
    id=SceneID.CH1_SCENE0, # const.py에 정의된 SceneID 사용
    name="새로운 연구실", # 장면의 이름
    initial_text="새로운 연구실에 도착했습니다. 먼지가 가득하고 낯선 기계들이 보입니다.", # 장면 진입 시 출력될 초기 텍스트
    initial_state={
        "is_light_on": False, # 이 장면에서 사용할 동적 상태 변수 (딕셔너리 형태)
    },
    on_enter_actions=[ # 장면 진입 시 자동으로 실행될 액션 목록
        Action(type=ActionType.PRINT_SYSTEM, value="주변을 잘 살펴보세요.")
    ],
    keywords={ # 이 장면에서 플레이어가 상호작용할 수 있는 키워드들
        KeywordId.LIGHT_SWITCH: KeywordData( # const.py에 정의된 KeywordId 사용
            type=KeywordType.OBJECT, # 키워드 타입 (OBJECT, ITEM, NPC, PORTAL, ALIAS)
            state=KeywordState.HIDDEN, # 초기 상태 (HIDDEN, DISCOVERED, INACTIVE)
            display_name="전등 스위치", # UI에 표시될 이름 (없으면 KeywordId 사용)
            description="오래된 전등 스위치입니다. 켜볼 수 있을 것 같습니다.", # 키워드 조사 시 출력될 설명
            interactions=[ # 이 키워드에 대한 상호작용 목록
                Interaction(
                    conditions=[ # 상호작용이 실행되기 위한 조건 (모든 조건이 True여야 함)
                        Condition(type=ConditionType.STATE_IS, target="is_light_on", value=False)
                    ],
                    actions=[ # 조건이 충족되었을 때 실행될 액션 목록
                        Action(type=ActionType.PRINT_NARRATIVE, value="스위치를 켜자 연구실에 불이 들어옵니다."),
                        Action(type=ActionType.UPDATE_STATE, value={"key": "is_light_on", "value": True}),
                        Action(type=ActionType.REMOVE_KEYWORD, value=KeywordId.LIGHT_SWITCH), # 스위치는 한 번만 켜지도록 제거
                        Action(type=ActionType.ADD_ITEM, value={"name": KeywordId.OLD_KEY, "description": "녹슨 오래된 열쇠입니다."}),
                        Action(type=ActionType.PRINT_SYSTEM, value="**[오래된 열쇠]**를 발견했습니다.")
                    ]
                ),
                Interaction( # 조건이 없는 Interaction은 항상 마지막에 위치해야 합니다.
                    actions=[
                        Action(type=ActionType.PRINT_NARRATIVE, value="이미 불이 켜져 있습니다.")
                    ]
                )
            ]
        ),
        KeywordId.DOOR: KeywordData(
            type=KeywordType.PORTAL, # 문은 PORTAL 타입으로 다른 장면으로 이동할 수 있습니다.
            state=KeywordState.DISCOVERED,
            interactions=[
                Interaction(
                    conditions=[Condition(type=ConditionType.HAS_ITEM, target=KeywordId.OLD_KEY)],
                    actions=[
                        Action(type=ActionType.PRINT_SYSTEM, value="열쇠로 문을 열고 다음 장소로 이동합니다."),
                        Action(type=ActionType.MOVE_SCENE, value=SceneID.CH1_SCENE1) # 다음 장면 ID
                    ]
                ),
                Interaction(
                    actions=[
                        Action(type=ActionType.PRINT_SYSTEM, value="문이 잠겨 있습니다. 열쇠가 필요해 보입니다.")
                    ]
                )
            ]
        ),
        KeywordId.OLD_KEY: KeywordData( # 아이템은 보통 HIDDEN 상태로 시작하여 특정 상호작용으로 DISCOVERED 됩니다.
            type=KeywordType.ITEM,
            state=KeywordState.HIDDEN,
            silent_discovery=True, # 이 키워드는 발견 시 시스템 메시지를 출력하지 않습니다. (ADD_ITEM 액션에서 메시지 처리)
            description="녹슨 오래된 열쇠입니다. 어디에 쓰는 물건일까요?"
        ),
        KeywordId.COMPUTER_ALIAS: KeywordData( # ALIAS 타입은 다른 키워드의 별칭입니다.
            type=KeywordType.ALIAS,
            target=KeywordId.OLD_COMPUTER # 실제 대상 키워드
        ),
        KeywordId.OLD_COMPUTER: KeywordData(
            type=KeywordType.OBJECT,
            state=KeywordState.HIDDEN,
            description="오래된 컴퓨터입니다. 전원이 꺼져 있습니다."
        )
    },
    combinations=[ # 두 키워드를 조합했을 때 발생하는 상호작용 목록
        Combination(
            targets=[KeywordId.OLD_COMPUTER, KeywordId.OLD_KEY], # 조합할 두 키워드
            conditions=[
                Condition(type=ConditionType.STATE_IS, target="is_light_on", value=True)
            ],
            actions=[
                Action(type=ActionType.PRINT_NARRATIVE, value="열쇠로 컴퓨터를 켜자 화면에 알 수 없는 문자가 나타납니다."),
                Action(type=ActionType.UPDATE_STATE, value={"keyword": KeywordId.OLD_COMPUTER, "state": KeywordState.DISCOVERED})
            ]
        )
    ]
)
```

### `SceneData` 필드 설명

*   **`id` (필수)**: `const.py`에 정의된 `SceneID` Enum 값입니다. 각 장면을 고유하게 식별합니다.
*   **`name` (필수)**: 게임 UI에 표시될 장면의 이름입니다.
*   **`initial_text` (필수)**: 플레이어가 이 장면에 진입했을 때 가장 먼저 출력될 스토리 텍스트입니다. 마크다운 문법을 사용할 수 있습니다.
*   **`initial_state` (선택)**: 이 장면 내에서만 유효한 동적인 상태 변수들을 딕셔너리 형태로 정의합니다. (예: `{"is_light_on": False}`)
*   **`on_enter_actions` (선택)**: 플레이어가 이 장면에 진입하자마자 자동으로 실행될 `Action` 목록입니다.
*   **`keywords` (선택)**: 이 장면에서 플레이어가 `[키워드]`를 입력하여 상호작용할 수 있는 모든 키워드를 정의합니다. `KeywordId`를 키로, `KeywordData` 객체를 값으로 하는 딕셔너리입니다.
*   **`combinations` (선택)**: 두 키워드를 조합했을 때 발생하는 특별한 상호작용을 정의합니다. `Combination` 객체들의 리스트입니다.

### `KeywordData` 필드 설명

*   **`type` (필수)**: `const.py`에 정의된 `KeywordType` Enum 값입니다.
    *   `OBJECT`: 일반적인 사물 (책상, 컴퓨터 등)
    *   `ITEM`: 플레이어가 획득할 수 있는 아이템 (법인카드, 스패너 등)
    *   `NPC`: 게임 내 캐릭터 (교수님 등)
    *   `PORTAL`: 다른 장면으로 이동할 수 있는 키워드 (문 등)
    *   `ALIAS`: 다른 키워드의 별칭 (예: "컴퓨터" -> "오래된 컴퓨터")
*   **`state` (필수)**: `const.py`에 정의된 `KeywordState` Enum 값입니다. 키워드의 현재 상태를 나타냅니다.
    *   `HIDDEN`: 플레이어의 시야에 보이지 않으며, 직접 입력해야만 상호작용 가능합니다.
    *   `DISCOVERED`: 플레이어의 시야에 보이며, 상호작용 가능합니다.
    *   `INACTIVE`: 시야에 보이지 않고, 상호작용도 불가능합니다. (주로 일회성 키워드 처리 후 사용)
*   **`display_name` (선택)**: UI의 시야 목록에 표시될 이름입니다. 이 값이 없으면 `KeywordId`가 대신 사용됩니다.
*   **`description` (선택)**: 플레이어가 이 키워드를 조사했을 때 출력될 설명 텍스트입니다.
*   **`interactions` (선택)**: 이 키워드에 대한 상호작용 목록입니다. `Interaction` 객체들의 리스트입니다.
    *   **주의**: `conditions`가 없는 `Interaction`은 항상 해당 키워드의 `interactions` 리스트의 **가장 마지막**에 위치해야 합니다. 조건이 없는 `Interaction`은 항상 실행되기 때문입니다.
*   **`silent_discovery` (선택)**: `True`로 설정하면 키워드가 `HIDDEN`에서 `DISCOVERED`로 변경될 때 "키워드를 발견했습니다"와 같은 시스템 메시지를 출력하지 않습니다. (주로 `ADD_ITEM` 액션 등에서 별도로 메시지를 출력할 때 사용)
*   **`target` (선택)**: `KeywordType.ALIAS`일 경우, 이 별칭이 가리키는 실제 `KeywordId`를 지정합니다.

### `Interaction` 필드 설명

*   **`conditions` (선택)**: `Condition` 객체들의 리스트입니다. 이 `Interaction`이 실행되기 위한 모든 조건이 `True`여야 합니다.
*   **`actions` (필수)**: `Action` 객체들의 리스트입니다. `conditions`가 충족되면 이 액션들이 순서대로 실행됩니다.

### `Condition` 필드 설명

*   **`type` (필수)**: `const.py`에 정의된 `ConditionType` Enum 값입니다.
    *   `HAS_ITEM`: 플레이어가 특정 아이템을 가지고 있는지 확인합니다.
    *   `NOT_HAS_ITEM`: 플레이어가 특정 아이템을 가지고 있지 않은지 확인합니다.
    *   `STATE_IS`: 장면의 `initial_state` 또는 키워드의 `state`가 특정 값과 일치하는지 확인합니다.
    *   `STATE_NOT`: 장면의 `initial_state` 또는 키워드의 `state`가 특정 값과 일치하지 않는지 확인합니다.
*   **`target` (필수)**: 조건의 대상이 되는 `KeywordId` (아이템 이름) 또는 `initial_state`의 키.
*   **`value` (선택)**: `STATE_IS` 또는 `STATE_NOT` 조건에서 비교할 값.

### `Action` 필드 설명

*   **`type` (필수)**: `const.py`에 정의된 `ActionType` Enum 값입니다.
    *   `PRINT_NARRATIVE`: 스토리 텍스트를 출력합니다.
    *   `PRINT_SYSTEM`: 시스템 메시지를 출력합니다.
    *   `ADD_ITEM`: 인벤토리에 아이템을 추가합니다. `value`는 `{"name": "아이템ID", "description": "설명", "silent": True/False}` 형태의 딕셔너리입니다.
    *   `REMOVE_ITEM`: 인벤토리에서 아이템을 제거합니다. `value`는 제거할 아이템의 `KeywordId`입니다.
    *   `MOVE_SCENE`: 다른 장면으로 이동합니다. `value`는 이동할 장면의 `SceneID`입니다.
    *   `REMOVE_KEYWORD`: 현재 장면에서 키워드를 완전히 제거합니다. `value`는 제거할 키워드의 `KeywordId`입니다.
    *   `UPDATE_STATE`: 장면의 `initial_state` 변수를 업데이트하거나, 특정 키워드의 `state`를 변경합니다.
        *   장면 상태 업데이트: `{"key": "상태변수키", "value": "새로운값"}`
        *   키워드 상태 업데이트: `{"keyword": "키워드ID", "state": KeywordState.새로운상태}`
    *   `GAME_END`: 게임을 종료하고 메시지를 출력합니다.

### `Combination` 필드 설명

*   **`targets` (필수)**: 조합할 두 키워드의 `KeywordId` 리스트입니다. (예: `[KeywordId.ITEM_A, KeywordId.OBJECT_B]`) 순서는 중요하지 않습니다.
*   **`conditions` (선택)**: 이 `Combination`이 실행되기 위한 `Condition` 목록입니다.
*   **`actions` (필수)**: `conditions`가 충족되면 실행될 `Action` 목록입니다.

---

### 단계 2: `const.py` 업데이트

새로운 장면 ID나 키워드 ID가 필요하다면 `const.py` 파일에 `SceneID` 또는 `KeywordId` Enum을 업데이트해야 합니다.

**예시: `const.py`**

```python
from enum import StrEnum

class SceneID(StrEnum):
    CH0_SCENE0 = "ch0scene0"
    CH0_SCENE1 = "ch0scene1"
    CH0_SCENE2 = "ch0scene2"
    CH1_SCENE0 = "ch1scene0" # 새로 추가된 장면 ID

class KeywordId(StrEnum):
    # Common
    PROFESSOR = "교수님"
    CORP_CARD = "법인카드"
    # ... 기존 키워드들 ...
    LIGHT_SWITCH = "전등 스위치" # 새로 추가된 키워드 ID
    OLD_KEY = "오래된 열쇠" # 새로 추가된 키워드 ID
    # ...
```

### 단계 3: `game.py` 업데이트

새로 정의한 장면 데이터를 게임이 인식하도록 `game.py` 파일의 `_create_and_register_scenes` 메서드에 등록해야 합니다.

1.  새로운 장면 데이터 파일을 `game.py` 상단에 임포트합니다.
2.  `factory.register_scene` 메서드를 사용하여 `SceneFactory`에 장면 데이터를 등록합니다.

**예시: `game.py`**

```python
# ... (기존 임포트) ...

# 데이터 파일 임포트
from story.chapter0 import CH0_SCENE0_DATA, CH0_SCENE1_DATA, CH0_SCENE2_DATA
from story.chapter1 import CH1_SCENE0_DATA # 새로 추가된 장면 데이터 임포트

# ... (Game 클래스 정의) ...

    def _create_and_register_scenes(self) -> SceneFactory:
        factory = SceneFactory(self, self.ui, self.inventory)

        factory.register_scene(SceneID.CH0_SCENE0, Scene, CH0_SCENE0_DATA)
        factory.register_scene(SceneID.CH0_SCENE1, Scene, CH0_SCENE1_DATA)
        factory.register_scene(SceneID.CH0_SCENE2, Scene, CH0_SCENE2_DATA)
        factory.register_scene(SceneID.CH1_SCENE0, Scene, CH1_SCENE0_DATA) # 새로 추가된 장면 등록

        return factory

# ... (나머지 game.py 코드) ...
```

---

이 가이드를 통해 새로운 스토리 콘텐츠를 게임에 쉽게 추가할 수 있기를 바랍니다. 궁금한 점이 있다면 언제든지 문의해주세요!
