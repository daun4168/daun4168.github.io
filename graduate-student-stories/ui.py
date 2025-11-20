from pyscript import document
import markdown

class UIManager:
    """DOM 조작 및 화면 출력을 전담하는 클래스."""

    def __init__(self):
        self.main_text_output = document.getElementById("main-text-output")
        self.location_display = document.getElementById("location")
        self.hp_display = document.getElementById("hp")
        self.keywords_display = document.getElementById("keywords")
        self.inventory_display = document.getElementById("inventory")

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

    def update_status(self, location: str, hp: int, keywords: list[str]):
        self.location_display.innerText = location
        self.hp_display.innerText = str(hp)
        self.keywords_display.innerHTML = ""
        for keyword in keywords:
            li = document.createElement("li")
            li.innerText = keyword
            self.keywords_display.appendChild(li)

    def update_inventory(self, items: list[str]):
        self.inventory_display.innerHTML = ""
        if not items:
            li = document.createElement("li")
            li.innerText = "비어 있음"
            self.inventory_display.appendChild(li)
        else:
            for item_name in items:
                li = document.createElement("li")
                li.innerText = item_name
                self.inventory_display.appendChild(li)

    def clear_output(self):
        self.main_text_output.innerHTML = ""

    def scroll_to_bottom(self):
        scroll_area = document.getElementById("content-scroll-area")
        scroll_area.scrollTop = scroll_area.scrollHeight
