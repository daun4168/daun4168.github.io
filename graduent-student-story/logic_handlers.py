from abc import ABC, abstractmethod
from entity import Item
from const import ActionType, ConditionType, KeywordState


# --- Base Interfaces ---

class ActionHandler(ABC):
    @abstractmethod
    def execute(self, scene, value):
        """
        :param scene: 동작을 수행할 Scene 인스턴스
        :param value: 데이터 파일에 정의된 액션의 value (dict, str 등)
        """
        pass


class ConditionHandler(ABC):
    @abstractmethod
    def check(self, scene, target, value) -> bool:
        """
        :param scene: 검사를 수행할 Scene 인스턴스
        :param target: 검사 대상 (item id, state key 등)
        :param value: 비교할 값
        """
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
        if target in scene.scene_data["keywords"]:
            del scene.scene_data["keywords"][target]
            scene.ui.update_sight_status(scene.scene_data["keywords"])


class UpdateStateHandler(ActionHandler):
    def execute(self, scene, value):
        # 1. 게임 상태 변수 업데이트
        if "key" in value:
            scene.state[value["key"]] = value["value"]

        # 2. 키워드(오브젝트) 상태 업데이트
        if "keyword" in value:
            k_name = value["keyword"]
            if k_name in scene.scene_data["keywords"]:
                scene.scene_data["keywords"][k_name]["state"] = value["state"]
                scene.ui.update_sight_status(scene.scene_data["keywords"])


class MoveSceneHandler(ActionHandler):
    def execute(self, scene, value):
        scene.game.scene_manager.switch_scene(value)


class GameEndHandler(ActionHandler):
    def execute(self, scene, value):
        scene.ui.print_narrative(value, is_markdown=True)
        scene.ui.print_system_message("--- GAME OVER ---", is_markdown=True)
        if scene.game:
            scene.game.user_input.disabled = True
            scene.game.submit_button.disabled = True


# --- Registries (Strategy Mapping) ---

CONDITION_HANDLERS = {
    ConditionType.HAS_ITEM: HasItemHandler(),
    ConditionType.NOT_HAS_ITEM: NotHasItemHandler(),
    ConditionType.STATE_IS: StateIsHandler(),
    ConditionType.STATE_NOT: StateNotHandler(),
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
}