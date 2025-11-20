import markdown

# const에서 Enum 임포트 (타입 비교용)
from const import KeywordState, KeywordType
from pyscript import document


def get_josa(word: str, josa_pair: str) -> str:
    particles = josa_pair.split("/")
    if len(particles) != 2:
        return ""
    last_char = word[-1]
    if "가" <= last_char <= "힣":
        has_jongseong = (ord(last_char) - 0xAC00) % 28 != 0
        return particles[0] if has_jongseong else particles[1]
    else:
        return particles[1]


class UIManager:
    def __init__(self):
        self.main_text_output = document.getElementById("main-text-output")
        self.inventory_status = document.getElementById("inventory-status")
        self.location_name = document.getElementById("location-name")
        self.sight_status = document.getElementById("sight-status")

    def set_location_name(self, name: str):
        self.location_name.innerText = f"지역: {name}" if name else ""

    def update_sight_status(self, keywords: dict):
        """
        keywords: Dict[str, KeywordData] 형태의 Pydantic 모델 딕셔너리를 받습니다.
        """
        if not keywords:
            self.sight_status.innerText = "시야: "
            return

        display_list = []
        for name, data in keywords.items():
            # Pydantic 모델 속성 접근 (.type, .state)
            if data.type == KeywordType.ALIAS:
                continue

            state = data.state
            if state == KeywordState.DISCOVERED:
                # display_name이 없으면(None) name을 사용
                display_name = data.display_name if data.display_name else name
                display_list.append(f"[{display_name}]")
            elif state == KeywordState.HIDDEN:
                display_list.append("[?]")

        self.sight_status.innerText = f"시야: {', '.join(display_list)}"

    def update_inventory_status(self, items: dict):
        if not items:
            display_list = ["비어있음"]
        else:
            display_list = [f"[{item.name}]" for item in items.values()]

        self.inventory_status.innerText = f"주머니: {', '.join(display_list)}"

    def _create_text_element(self, parent, text: str, classes: list, is_markdown: bool = False):
        p = document.createElement("p")
        for cls in classes:
            p.classList.add(cls)
        p.innerHTML = markdown.markdown(text) if is_markdown else text
        parent.appendChild(p)
        self.scroll_to_bottom()

    def print_user_log(self, text: str):
        self._create_text_element(self.main_text_output, text, ["user-input-log"])

    def print_system_message(self, text: str, is_markdown: bool = True):
        self._create_text_element(self.main_text_output, text, ["system-message"], is_markdown=is_markdown)

    def print_narrative(self, text: str, is_markdown: bool = True):
        self._create_text_element(self.main_text_output, text, ["narrative-text"], is_markdown=is_markdown)

    def scroll_to_bottom(self):
        scroll_area = document.getElementById("content-scroll-area")
        scroll_area.scrollTop = scroll_area.scrollHeight
