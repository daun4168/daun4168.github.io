from abc import ABC, abstractmethod

from const import ActionType, ConditionType
from entity import Item

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


class StateIsHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.state.get(target) == value


class StateNotHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.state.get(target) != value


class StaminaMinHandler(ConditionHandler):
    def check(self, scene, target, value) -> bool:
        return scene.player.current_stamina >= int(value)


# --- Action Implementations ---


class PrintNarrativeHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_narrative(value, is_markdown=True)


class PrintSystemHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_system_message(value, is_markdown=True)


class AddItemHandler(ActionHandler):
    def execute(self, scene, value):
        new_item = Item(value["name"], value["description"])
        is_silent = value.get("silent", False)
        scene.inventory.add(new_item, silent=is_silent)


class RemoveItemHandler(ActionHandler):
    def execute(self, scene, value):
        scene.inventory.remove(value)


class RemoveKeywordHandler(ActionHandler):
    def execute(self, scene, value):
        target = value
        if target in scene.scene_data.keywords:
            del scene.scene_data.keywords[target]
            scene.ui.update_sight_status(scene.scene_data.keywords)


class UpdateStateHandler(ActionHandler):
    def execute(self, scene, value):
        if "key" in value:
            scene.state[value["key"]] = value["value"]

        if "keyword" in value:
            k_name = value["keyword"]
            if k_name in scene.scene_data.keywords:
                scene.scene_data.keywords[k_name].state = value["state"]
                scene.ui.update_sight_status(scene.scene_data.keywords)


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


class UpdateKeywordDataHandler(ActionHandler):
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

        if keyword_id in scene.scene_data.keywords:
            keyword_data = scene.scene_data.keywords[keyword_id]
            if field == "display_name":
                keyword_data.display_name = new_value
            elif field == "description":
                keyword_data.description = new_value
            scene.ui.update_sight_status(scene.scene_data.keywords)


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
    ConditionType.STATE_IS: StateIsHandler(),
    ConditionType.STATE_NOT: StateNotHandler(),
    ConditionType.STAMINA_MIN: StaminaMinHandler(),
}

ACTION_HANDLERS = {
    ActionType.PRINT_NARRATIVE: PrintNarrativeHandler(),
    ActionType.PRINT_SYSTEM: PrintSystemHandler(),
    ActionType.ADD_ITEM: AddItemHandler(),
    ActionType.REMOVE_ITEM: RemoveItemHandler(),
    ActionType.REMOVE_KEYWORD: RemoveKeywordHandler(),
    ActionType.UPDATE_STATE: UpdateStateHandler(),
    ActionType.MOVE_SCENE: MoveSceneHandler(),
    ActionType.GAME_END: GameEndHandler(),
    ActionType.MODIFY_STAMINA: ModifyStaminaHandler(),
    ActionType.SAVE_CHECKPOINT: SaveCheckpointHandler(),
    ActionType.RELOAD_CHECKPOINT: ReloadCheckpointHandler(),
    ActionType.SHOW_STAMINA_UI: ShowStaminaUIHandler(),
    ActionType.REQUEST_CONFIRMATION: RequestConfirmationHandler(),
    ActionType.UPDATE_KEYWORD_DATA: UpdateKeywordDataHandler(),
    ActionType.UPDATE_ITEM_DATA: UpdateItemDataHandler(),
}
