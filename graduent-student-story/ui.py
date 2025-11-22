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
        # [추가] 체력 UI 바인딩
        self.stamina_status = document.getElementById("stamina-status")

    def set_location_name(self, name: str):
        self.location_name.innerText = f"지역: {name}" if name else ""

    def update_stamina_status(self, current: int, maximum: int):
        """체력 상태 UI를 업데이트합니다."""
        if self.stamina_status:
            self.stamina_status.innerText = f"체력: {current} / {maximum}"

            # 체력이 30% 이하일 때 붉은색으로 경고 표시
            if current <= (maximum * 0.3):
                self.stamina_status.style.color = "#ff6b6b"  # 밝은 붉은색
                self.stamina_status.style.fontWeight = "bold"
            else:
                self.stamina_status.style.color = "rgba(255, 255, 255, 0.9)"  # 기본색 복구
                self.stamina_status.style.fontWeight = "400"

    def toggle_stamina_ui(self, show: bool):
        """체력 UI의 표시 여부를 결정합니다."""
        if self.stamina_status:
            self.stamina_status.style.display = "block" if show else "none"

    def update_sight_status(self, keywords: dict):
        if not keywords:
            self.sight_status.innerText = "시야: "
            return

        display_list = []
        for name, data in keywords.items():
            if data.type == KeywordType.ALIAS:
                continue

            state = data.state
            if state == KeywordState.DISCOVERED:
                display_name = data.display_name if data.display_name else name
                display_list.append(f"[{display_name}]")
            elif state == KeywordState.HIDDEN:
                display_list.append("[?]")

        self.sight_status.innerText = f"시야: {', '.join(display_list)}"

    def update_inventory_status(self, items: dict):
        if not items:
            display_list = ["비어있음"]
        else:
            display_list = [f"[{item}]" for item in items.values()]

        self.inventory_status.innerText = f"주머니: {', '.join(display_list)}"

    def _create_text_element(self, parent, text: str, classes: list, is_markdown: bool = False):
        p = document.createElement("p")
        for cls in classes:
            p.classList.add(cls)
        p.innerHTML = markdown.markdown(text, extensions=["tables", "fenced_code"]) if is_markdown else text
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
