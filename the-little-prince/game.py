import re
from pyscript import document
from ui import UIManager, get_josa
from entity import Entity, Item, Bag

# --- 상수 정의 ---
CMD_LOOK_AROUND = "둘러보기"
CMD_EXAMINE = ["조사", "보기"]
CMD_BAG = ["가방"]
CMD_COMBINE = "조합"
CMD_USE = ["사용", "사용하기"]
CMD_ANSWER = ["정답"]
CMD_DIAL = ["다이얼"]
CMD_START = "시작"

INITIAL_ITEM_DATA = {
    "연필": ("평범한 연필입니다.", []),
    "돋보기": ("작은 것들을 관찰할 수 있는 돋보기입니다.", []),
    "깨진 거울 조각": ("빛을 반사하는 날카로운 조각입니다.", ["거울"]),
}

DIARY_RIDDLES = [
    {"id": "diary_1", "title": "첫 번째 페이지: 어른들의 세상", "hint": "어릴 적, 나는 코끼리를 삼킨 보아뱀을 그렸다. 하지만 어른들은 그저 OO라고 말했다.", "content": "<img src='assets/boa_hat.png' alt='코끼리를 삼킨 보아뱀 그림' style='max-width: 300px; display: block; margin: 1rem auto;'>", "answer": "모자"},
    {"id": "diary_2", "title": "두 번째 페이지: 사막의 목소리", "hint": "나는 입이 없지만 소리를 따라 하고, 몸이 없지만 골짜기를 채운다. 나는 무엇일까?", "content": "[소리가 울려퍼지는 사막 협곡 그림]", "answer": "메아리"},
    {"id": "diary_3", "title": "마지막 페이지: 밤의 보석", "hint": "밤이 되면 수억 개의 내가 떠오르지만, 그 누구도 나를 가질 수는 없다. 나는 무엇일까?", "content": "[별이 가득한 사막의 밤하늘 그림]", "answer": "별"}
]


class Game:
    """게임의 핵심 로직, 이벤트 핸들러, 명령어 처리 및 상태 관리를 담당합니다."""

    def __init__(self):
        self.ui = UIManager()
        Entity.set_ui_manager(self.ui)

        self.user_input = document.getElementById("user-input")
        self.submit_button = document.getElementById("submit-button")
        self.user_input.onkeypress = self._handle_enter
        self.submit_button.onclick = self._handle_click

        self.bag = None
        self.game_started = False
        self.current_puzzle = None
        self.clues = {"tail_number": None, "diary_page": None, "volcanoes": None}
        
        self.has_checked_bag = False
        self.investigated_items = set()
        self.has_been_told_to_combine = False
        self.diary_riddles_solved = 0

        self.ui.print_narrative(
            "**어린 왕자: 사막의 별**\n\n"
            "눈을 뜨자 끝없는 모래 언덕이 펼쳐집니다.\n"
            "당신은 불시착한 비행기의 조종사입니다.\n\n"
            f"모험을 시작하려면 `{CMD_START}`을 입력하세요.",
            is_markdown=True
        )

    def _handle_click(self, event):
        content = self.user_input.value.strip()
        if not content: return
        self.process_command(content)
        self.user_input.value = ""
        self.user_input.focus()

    def _handle_enter(self, event):
        if event.key == "Enter": self._handle_click(event)

    def _parse_arguments(self, arg_string: str) -> list[str]:
        args = re.findall(r'"[^"]+"|\'[^\']+\'|\S+', arg_string)
        return [arg.strip("'\"") for arg in args]

    def process_command(self, command: str):
        self.ui.print_user_log(command)
        parts = command.strip().split()
        if not parts: return

        verb = parts[0].lower()
        arg_string = " ".join(parts[1:])
        args = self._parse_arguments(arg_string)

        if not self.game_started:
            if verb == CMD_START: self._start_game()
            else: self.ui.print_system_message(f"모험을 시작하려면 `{CMD_START}`을 입력하세요.")
            return

        if self.bag is None:
            if verb == CMD_LOOK_AROUND: self._acquire_bag()
            else: self.ui.print_system_message(f"무엇을 해야 할지 모르겠다. 우선 `{CMD_LOOK_AROUND}`로 주변을 살펴보자.")
            return

        if verb == CMD_COMBINE: self._combine_items(args)
        elif verb in CMD_BAG: self._check_bag()
        elif verb in CMD_EXAMINE: self._examine_item(args)
        elif verb in CMD_USE: self._use_item(args)
        elif verb in CMD_ANSWER: self._check_answer(arg_string)
        elif verb in CMD_DIAL: self._dial_combination(arg_string)
        elif verb == CMD_LOOK_AROUND: self.ui.print_system_message("이미 주변을 둘러보았다. 특별한 것은 보이지 않는다.")
        else:
            josa = get_josa(command, "은/는")
            self.ui.print_system_message(f"'{command}'{josa} 알 수 없는 명령어입니다.")

    def _start_game(self):
        self.game_started = True
        self.ui.set_location_name("사하라 사막")
        self.ui.show_hr_divider()
        self.ui.print_narrative("비행기가 사막에 불시착했다. 정신을 차려보니 주변은 고요하다. 비행기 꼬리에는 `B-612`라는 글자가 희미하게 보인다.", is_markdown=True)
        self.clues["tail_number"] = 6
        self.ui.print_system_message(f"우선 `{CMD_LOOK_AROUND}`로 주변을 살펴보자.")

    def _acquire_bag(self):
        self.ui.print_narrative("비행기 잔해 속을 뒤지자, 낡은 가죽 가방 하나를 발견했다.", is_markdown=True)
        self.bag = Bag()
        for name, (desc, aliases) in INITIAL_ITEM_DATA.items():
            self.bag.add(Item(name, desc, aliases), silent=True)
        
        self.ui.set_initial_bag_status()
        self.ui.print_system_message(f"상단에 가방 상태가 표시되었다. 이제 `{CMD_BAG[0]}`을 열어 내용물을 확인해보자.")

    def _check_bag(self):
        self.bag.show()
        if not self.has_checked_bag:
            self.ui.update_bag_status(self.bag.items)
            self.ui.print_system_message("상단 가방의 상태가 단축어로 업데이트 되었습니다.")
            self.ui.print_system_message(f"가방 안의 도구들을 `{CMD_EXAMINE[0]}` 명령어로 모두 살펴보자. 단축어를 사용해서 살펴볼 수 있다.")
            self.has_checked_bag = True

    def _examine_item(self, args: list[str]):
        if not args:
            self.ui.print_system_message(f"사용법: `{CMD_EXAMINE[0]} <아이템>`")
            return

        item_name = " ".join(args)
        item = self._find_item_in_bag(item_name)
        if not item:
            josa = get_josa(item_name, "은/는")
            self.ui.print_system_message(f"'{item_name}'{josa} 조사할 수 없는 대상입니다.")
            return
        
        if item.name == "낡은 일기장":
            self.ui.print_narrative(
                "일기장을 펼치자, 오래된 잉크 냄새와 함께 낡은 종이가 모습을 드러낸다.\n"
                "첫 페이지에는 무언가 그려져 있었던 것 같지만, 세월의 흔적인지 잉크가 번져 형체를 알아보기 어렵다.\n"
                "자세히 보니 희미하게 선들이 남아있다. 어쩌면... 연필로 빈 곳을 채우면 그림의 비밀을 풀 수 있을지도 모른다.",
                is_markdown=True
            )
            return
        
        if item.name == "수수께끼가 담긴 일기장":
            self._read_diary()
            return

        item.show()
        
        if item.name in INITIAL_ITEM_DATA:
            self.investigated_items.add(item.name)
            if len(self.investigated_items) == len(INITIAL_ITEM_DATA) and not self.has_been_told_to_combine:
                self.ui.print_system_message(f"이제 각 도구의 단축어를 알게 되었다. `{CMD_COMBINE}` 명령어로 도구들을 조합해보자.\n(예: `{CMD_COMBINE} 돋보기 거울`)")
                self.has_been_told_to_combine = True

    def _combine_items(self, args: list[str]):
        if len(args) != 2:
            self.ui.print_system_message(f"사용법: `{CMD_COMBINE} <아이템1> <아이템2>`\n(띄어쓰기가 포함된 이름은 따옴표로 감싸거나, 단축어를 사용하세요.)")
            return

        item_a = self._find_item_in_bag(args[0])
        item_b = self._find_item_in_bag(args[1])

        if not item_a or not item_b or item_a == item_b:
            self.ui.print_system_message("의미 있는 조합이 아니거나, 가방에 없는 물건입니다.")
            return
        
        self._try_crafting(item_a, item_b)

    def _is_target_tuple(self, key: list[str], target: list[str]) -> bool:
        if tuple(sorted(key)) == tuple(sorted(target)):
            return True
        return False
    
    def _try_crafting(self, item_a: Item, item_b: Item):
        keys = [item_a.name, item_b.name]
        if self._is_target_tuple(keys, ["돋보기", "깨진 거울 조각"]):
            self.bag.remove(item_a.name)
            self.bag.remove(item_b.name)
            
            new_item = Item("태양열 집광 장치", "강력한 열을 모을 수 있습니다. 무언가를 녹일 수 있을 것 같습니다.", ["집광기"])
            self.bag.add(new_item, silent=True)
            self.ui.update_bag_status(self.bag.items)
            
            self.ui.print_narrative("두 조각을 합쳐 **태양열 집광 장치**를 만들었습니다!", is_markdown=True)
            self.ui.print_system_message(f"'{new_item.name}'(단축어: `{new_item.aliases[0]}`)를 가방에 추가했습니다.")

            self.current_puzzle = "rusty_pin"
            self.ui.create_puzzle("수수께끼: 비행기 잔해", "비행기 동체에 무언가를 고정했던 것으로 보이는 **녹슨 핀**이 박혀있다. 손으로는 뽑을 수 없다.", f"방금 만든 도구를 `{CMD_USE[0]}` 명령어로 사용해볼 수 있을 것 같다.\n(예: `{CMD_USE[0]} 집광기 녹슨핀`)")
        elif self._is_target_tuple(keys, ["연필", "낡은 일기장"]):
            self.bag.remove(item_a.name)
            self.bag.remove(item_b.name)
            
            new_item = Item("수수께끼가 담긴 일기장", "연필로 그림의 윤곽을 채우자 희미한 글자들이 드러났다.", ["일기"])
            self.bag.add(new_item, silent=True)
            self.ui.update_bag_status(self.bag.items)
            
            self.ui.print_narrative("연필로 일기장의 빈 곳을 칠하자, 숨겨져 있던 글자들이 드러나기 시작했다!", is_markdown=True)
            self.ui.print_system_message(f"**수수께끼가 담긴 일기장** (단축어: `일기`)을 얻었다. `{CMD_EXAMINE[0]} 일기`로 내용을 확인해보자.")
        else:
            self.ui.print_system_message("두 아이템을 조합했지만 아무 일도 일어나지 않았습니다.")

    def _use_item(self, args: list[str]):
        if len(args) != 2:
            self.ui.print_system_message(f"사용법: `{CMD_USE[0]} <도구> <대상>`")
            return
        
        tool_name, target_name = args[0], args[1]
        tool = self._find_item_in_bag(tool_name)
        if not tool:
            self.ui.print_system_message(f"'{tool_name}'{get_josa(tool_name, '은/는')} 가방에 없는 도구입니다.")
            return

        if self.current_puzzle == "rusty_pin" and tool.name == "태양열 집광 장치" and target_name in ["녹슨핀"]:
            self.bag.remove(tool.name)
            self.ui.update_bag_status(self.bag.items)
            
            self.ui.print_narrative("태양열 집광 장치로 햇빛을 모아 핀에 비추자, 핀이 시뻘겋게 달아오르며 녹아내렸다. 그 아래에는 **낡은 일기장**이 숨겨져 있었다.", is_markdown=True)
            
            diary = Item("낡은 일기장", "오래되어 바래진 가죽 표지의 일기장이다.", ["일기"])
            self.bag.add(diary)
            self.ui.update_bag_status(self.bag.items)
            
            self.current_puzzle = None
            self.ui.print_system_message(f"이제 `{CMD_EXAMINE[0]} 일기`로 일기장을 펼쳐볼 수 있다.")
        else:
            self.ui.print_system_message("아무 일도 일어나지 않았다.")

    def _read_diary(self):
        if self.diary_riddles_solved < len(DIARY_RIDDLES):
            riddle = DIARY_RIDDLES[self.diary_riddles_solved]
            self.current_puzzle = riddle["id"]
            self.ui.create_puzzle(riddle["title"], riddle["hint"], riddle["content"])
            self.ui.print_system_message(f"`{CMD_ANSWER[0]} <답안>` 형식으로 정답을 입력하세요.")
            if self.diary_riddles_solved == 0:
                self.clues["diary_page"] = 1
        else:
            self.ui.print_narrative("일기장의 마지막 페이지를 넘겼지만, 더 이상 쓰여있는 것이 없다.", is_markdown=True)

    def _check_answer(self, answer: str):
        if not self.current_puzzle or not self.current_puzzle.startswith("diary_"):
            self.ui.print_system_message("지금은 수수께끼를 푸는 상황이 아니다.")
            return
        
        riddle = DIARY_RIDDLES[self.diary_riddles_solved]
        if answer == riddle["answer"]:
            self.diary_riddles_solved += 1
            self.current_puzzle = None
            self.ui.print_narrative("정답이다! 머릿속이 맑아지는 기분이다.", is_markdown=True)

            if self.diary_riddles_solved < len(DIARY_RIDDLES):
                self.ui.print_system_message(f"`{CMD_EXAMINE[0]} 일기`로 다음 페이지를 확인하자.")
            else:
                self.ui.print_narrative("일기장에는 조종사가 살던 작은 별에 대한 이야기도 적혀 있었다. 활화산 두 개와 잠든 화산 하나가 있었다고 한다.", is_markdown=True)
                self.clues["volcanoes"] = 3
                self._meet_little_prince()
        else:
            self.ui.print_system_message("틀린 것 같다. 다시 한번 생각해보자.")

    def _meet_little_prince(self):
        self.ui.print_narrative(
            "일기장의 마지막 페이지를 덮는 순간, 등 뒤에서 작은 목소리가 들려왔다.\n\n"
            "**\"내 별로 돌아갈 지도를 찾아야 해. 저 상자 안에 있을지도 몰라...\"**\n\n"
            "뒤를 돌아보니, 금발의 작은 소년이 조종석 아래의 금속 상자를 가리키고 있었다.",
            is_markdown=True
        )
        self.current_puzzle = "locked_box"
        self.ui.create_puzzle(
            "퍼즐: 조종사의 상자",
            "오래된 금속 상자. 3자리 다이얼 자물쇠로 잠겨있다.",
            f"지금까지의 여정에서 단서를 찾을 수 있을 것 같다. `{CMD_DIAL[0]} <숫자>` 로 번호를 맞출 수 있다."
        )

    def _dial_combination(self, combination: str):
        if self.current_puzzle != "locked_box":
            self.ui.print_system_message("다이얼을 돌릴 만한 것이 보이지 않는다.")
            return

        correct_combo = f"{self.clues['tail_number']}{self.clues['diary_page']}{self.clues['volcanoes']}"
        if combination == correct_combo:
            self.ui.print_narrative("철컥, 소리와 함께 상자의 자물쇠가 풀렸다. 상자 안에는 양피지에 그려진 **별자리 지도**가 들어있었다.", is_markdown=True)
            star_map = Item("별자리 지도", "수많은 별들 사이로 길이 그려져 있는 오래된 지도.", ["지도"])
            self.bag.add(star_map)
            self.ui.update_bag_status(self.bag.items)
            self.current_puzzle = None
            # 다음 스토리 진행...
        else:
            self.ui.print_system_message("번호가 맞지 않는다. 딸깍거리는 소리만 날 뿐이다.")

    def _find_item_in_bag(self, name: str) -> Item | None:
        name_lower = name.lower()
        for item in self.bag.items.values():
            if item.name.lower() == name_lower or name_lower in [alias.lower() for alias in item.aliases]:
                return item
        return None
