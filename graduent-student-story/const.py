from enum import StrEnum


class ChapterID(StrEnum):
    CH0 = "ch0"
    CH1 = "ch1"


class SceneID(StrEnum):
    CH0_SCENE0 = "ch0_scene0"
    CH0_SCENE1 = "ch0_scene1"
    CH0_SCENE2 = "ch0_scene2"

    CH1_SCENE0 = "ch1_scene0"
    CH1_SCENE1 = "ch1_scene1"  # 베이스캠프
    CH1_SCENE2 = "ch1_scene2"  # 난파선
    CH1_SCENE3 = "ch1_scene3"  # 난파선 내부
    CH1_SCENE4 = "ch1_scene4"  # 공명하는 숲 (생태 관측소)
    CH1_SCENE5 = "ch1_scene5"  # 늪지대
    CH1_SCENE6 = "ch1_scene6"  # 동굴
    CH1_SCENE7 = "ch1_scene7"
    CH1_SCENE8 = "ch1_scene8"
    CH1_SCENE9 = "ch1_scene9"
    CH1_SCENE10 = "ch1_scene10"


class KeywordId(StrEnum):
    # --- CH0_SCENE0 ---
    PROFESSOR = "교수님"
    CORP_CARD = "법인카드"
    DOOR = "문"
    # -- UNSEEN --
    THESIS = "논문"
    DESK = "책상"
    GLASSES = "안경알"
    POINT = "포인트"
    SAUNA = "사우나"
    CLEANING = "청소"
    GUEST = "손님"
    ME = "나"

    # CH0_SCENE1
    SPANNER = "스패너"
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
    AIR_DUSTER = "먼지 제거제"
    LAB_COAT = "실험용 랩 가운"
    ETHANOL = "에탄올"
    KEY = "열쇠"
    CLEANING_CABINET = "청소도구함"

    # CH0_SCENE2
    MK_II = "MK-II"
    WIRE = "전선"
    OUTLET = "콘센트"
    HATCH = "탑승구"

    # CH1_SCENE0
    COMMS = "통신기"
    SEA = "바다"
    SUN = "태양"
    SKY = "하늘"
    SAND = "모래"
    SANDY_BEACH = "모래사장"

    # CH1_SCENE1
    WRECKAGE = "난파선 잔해"
    FOREST_ENTRY = "숲 입구"
    SHADE = "그늘막"
    PALM_TREE = "야자수"
    TRASH_PILE = "쓰레기 더미"
    COCONUT = "코코넛"
    PLASTIC_BOTTLE = "빈 페트병"
    VINYL = "비닐"

    # CH1_SCENE2
    RUSTY_BUCKET = "녹슨 양동이"
    BEACH = "해변"
    BASECAMP = "베이스캠프"
    EMERGENCY_CABINET = "비상 캐비닛"  # 조명탄 파밍 장소
    FLARE = "조명탄"  # 가열 아이템
    IRON_DOOR = "강화 격벽"  # 메인 퍼즐 장애물
    BULKHEAD = "격벽"  # 메인 퍼즐 장애물
    UNDERGROUND_PASSAGE = "지하 통로"  # 문 열면 등장
    WARNING_SIGN = "경고문"
    PIPE = "파이프"
    FLOOR_WIRES = "전선"  # 바닥에 널린 전선들 (아이템 아님)

    # --- [Scene 3: 화물칸 (위험물 적재소)] ---
    # 1. 지역 및 이동
    SHIPWRECK_ENTRANCE = "난파선 입구"

    # 2. 환경 오브젝트 & Alias
    ACID_PUDDLE = "산성 웅덩이"
    ACID_PUDDLE_ALIAS = "웅덩이"
    WHITE_POWDER = "하얀 가루"
    WHITE_POWDER_ALIAS = "가루"
    WORKBENCH = "작업대"
    MULTIMETER = "멀티미터"
    SAFE = "전자 금고"
    SAFE_ALIAS = "금고"
    RUSTY_CLAMP = "녹슨 클램프"
    RUSTY_CLAMP_ALIAS = "클램프"
    MEMO_VOLTAGE = "정비 메모"
    SCATTERED_SUPPLIES = "흩어진 보급품"
    SCATTERED_SUPPLIES_ALIAS = "보급품"
    PERIODIC_TABLE = "주기율표"
    NOTE = "쪽지"
    PUZZLE_NOTE = "수수께끼 쪽지"

    # 3. 아이템
    EMPTY_BOTTLE = "빈 페트병"
    STARCH = "전분 가루"

    CAUSTIC_SODA_BUCKET = "가성소다 양동이"
    ACID_BOTTLE = "산성 용액 병"
    ACID_GEL = "산성 젤"

    # 4. 배터리 관련
    BATTERY_CASE = "배터리 케이스"
    BATTERY_PACK = "배터리 팩"

    # 미확인 건전지 (ID는 하나로 유지)
    BATTERY_1 = "건전지 1"
    BATTERY_2 = "건전지 2"
    BATTERY_3 = "건전지 3"
    BATTERY_4 = "건전지 4"
    BATTERY_5 = "건전지 5"

    # 5. 최종 보상
    FIRE_AXE = "소방 도끼"
    HEAVY_BATTERY = "산업용 배터리"

    # CH1_SCENE4: 공명하는 숲 (생태 관측소)
    ECO_OBSERVATORY = "생태 관측소"
    OBSERVATORY_INSIDE = "관측소 내부"
    VINE = "덩굴"
    VINE_STEM = "덩굴 줄기"
    BOTANIST_MURAL = "벽화"
    FLOWER_BED = "화단"
    BOTANY_NOTE = "관찰 일지"
    LAB_DOOR = "관측소 문"
    SUPPLY_LOCKER = "보급품 로커"
    MICROPHONE = "마이크"
    LONG_PIPE = "긴 파이프"
    SHORT_PIPE = "짧은 파이프"
    TREE = "나무"

    SWAMP_PATH = "늪지대로 가는 길"
    SWAMP_PATH_ALIAS = "늪지대"
    VINEGAR = "식초"
    VINEGAR_HALF = "반쯤 남은 식초"
    WATERPROOF_TAPE = "방수 테이프"

    # 준비용 재료/장비
    LATEX = "라텍스"
    RUBBER = "고무"
    RESIN = "송진"
    INSULATED_WIRE = "절연 전선"
    WATERPROOF_BOOTS = "방수 부츠"
    RUBBER_TREE = "고무나무"
    COATED_COCONUT_SHELL = "코팅된 코코넛 껍질"
    INSULATED_COPPER_WIRE = "절연 구리선"

    # CH1_SCENE5 - 늪지대
    SWAMP_TRASH = "늪 쓰레기 더미"
    SWAMP_WATER = "늪물"
    GIANT_CROCODILE = "거대한 악어"
    BROKEN_BRIDGE = "끊어진 다리"
    GAS_BUCKET = "독가스 양동이"
    FLOATING_BAG = "부력 주머니"
    FLOATING_DEVICE = "부력 장치"

    WATER_BUCKET = "늪물 담은 양동이"
    CHLORINE_BUCKET = "염소 양동이"
    CHLORINE_AGENT = "염소 소독제"  # 늪 쓰레기 더미에서 줍는 염소 기반 소독제

    # CH1_SCENE5 - 늪지대 alias 키워드
    SWAMP_TRASH_ALIAS = "쓰레기 더미"
    SWAMP_WATER_ALIAS = "늪"
    GIANT_CROCODILE_ALIAS = "악어"
    BROKEN_BRIDGE_ALIAS = "다리"

    CAVE_ENTRANCE = "동굴 입구"
    CAVE = "동굴"

    # ---- Scene 6: 석회 동굴 (수정 동굴) ----
    CAVE_HALL = "동굴 홀"

    # 그림자 시계 퍼즐용 돌 3개
    SHORT_STONE = "짧은 돌"
    MID_STONE = "중간 돌"
    LONG_STONE = "긴 돌"

    # 시계 모양 석회문
    TIME_DOOR = "석회문"

    # 위쪽 절벽 / 아래쪽 지하 호수로 가는 통로
    CLIFF_PATH = "절벽 길"
    UNDERGROUND_LAKE_PATH = "지하 호수 통로"

    # 석회 패널(2진수 퍼즐)
    LIME_PANEL = "석회 패널"
    LIME_DOT_1 = "석회 패널 1번 점"
    LIME_DOT_2 = "석회 패널 2번 점"
    LIME_DOT_3 = "석회 패널 3번 점"
    LIME_DOT_4 = "석회 패널 4번 점"
    LIME_DOT_5 = "석회 패널 5번 점"
    LIME_CONFIRM = "석회 패널 래버"

    # 지하 샘 / 석영 군집 및 아이템
    UNDERGROUND_SPRING = "지하 샘"
    COLD_GROUNDWATER = "차가운 지하수"

    QUARTZ_CLUSTER = "석영 군집"
    QUARTZ_SHARD = "석영 조각"

    GROWTH_PATTERN = "이상한 무늬"
    GROWTH_INSCRIPTION = "짧은 글귀"
    GROWTH_PATTERN_ALIAS = "무늬"
    GROWTH_INSCRIPTION_ALIAS = "글귀"

    # 7
    UNDERGROUND_LAKE = "지하 호수"
    UNDERGROUND_LAKE_ALIAS = "호수"
    WATERFALL = "폭포"
    WATERFALL_ALIAS = "물폭포"
    LAKE_SHORE = "호숫가"
    STONE_RING = "바위 고리"
    MAGNETIC_ROCK = "검은 바위"
    MAGNETIC_ROCK_ALIAS2 = "검은 바위 덩어리"
    MAGNETIC_ROCK_ALIAS3 = "바위 덩어리"
    LAKE_BACK_TUNNEL = "경사로"

    MAGNETITE_CHUNK = "자철석 조각"
    COPPER_WIRE = "구리선"
    COCONUT_SHELL = "코코넛 껍질"
    MAKESHIFT_ROTOR = "임시 수차 로터"
    DYNAMO_CORE = "발전 코어"
    WOODEN_SHAFT = "나무 축"  # 호숫가에서 줍는 회전축
    SHAFTED_ROTOR = "축 달린 수차"  # 수차 로터 + 나무 축
    MOUNTED_ROTOR = "고리에 끼운 수차"  # 바위 고리에 끼운 수차
    HYDRO_DYNAMO_MODULE = "수력 발전 모듈"
    HYDRO_GENERATOR = "수력 발전기"
    CHARGED_HEAVY_BATTERY = "충전된 산업용 배터리"

    # 8
    CLIFF_FACE = "절벽"
    CLIFF_BACK_PATH = "석회 동굴"
    PULLEY_ANCHOR = "바위 턱"
    STONE_PILE = "돌무더기"

    EQUIPMENT_BUNDLE = "장비 상자"
    CLIMBING_ROPE = "등반용 로프"
    PULLEY_WHEEL = "도르래 바퀴"
    CARGO_NET = "그물 바구니"

    WEATHER_CRATE = "관측 장비 상자"
    ASCENT_CRATE = "등반 장비 상자"  # 상자 3 (도르래 재료 상자)

    # 풍향계 재료
    METAL_PIPE = "금속 파이프 뭉치"
    ROTATION_BRACKET = "회전 브래킷"
    ALUMINUM_PLATE = "알루미늄 판"
    PLASTIC_ROD = "플라스틱 막대"
    BOLT_SET = "볼트 세트"

    # 풍향계 제작 중간품/완성품
    TRIMMED_TAIL_PLATE = "다듬은 꼬리판"
    ARROW_HEAD = "화살 헤드"
    WIND_VANE_WINGS = "풍향계 날개"
    WIND_VANE_POLE = "풍향계 기둥"
    TIGHTENED_PIVOT = "조여진 회전축"
    PIVOT_POLE_SET = "회전 기둥 세트"
    WIND_VANE = "풍향계"

    # 도르래 재료
    LARGE_PULLEY = "큰 도르래"
    SMALL_PULLEY = "작은 도르래"
    HARNESS = "하네스"

    # 도르래 중간품
    ROPE_TIP_CUT = "정리된 로프 끝"
    HARNESS_SET = "하네스 세트"
    MOUNTABLE_PULLEY = "설치용 큰 도르래"

    # 무게추 (돌 1~5)
    STONE_1 = "돌 1"
    STONE_2 = "돌 2"
    STONE_3 = "돌 3"
    STONE_4 = "돌 4"
    STONE_5 = "돌 5"

    # 풍향 측정용 오브젝트 (절벽 바람)
    CLIFF_WIND = "바람"

    EQUIPMENT_NAMEPLATE = "장비 상자 명판"
    BROKEN_FEATURE_PHONE = "고장난 피쳐폰"

    # 9
    ANTENNA_MOUNT = "콘크리트 기단"
    LONG_WIRE = "기다란 전선"
    LONG_WIRE_FREE_END = "기다란 전선 끝"
    WIRE_CRATE = "전선 상자"
    WIRE_CRATE_ALIAS1 = "상자"
    WIRE_CRATE_ALIAS2 = "금속 상자"
    ANTENNA = "안테나"

    LAB_ROOM = "연구실"  # 연구실 전체
    LAB_DESK = "책상"  # 연구실 책상/작업대
    ENDING_NOTE = "수상한 메모"  # 엔딩 떡밥 메모


class KeywordState(StrEnum):
    HIDDEN = "hidden"
    DISCOVERED = "discovered"
    INACTIVE = "inactive"
    UNSEEN = "unseen"


class ConditionType(StrEnum):
    HAS_ITEM = "has_item"
    NOT_HAS_ITEM = "not_has_item"
    STATE_IS = "state_is"
    STATE_NOT = "state_not"
    STAMINA_MIN = "stamina_min"
    STONE_PUZZLE = "stone_puzzle"


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
    REQUEST_CONFIRMATION = "request_confirmation"  # [추가] 확인 요청 액션
    UPDATE_KEYWORD_DATA = "update_keyword_data"
    UPDATE_ITEM_DATA = "update_item_data"


class KeywordType(StrEnum):
    ITEM = "Item"
    OBJECT = "Object"
    NPC = "NPC"
    ALIAS = "Alias"
    PORTAL = "Portal"


# 명령어 관리용 Enum
class CommandType(StrEnum):
    WAKE_UP = "일어나기"
    LOOK_AROUND = "둘러보기"


# 조합의 성격을 구분하는 Enum
class CombinationType(StrEnum):
    DEFAULT = "default"  # 일반 아이템 조합 (+)
    PASSWORD = "password"  # 비밀번호 입력 (:)
    PASSWORD_CH1_FINAL = "password_ch1_final"  # 비밀번호 입력 (:)
