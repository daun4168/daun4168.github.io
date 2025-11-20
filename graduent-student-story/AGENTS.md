# Project Structure for New Agents

This document provides a high-level overview of the project's core components, focusing on how game logic, data structures, and content are organized.

## Core Concepts

The game is structured around **Scenes**, which contain **Keywords** and define possible **Interactions**. These interactions are governed by **Conditions** and trigger **Actions**.

## Key Files and Their Roles

### `schemas.py`

This file defines the data models for the game's content using `Pydantic`'s `BaseModel`. It acts as the blueprint for how all game data is structured.

*   **`Condition`**: Represents a prerequisite for an action to occur. It has a `type` (e.g., `HAS_ITEM`, `STATE_IS`), a `target` (e.g., an item ID, a state key), and a `value` to compare against.
*   **`Action`**: Represents an effect that happens in the game. It has a `type` (e.g., `PRINT_NARRATIVE`, `ADD_ITEM`, `MOVE_SCENE`) and a `value` which provides the necessary data for the action.
*   **`Interaction`**: A collection of `conditions` and `actions`. If all conditions are met, the actions are executed.
*   **`KeywordData`**: Defines an interactive element within a scene (e.g., an object, an NPC, a portal). It includes:
    *   `type`: The category of the keyword (e.g., `OBJECT`, `NPC`, `PORTAL`).
    *   `state`: Its current visibility/interactability state (e.g., `HIDDEN`, `VISIBLE`).
    *   `display_name`, `description`: Textual information.
    *   `interactions`: A list of possible `Interaction` objects associated with this keyword.
    *   `silent_discovery`: If `True`, the keyword is discovered without a system message.
    *   `target`: Used for aliases or specific targeting.
*   **`Combination`**: Defines interactions that occur when multiple keywords are combined.
*   **`SceneData`**: The top-level data model for a single scene. It encapsulates:
    *   `id`: Unique identifier for the scene.
    *   `name`: Display name of the scene.
    *   `initial_text`: The narrative text displayed when entering the scene.
    *   `initial_state`: Initial state variables specific to this scene.
    *   `keywords`: A dictionary mapping keyword IDs to `KeywordData` objects.
    *   `combinations`: A list of `Combination` objects.
    *   `on_enter_actions`: Actions to be executed automatically when the scene is entered.

### `logic_handlers.py`

This file contains the concrete implementations for handling game conditions and actions. It follows a Strategy pattern, where different `ConditionHandler` and `ActionHandler` classes are responsible for specific types of conditions and actions.

*   **`ActionHandler` (ABC)**: Abstract base class for all action handlers. Subclasses must implement the `execute(self, scene, value)` method.
*   **`ConditionHandler` (ABC)**: Abstract base class for all condition handlers. Subclasses must implement the `check(self, scene, target, value) -> bool` method.
*   **Concrete Implementations**:
    *   **Condition Handlers**: `HasItemHandler`, `NotHasItemHandler`, `StateIsHandler`, `StateNotHandler` – these check various conditions related to the player's inventory or the scene's state.
    *   **Action Handlers**: `PrintNarrativeHandler`, `PrintSystemHandler`, `AddItemHandler`, `RemoveItemHandler`, `RemoveKeywordHandler`, `UpdateStateHandler`, `MoveSceneHandler`, `GameEndHandler` – these perform various game operations like displaying text, modifying inventory, changing scene state, or transitioning between scenes.
*   **`CONDITION_HANDLERS` & `ACTION_HANDLERS`**: Dictionaries that map `ConditionType` and `ActionType` enums (defined in `const.py`) to their respective handler instances. This allows the game engine to dynamically select the correct handler based on the `type` specified in the `Condition` and `Action` data models.

### `scene.py`

This file defines the `Scene` class, which represents a single game scene and manages its specific logic and state.

*   **`Scene` Class**:
    *   Holds a `SceneData` object (from `schemas.py`) which contains the static definition of the scene.
    *   Manages the dynamic `state` of the current scene.
    *   Provides methods for `on_enter` (actions when entering the scene) and `on_redisplay` (when the scene text is shown again, e.g., "look around").
    *   Handles `resolve_alias` for keywords.
    *   Contains `process_keyword` and `process_combination` methods to interpret user input related to interactive elements within the scene.
    *   Uses `_check_conditions` and `_execute_actions` internally, delegating to the handlers defined in `logic_handlers.py`.
    *   Manages keyword discovery and visibility (`_discover_keyword`, `_check_keyword_visible`).

### `scene_manager.py`

This file contains `SceneFactory` and `SceneManager` classes, responsible for creating and managing game scenes.

*   **`SceneFactory`**:
    *   Registers `SceneData` objects with their corresponding `Scene` classes.
    *   Creates `Scene` instances on demand, injecting necessary dependencies (`game`, `ui`, `inventory`).
*   **`SceneManager`**:
    *   Manages the active `Scene` instance.
    *   Handles switching between different scenes (`switch_scene`).
    *   Delegates user commands to the `current_scene` for processing (`process_command`).
    *   Caches `Scene` instances to avoid redundant creation.

### `ui.py`

This file manages all user interface interactions, abstracting away the details of the HTML DOM manipulation.

*   **`UIManager` Class**:
    *   Provides methods to update various UI elements such as the main text output, inventory status, location name, and visible keywords (sight status).
    *   Handles printing narrative text, system messages, and user input logs.
    *   Includes a `scroll_to_bottom` method to ensure the latest text is always visible.
*   **`get_josa` Function**: A utility function to correctly append Korean particles (josa) based on the preceding word's last character.

### `entity.py`

This file defines the base `Entity` class and specific game entities like `Item` and `Inventory`.

*   **`Entity`**: A base class for game objects, providing a way to set a global `UIManager` for all entities to interact with the UI.
*   **`Item`**: Represents an item in the game, with a `name` and `description`. It can display its description via the `UIManager`.
*   **`Inventory`**: Manages a collection of `Item` objects for the player. It can add, remove, check for, and retrieve items, and updates the UI's inventory status.

### `const.py`

This file defines various `StrEnum` classes that serve as constants throughout the game.

*   **`SceneID`**: Unique identifiers for each scene.
*   **`KeywordId`**: Unique identifiers for interactive keywords within scenes.
*   **`KeywordState`**: Defines possible states for keywords (e.g., `HIDDEN`, `DISCOVERED`, `INACTIVE`).
*   **`ConditionType`**: Defines types of conditions that can be checked (e.g., `HAS_ITEM`, `STATE_IS`).
*   **`ActionType`**: Defines types of actions that can be executed (e.g., `PRINT_NARRATIVE`, `ADD_ITEM`, `MOVE_SCENE`).
*   **`KeywordType`**: Categorizes keywords (e.g., `OBJECT`, `NPC`, `PORTAL`, `ALIAS`).
*   **`CommandType`**: Defines special commands recognized by the game (e.g., `INVENTORY`, `WAKE_UP`, `LOOK_AROUND`).

### `test.py`

This file provides a testing utility to automate game command sequences.

*   **`TestRunner`**:
    *   Contains predefined sequences of commands for different scenes.
    *   Can execute these sequences to simulate player input for testing purposes.
    *   Integrates with the `Game` class to process commands.

### `main.py`

This is the entry point of the application.

*   It initializes the core components (`UIManager`, `Inventory`, `TestRunner`).
*   It then creates the main `Game` instance, injecting these dependencies.
*   This file essentially kicks off the game.

### Scene Data Files (e.g., `story/chapter0/scene0.py`)

These files contain the actual game content, defined as instances of `SceneData` using the schemas from `schemas.py`.

*   Each file typically defines one or more `SceneData` objects.
*   They populate the `SceneData` fields with specific narrative text, initial states, and detailed `KeywordData` objects, including their `interactions` (conditions and actions).
*   This separation allows game designers to create and modify game content without touching the core game logic.

## How it all connects

1.  **Application Startup (`main.py`)**: The `main.py` script is executed, which initializes essential services like `UIManager`, `Inventory`, and `TestRunner`. It then creates the central `Game` object, injecting these services as dependencies.
2.  **Game Initialization (`game.py`)**: The `Game` class is instantiated. It sets up the `SceneFactory` and `SceneManager`, registering all available `SceneData` objects (loaded from `story/chapterX/sceneY.py` files) with the `SceneFactory`. The `UIManager` is also configured for initial display.
3.  **Intro Sequence (`game.py`)**: The `Game` class displays an intro sequence using the `UIManager`. User input is disabled until the intro concludes.
4.  **Game Start (`game.py` -> `scene_manager.py`)**: Once the player issues the `WAKE_UP` command (defined in `const.py`), `game.start_game()` is called. This instructs the `SceneManager` to switch to the initial scene (e.g., `CH0_SCENE0`).
5.  **Scene Entry (`scene_manager.py` -> `scene.py`)**:
    *   When `SceneManager.switch_scene()` is called, it either retrieves an existing `Scene` instance from its cache or creates a new one using the `SceneFactory` (which uses the registered `SceneData` and `Scene` class).
    *   The `SceneManager` then calls the `Scene` instance's `on_enter()` method.
    *   The `Scene.on_enter()` method displays the scene's initial narrative text using the `UIManager`, updates the UI's location name, and executes any `on_enter_actions` defined in the `SceneData`.
6.  **User Input Processing (`game.py` -> `scene_manager.py` -> `scene.py`)**:
    *   The `Game` class continuously listens for user input via HTML event handlers.
    *   When a command is entered, `game.process_command()` is called.
    *   This method first checks for special commands (like `LOOK_AROUND` from `const.py`), test commands (handled by `TestRunner`), or inventory item descriptions (checked against `Inventory`).
    *   If the command is not a global one, it's delegated to the `SceneManager`'s `process_command` method, which then passes it to the `process_command` method of the *current active `Scene` instance*.
7.  **Scene Logic Execution (`scene.py` -> `logic_handlers.py`)**:
    *   The `Scene` instance's `process_command` (or `process_keyword`, `process_combination`) attempts to match the user's input to a `Keyword` or `Combination` defined in its `SceneData`.
    *   For each potential `Interaction` or `Combination`, the `Scene` calls its `_check_conditions()` method. This method iterates through the `conditions` and uses the `CONDITION_HANDLERS` registry (from `logic_handlers.py`) to find and execute the appropriate `ConditionHandler` (e.g., `HasItemHandler`, `StateIsHandler`).
    *   If all conditions are met, the `Scene` then calls its `_execute_actions()` method. This method iterates through the `actions` and uses the `ACTION_HANDLERS` registry (from `logic_handlers.py`) to find and execute the appropriate `ActionHandler` (e.g., `PrintNarrativeHandler`, `AddItemHandler`, `MoveSceneHandler`). These actions frequently interact with the `UIManager` to update the display or the `Inventory` to modify player items.
8.  **Dynamic Behavior**: This architecture allows for highly flexible and data-driven game logic. New conditions or actions can be added by creating new handler classes and registering them in `logic_handlers.py`, without modifying existing game content or the core engine. Similarly, new game content can be created by simply defining new `SceneData` objects using the existing schemas.

This modular design ensures that the game logic is separated from the game content, making it easier to develop, maintain, and extend the game.
