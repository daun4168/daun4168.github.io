from pyscript import document
import markdown


class UIManager:
    """
    DOM 조작 및 화면 출력을 전담하는 클래스.
    텍스트 박스 생성, 스타일 적용, 스크롤 관리 등을 수행합니다.
    """
    def __init__(self):
        # 필수 DOM 요소 참조
        self.main_text_output = document.getElementById("main-text-output")
        self.puzzle_area = document.getElementById("puzzle-area")
        self.inventory_status = document.getElementById("inventory-status")
        self.location_name = document.getElementById("location-name")
        self.hr_divider = document.querySelector("#main-text-output + hr")

    def set_location_name(self, name: str):
        """현재 위치 이름을 설정합니다."""
        self.location_name.innerText = f"현재 위치: {name}"

    def show_hr_divider(self):
        """구분선을 표시합니다."""
        self.hr_divider.style.display = "block"

    def _create_text_element(self, parent, text: str, classes: list, is_markdown: bool = False):
        """공통 텍스트 요소 생성 및 추가 로직"""
        p = document.createElement("p")
        for cls in classes:
            p.classList.add(cls)

        if is_markdown:
            html_content = markdown.markdown(text)
            p.innerHTML = html_content
        else:
            p.innerText = text
        
        parent.appendChild(p)
        self.scroll_to_bottom()
        return p

    def print_user_log(self, text: str):
        """사용자 입력 로그 출력 (> 명령)"""
        self._create_text_element(self.main_text_output, f"{text}", ["user-input-log"])

    def print_system_message(self, text: str, is_markdown: bool = True):
        """시스템 메시지 출력 (기능적 피드백)"""
        self._create_text_element(self.main_text_output, text, ["system-message"], is_markdown=is_markdown)

    def print_narrative(self, text: str, is_markdown: bool = True):
        """스토리/내러티브 텍스트 출력"""
        self._create_text_element(self.main_text_output, text, ["narrative-text"], is_markdown=is_markdown)

    def create_puzzle(self, title: str, hint: str, content: str):
        """수수께끼 영역을 동적으로 생성합니다."""
        self.puzzle_area.innerHTML = ""

        h3 = document.createElement("h3")
        h3.classList.add("puzzle-title")
        h3.innerHTML = markdown.markdown(title)
        self.puzzle_area.appendChild(h3)

        self._create_text_element(self.puzzle_area, hint, ["puzzle-hint"], is_markdown=True)

        content_div = document.createElement("div")
        content_div.id = "puzzle-content"
        content_div.innerHTML = content
        self.puzzle_area.appendChild(content_div)
        
        self.scroll_to_bottom()

    def update_inventory_ui(self, items_dict: dict):
        """상단 인벤토리 표시줄 업데이트"""
        item_list = ', '.join(items_dict.keys())
        text = f"인벤토리: {item_list if item_list else '비어 있음'}"
        self.inventory_status.innerText = text

    def scroll_to_bottom(self):
        """스크롤을 최하단으로 이동"""
        scroll_area = document.getElementById("content-scroll-area")
        scroll_area.scrollTop = scroll_area.scrollHeight
