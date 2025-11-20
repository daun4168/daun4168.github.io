# const.py (업데이트)


class SceneID:
    CH0_SCENE0 = "ch0scene0"
    CH0_SCENE1 = "ch0scene1"
    CH0_SCENE2 = "ch0scene2"


class KeywordId:
    # Common
    PROFESSOR = "교수님"
    CORP_CARD = "법인카드"
    SPANNER = "스패너"

    # Scene 0
    DOOR_0 = "문"
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

    # Scene 2 (New)
    MK_II = "MK-II"
    WIRE = "전선"
    OUTLET = "콘센트"
    HATCH = "탑승구"


class KeywordState:
    HIDDEN = "hidden"
    DISCOVERED = "discovered"


class ConditionType:
    HAS_ITEM = "has_item"
    NOT_HAS_ITEM = "not_has_item"
    STATE_IS = "state_is"
    STATE_NOT = "state_not"


class ActionType:
    PRINT_NARRATIVE = "print_narrative"
    PRINT_SYSTEM = "print_system"
    ADD_ITEM = "add_item"
    REMOVE_ITEM = "remove_item"
    MOVE_SCENE = "move_scene"
    REMOVE_KEYWORD = "remove_keyword"
    UPDATE_STATE = "update_state"
    GAME_END = "game_end"  # 게임 엔딩 처리용


class KeywordType:
    ITEM = "Item"
    OBJECT = "Object"
    NPC = "NPC"
    ALIAS = "Alias"
    PORTAL = "Portal"
