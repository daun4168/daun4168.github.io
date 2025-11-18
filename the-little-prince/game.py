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
