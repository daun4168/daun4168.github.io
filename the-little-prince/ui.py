from pyscript import document
import markdown


def get_josa(word: str, josa_pair: str) -> str:
    """
    한글 단어의 마지막 글자 받침 유무에 따라 적절한 조사를 선택하여 반환합니다.
    """
    particles = josa_pair.split('/')
    if len(particles) != 2: return ""
    last_char = word[-1]
    if '가' <= last_char <= '힣':
        has_jongseong = (ord(last_char) - 0xAC00) % 28 != 0
        return particles[0] if has_jongseong else particles[1]
    else:
        return particles[1]


class UIManager:
    """DOM 조작 및 화면 출력을 전담하는 클래스."""

    def __init__(self):
        self.main_text_output = document.getElementById("main-text-output")
        self.bag_status = document.getElementById("bag-status")
        self.location_name = document.getElementById("location-name")
        self.hr_divider = document.querySelector("#main-text-output + hr")

    def set_initial_bag_status(self):
        self.bag_status.innerText = "가방: ???"

    def set_location_name(self, name: str):
        self.location_name.innerText = f"현재 위치: {name}"

    def show_hr_divider(self):
        self.hr_divider.style.display = "block"

    def _create_text_element(self, parent, text: str, classes: list, is_markdown: bool = False):
        p = document.createElement("p")
        for cls in classes: p.classList.add(cls)
        p.innerHTML = markdown.markdown(text) if is_markdown else text
        parent.appendChild(p)
        self.scroll_to_bottom()

    def print_user_log(self, text: str):
        self._create_text_element(self.main_text_output, text, ["user-input-log"])

    def print_system_message(self, text: str, is_markdown: bool = True):
        self._create_text_element(self.main_text_output, text, ["system-message"], is_markdown=is_markdown)

    def print_narrative(self, text: str, is_markdown: bool = True):
        self._create_text_element(self.main_text_output, text, ["narrative-text"], is_markdown=is_markdown)

    def create_puzzle(self, title: str, hint: str, content: str):
        """메인 출력 영역에 수수께끼 스타일의 블록을 생성합니다."""
        puzzle_container = document.createElement("div")
        puzzle_container.classList.add("puzzle-container")

        h3 = document.createElement("h3")
        h3.classList.add("puzzle-title")
        h3.innerHTML = markdown.markdown(title)
        puzzle_container.appendChild(h3)

        hint_p = document.createElement("p")
        hint_p.classList.add("puzzle-hint")
        hint_p.innerHTML = markdown.markdown(hint)
        puzzle_container.appendChild(hint_p)

        content_div = document.createElement("div")
        content_div.id = "puzzle-content"
        content_div.innerHTML = markdown.markdown(content)
        puzzle_container.appendChild(content_div)
        
        self.main_text_output.appendChild(puzzle_container)
        self.scroll_to_bottom()

    def update_bag_status(self, items: dict):
        """상단 가방 상태 표시줄을 아이템의 단축어로 업데이트합니다."""
        if not items:
            display_list = ["비어 있음"]
        else:
            display_list = []
            for item in items.values():
                display_name = item.aliases[0] if item.aliases else item.name
                display_list.append(display_name)
        
        text = f"가방: {', '.join(display_list)}"
        self.bag_status.innerText = text

    def scroll_to_bottom(self):
        scroll_area = document.getElementById("content-scroll-area")
        scroll_area.scrollTop = scroll_area.scrollHeight
