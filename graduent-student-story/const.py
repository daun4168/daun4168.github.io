from enum import StrEnum


class SceneID(StrEnum):
    CH0_SCENE0 = "ch0_scene0"
    CH0_SCENE1 = "ch0_scene1"
    CH0_SCENE2 = "ch0_scene2"
    CH1_SCENE0 = "ch1_scene0"  # Chapter 1 Intro
    CH1_SCENE1 = "ch1_scene1"  # Chapter 1 Main


class KeywordId(StrEnum):
    # Common
    PROFESSOR = "교수님"
    CORP_CARD = "법인카드"
    SPANNER = "스패너"
    DOOR = "문"

    # Scene 0
    THESIS = "논문"
    DESK = "책상"
    GLASSES = "안경알"

    # Scene 1
    TRASH_CAN = "쓰레기통"
    BOX = "박스"
    BROOM = "빗자루"
    OLD_COMPUTER = "오래된 컴퓨터"
    COMPUTER_ALIAS = "컴퓨터"
    MYSTERY_LIQUID = "의문의 액체"
    CABINET = "시약장"
    FLOOR = "바닥"
    WALL = "벽"
    WALL_ALIAS = "벽면"
    MEMO = "메모"
    WRAPPER = "에너지바 껍질"
    LAB_COAT = "실험용 랩 가운"
    ETHANOL = "에탄올"

    # Scene 2
    MK_II = "MK-II"
    WIRE = "전선"
    OUTLET = "콘센트"
    HATCH = "탑승구"

    # Chapter 1
    COMMS = "통신기"
    SEA = "바다"
    SUN = "태양"
    SKY = "하늘"
    SAND = "모래"
    SANDY_BEACH = "모래사장"


class KeywordState(StrEnum):
    HIDDEN = "hidden"
    DISCOVERED = "discovered"
    INACTIVE = "inactive"
    NORMAL = "normal"


class ConditionType(StrEnum):
    HAS_ITEM = "has_item"
    NOT_HAS_ITEM = "not_has_item"
    STATE_IS = "state_is"
    STATE_NOT = "state_not"
    STAMINA_MIN = "stamina_min"


class ActionType(StrEnum):
    PRINT_NARRATIVE = "print_narrative"
    PRINT_SYSTEM = "print_system"
    ADD_ITEM = "add_item"
    REMOVE_ITEM = "remove_item"
    MOVE_SCENE = "move_scene"
    REMOVE_KEYWORD = "remove_keyword"
    UPDATE_STATE = "update_state"
    GAME_END = "game_end"
    MODIFY_STAMINA = "modify_stamina"
    SAVE_CHECKPOINT = "save_checkpoint"
    RELOAD_CHECKPOINT = "reload_checkpoint"
    SHOW_STAMINA_UI = "show_stamina_ui"  # [추가] 체력 UI 표시 여부 토글


class KeywordType(StrEnum):
    ITEM = "Item"
    OBJECT = "Object"
    NPC = "NPC"
    ALIAS = "Alias"
    PORTAL = "Portal"


# 명령어 관리용 Enum
class CommandType(StrEnum):
    INVENTORY = "주머니"
    WAKE_UP = "일어나기"
    LOOK_AROUND = "둘러보기"


# 조합의 성격을 구분하는 Enum
class CombinationType(StrEnum):
    DEFAULT = "default"  # 일반 아이템 조합 (+)
    PASSWORD = "password"  # 비밀번호 입력 (:)
