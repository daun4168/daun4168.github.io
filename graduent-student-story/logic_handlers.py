from abc import ABC, abstractmethod

from const import ActionType, ConditionType, KeywordState
from entity import Item
import json
from ui import get_josa

# --- Base Interfaces ---


class ActionHandler(ABC):
    @abstractmethod
    def execute(self, scene, value):
        pass


class ConditionHandler(ABC):
    @abstractmethod
    def check(self, scene, target, value) -> bool:
        pass


# --- Condition Implementations ---


class HasItemHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.inventory.has(target)


class NotHasItemHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return not scene.inventory.has(target)


class NotHasAllItemsHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        has_all = True
        for item in target:
            if scene.inventory.has(item):
                has_all = False
        return has_all


class StateIsHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.state.get(target) == value


class StateNotHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.state.get(target) != value


class ChapterStateIsHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        # scene.chapter_state에서 target 키의 값을 확인
        return scene.chapter_state.get(target) == value


class ChapterStateNotHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.chapter_state.get(target) != value


class StaminaMinHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.player.current_stamina >= int(value)


class StonePuzzleHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        target = json.loads(target)
        keys = target["keys"]
        weights = target["weights"]
        target_weight = target["target_weight"]

        total_weight = 0
        for key, weight in zip(keys, weights):
            if scene.state.get(key, False):
                total_weight += weight

        # value is one of gt, lt, eq
        if value == "gt":
            return total_weight > target_weight
        elif value == "lt":
            return total_weight < target_weight
        elif value == "eq":
            return total_weight == target_weight
        return False


# --- Action Implementations ---


class PrintNarrativeHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_narrative(value, is_markdown=True)


class PrintSystemHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_system_message(value, is_markdown=True)


class PrintImageHandler(ActionHandler):
    def execute(self, scene, value):
        src = value.get("src", "")
        alt = value.get("alt", "")
        width = value.get("width", 400)
        text = f"""
        <img src="{src}" alt="{alt}" width="{width}">
        """.strip()
        scene.ui.print_system_message(text, is_markdown=False)


class AddItemHandler(ActionHandler):
    def execute(self, scene, value):
        new_item = Item(value["name"], value["description"])
        is_silent = value.get("silent", False)
        scene.inventory.add(new_item, silent=is_silent)
        if not is_silent:
            new_item.show_description()


class RemoveItemHandler(ActionHandler):
    def execute(self, scene, value):
        scene.inventory.remove(value)


class DiscoverKeywordHandler(ActionHandler):
    def execute(self, scene, value):
        if value in scene.scene_data.keywords:
            scene.scene_data.keywords[value].state = KeywordState.DISCOVERED
            scene.ui.update_sight_status(scene.scene_data.keywords)
            text = f"**[{value}]**{get_josa(str(value), '을/를')} 발견하여 **시야**에 추가합니다."
            scene.ui.print_system_message(text, is_markdown=True)


class RemoveKeywordHandler(ActionHandler):
    def execute(self, scene, value):
        target = value
        if target in scene.scene_data.keywords:
            del scene.scene_data.keywords[target]
            scene.ui.update_sight_status(scene.scene_data.keywords)


class UpdateStateHandler(ActionHandler):
    def execute(self, scene, value):
        if "scene_id" in value:
            scene_id = value["scene_id"]
            scenes = scene.game.scene_manager.scenes
            if scene_id in scenes:
                scene = scenes[scene_id]
            else:
                return

        if "key" in value:
            scene.state[value["key"]] = value["value"]

        if "keyword" in value:
            k_name = value["keyword"]
            if k_name in scene.scene_data.keywords:
                scene.scene_data.keywords[k_name].state = value["state"]

        if "scene_id" not in value:
            scene.ui.update_sight_status(scene.scene_data.keywords)


class UpdateChapterStateHandler(ActionHandler):
    def execute(self, scene, value):
        # value 구조 예시: {"key": "has_met_professor", "value": True}
        if "key" in value:
            scene.chapter_state[value["key"]] = value["value"]


class ToggleSwitchHandler(ActionHandler):
    def execute(self, scene, value):
        target = value
        if target in scene.state:
            scene.state[target] = not scene.state[target]


class PrintSwitchHandler:  # ActionHandler를 상속받는다고 가정
    def execute(self, scene, value):
        """
        value: list[bool] 형태의 스위치 5개 상태를 받아서 출력합니다.
        예: [False, True, False, True, True]
        """
        output_parts = []
        HINDI_NUMERALS = ["①", "②", "③", "④", "⑤"]

        # value는 [sw1_state, sw2_state, ...] 순서로 들어온다고 가정
        if not isinstance(value, list) or len(value) != 5:
            # 오류 처리 로직
            scene.ui.print_system_message("Error: PrintSwitchHandler requires a list of 5 boolean values.")
            return

        for i, target in enumerate(value):
            if target in scene.state:
                state = scene.state[target]
                # 상태에 따라 ON/OFF 문자열 결정
                status = "[ON]" if state else "[OFF]"

                # ① [OFF] 형태로 포맷팅하여 리스트에 추가
                output_parts.append(f"{HINDI_NUMERALS[i]} {status}")

        # 전체 문자열을 ", "로 연결하고 마침표 추가
        output_string = ", ".join(output_parts)

        # 출력
        scene.ui.print_narrative(output_string)


class MoveSceneHandler(ActionHandler):
    def execute(self, scene, value):
        scene.game.scene_manager.switch_scene(value)


class GameEndHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_narrative(value, is_markdown=True)
        scene.ui.print_system_message("--- GAME OVER ---\n(새로고침하여 다시 시작하세요)", is_markdown=True)
        if scene.game:
            scene.game.user_input.disabled = True
            scene.game.submit_button.disabled = True


class ModifyStaminaHandler(ActionHandler):
    def execute(self, scene, value):
        amount = int(value)
        scene.player.modify_stamina(amount)

        # 사망 체크 및 부활 로직
        if scene.player.is_dead():
            scene.ui.print_narrative(
                "\n**[시야가 암전됩니다...]**\n극심한 피로와 탈진으로 의식을 잃었습니다.\n\n(가장 최근의 체크포인트로 되돌아갑니다.)",
                is_markdown=True,
            )
            if scene.game:
                scene.game.load_checkpoint()


class SaveCheckpointHandler(ActionHandler):
    def execute(self, scene, value):
        scene.game.save_checkpoint(scene.scene_id)


class ReloadCheckpointHandler(ActionHandler):
    def execute(self, scene, value):
        scene.game.load_checkpoint()


class ShowStaminaUIHandler(ActionHandler):
    def execute(self, scene, value):
        """체력 UI 표시 여부를 제어합니다. value: bool"""
        scene.ui.toggle_stamina_ui(value)


class RequestConfirmationHandler(ActionHandler):
    def execute(self, scene, value):
        """
        value 구조:
        {
            "prompt": "질문 내용",
            "confirm_actions": [Action 객체 리스트],
            "cancel_actions": [Action 객체 리스트]
        }
        """
        prompt = value.get("prompt", "진행하시겠습니까? (예/아니오)")

        # 질문 출력
        scene.ui.print_narrative(prompt, is_markdown=True)
        scene.ui.print_system_message("`예` 또는 `아니오`를 입력하세요.")

        # 게임 상태를 대기 모드로 전환하고 할 일 저장
        scene.game.pending_confirmation = {
            "on_confirm": value.get("confirm_actions", []),
            "on_cancel": value.get("cancel_actions", []),
        }


class UpdateItemDataHandler(ActionHandler):
    def execute(self, scene, value):
        """
        value 구조:
        {
            "keyword": KeywordId,
            "field": "display_name" | "description",
            "value": "변경할 내용"
        }
        """
        keyword_id = value.get("keyword")
        field = value.get("field")
        new_value = value.get("value")
        scene.inventory.update(keyword_id, field, new_value)


# --- Registries (Strategy Mapping) ---

CONDITION_HANDLERS = {
    ConditionType.HAS_ITEM: HasItemHandler(),
    ConditionType.NOT_HAS_ITEM: NotHasItemHandler(),
    ConditionType.NOT_HAS_ALL_ITEMS: NotHasAllItemsHandler(),
    ConditionType.STATE_IS: StateIsHandler(),
    ConditionType.STATE_NOT: StateNotHandler(),
    ConditionType.STAMINA_MIN: StaminaMinHandler(),
    ConditionType.STONE_PUZZLE: StonePuzzleHandler(),
    ConditionType.CHAPTER_STATE_IS: ChapterStateIsHandler(),
    ConditionType.CHAPTER_STATE_NOT: ChapterStateNotHandler(),
}

ACTION_HANDLERS = {
    # Print
    ActionType.PRINT_NARRATIVE: PrintNarrativeHandler(),
    ActionType.PRINT_SYSTEM: PrintSystemHandler(),
    ActionType.PRINT_IMAGE: PrintImageHandler(),
    # Modify
    ActionType.ADD_ITEM: AddItemHandler(),
    ActionType.REMOVE_ITEM: RemoveItemHandler(),
    ActionType.DISCOVER_KEYWORD: DiscoverKeywordHandler(),
    ActionType.REMOVE_KEYWORD: RemoveKeywordHandler(),
    ActionType.UPDATE_STATE: UpdateStateHandler(),
    ActionType.UPDATE_ITEM_DATA: UpdateItemDataHandler(),
    ActionType.UPDATE_CHAPTER_STATE: UpdateChapterStateHandler(),
    ActionType.TOGGLE_SWITCH: ToggleSwitchHandler(),
    ActionType.PRINT_SWITCH: PrintSwitchHandler(),
    # Game
    ActionType.MOVE_SCENE: MoveSceneHandler(),
    ActionType.SAVE_CHECKPOINT: SaveCheckpointHandler(),
    ActionType.RELOAD_CHECKPOINT: ReloadCheckpointHandler(),
    ActionType.SHOW_STAMINA_UI: ShowStaminaUIHandler(),
    ActionType.GAME_END: GameEndHandler(),
    ActionType.MODIFY_STAMINA: ModifyStaminaHandler(),
    ActionType.REQUEST_CONFIRMATION: RequestConfirmationHandler(),
}
