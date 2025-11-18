from pyscript import document


class Game:
    def __init__(self):
        self.location_info = document.getElementById("location-info")
        self.main_text_output = document.getElementById("main-text-output")
        self.puzzle_area = document.getElementById("puzzle-area")
        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")

        self.submit_button.onclick = self.handle_click
        self.user_input.onkeypress = self.handle_enter

        self.exec_globals = {}
        print("Game Initialized")

    # 클릭 이벤트 핸들러
    def handle_click(self, event):
        # 입력값 가져오기
        content = self.user_input.value.strip()

        if not content:
            return

        print(f"Button Clicked: {content}")
        self.process_command(content)  # 로직 처리 함수 호출

        # 입력창 비우기
        self.user_input.value = ""
        self.user_input.focus()

    # 엔터키 이벤트 핸들러
    def handle_enter(self, event):
        if event.key == "Enter":
            print(f"Enter Key Pressed Clicked")
            self.handle_click(event)

    def process_command(self, command):
        # 여기에 텍스트 출력 로직 등을 작성
        try:
            exec(command, self.exec_globals)
        except Exception as e:
            print(f"Error executing command: {e}")

        new_p = document.createElement("p")
        new_p.innerText = f"> {command}"
        self.main_text_output.appendChild(new_p)

        # 스크롤을 항상 최하단으로
        self.main_text_output.parentElement.scrollTop = self.main_text_output.parentElement.scrollHeight

    def game_start(self):
        self.bag = Bag()
        self.exec_globals['가방'] = self.bag


from contextlib import contextmanager


class LockAble:
    # 1. 모든 상속받은 클래스가 공유하는 단 하나의 스위치
    _global_lock = False

    @classmethod
    def set_lock(cls, status: bool):
        cls._global_lock = status

    @classmethod
    @contextmanager
    def safe_execution(cls):
        """exec 실행 중에만 잠그고, 끝나면 무조건 푸는 안전장치"""
        try:
            cls.set_lock(True)  # 잠금 ON
            yield
        finally:
            cls.set_lock(False)  # 잠금 OFF (에러가 나도 실행됨)

    def __getattribute__(self, name):
        # 2. 현재 잠금 상태인지 확인 (부모 클래스의 변수 확인)
        is_locked = object.__getattribute__(LockAble, '_global_lock')

        # 잠금 상태가 아니면 -> 통과
        if not is_locked:
            return object.__getattribute__(self, name)

        # 3. 잠금 상태일 때 허용할 화이트리스트
        allowed = ['__getitem__', '__repr__', '__str__']

        if name in allowed:
            return object.__getattribute__(self, name)

        # 그 외(__class__, __dir__, 내부 변수 등) 모두 차단
        raise AttributeError(f"[보안] '{type(self).__name__}' 객체의 '{name}' 속성은 잠겨있습니다.")


# --- 자식 클래스 정의 (LockAble 상속) ---

class Character(LockAble):
    def __init__(self, name, hp):
        self._data = {'name': name, 'hp': hp}

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f"<Character: {self._data['name']}>"


class Item(LockAble):
    def __init__(self, name, desc):
        self._data = {'name': name, 'desc': desc}

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f"<Item: {self._data['name']}>"


# --- 사용 예시 ---

# 1. 객체 생성 (평소에는 자유롭게 접근 가능)
hero = Character("어린왕자", 100)
sword = Item("장미칼", "아주 날카롭다")

print("=== 평상시 (관리자 모드) ===")
print(hero._data)  # 내부 데이터 접근 가능
print(hero.__class__)  # 클래스 정보 접근 가능
hero.new_attr = "test"  # 속성 추가 가능 (setattr은 막지 않았지만 getattribute가 막히면 확인 불가)

print("\n=== 사용자 코드 실행 (보안 모드) ===")

user_script = """
print(f"1. 영웅 확인: {hero}")          # [O] __repr__ 허용
print(f"2. 영웅 체력: {hero['hp']}")    # [O] __getitem__ 허용
print(f"3. 아이템: {sword}")            # [O] 다른 클래스도 허용

# 해킹 시도
try:
    print(hero.__class__)              # [X] 차단됨
except AttributeError as e:
    print(f"차단 성공: {e}")

try:
    print(sword._data)                 # [X] 차단됨
except AttributeError as e:
    print(f"차단 성공: {e}")
"""

# with 문을 사용하여 안전하게 실행
# 이 블록 안에서만 hero, sword 등 모든 LockAble 자식들이 잠김
with LockAble.safe_execution():
    exec(user_script, {'hero': hero, 'sword': sword})

print("\n=== 실행 종료 후 (다시 관리자 모드) ===")
print(hero.__class__)  # 다시 접근 가능
