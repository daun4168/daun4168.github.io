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
*   **`Combination`**: Defines interactions that occur when multiple keywords are combined. It includes a `type` and a list of `targets`.
*   **`ChapterData`**: A model for data that is common across all scenes within a single chapter, such as shared `combinations`.
*   **`SceneData`**: The top-level data model for a single scene. It encapsulates:
    *   `id`: Unique identifier for the scene.
    *   `name`: Display name of the scene.
    *   `initial_text`: The narrative text displayed when entering the scene.
    *   `initial_state`: Initial state variables specific to this scene.
    *   `keywords`: A dictionary mapping keyword IDs to `KeywordData` objects.
    *   `combinations`: A list of `Combination` objects specific to this scene.
    *   `on_enter_actions`: Actions to be executed automatically when the scene is entered.

### `logic_handlers.py`

This file contains the concrete implementations for handling game conditions and actions. It follows a Strategy pattern, where different `ConditionHandler` and `ActionHandler` classes are responsible for specific types of conditions and actions.

*   **`ActionHandler` (ABC)**: Abstract base class for all action handlers. Subclasses must implement the `execute(self, scene, value)` method.
*   **`ConditionHandler` (ABC)**: Abstract base class for all condition handlers. Subclasses must implement the `check(self, scene, target, value) -> bool` method.
*   **Concrete Implementations**:
    *   **Condition Handlers**: `HasItemHandler`, `NotHasItemHandler`, `StateIsHandler`, `StateNotHandler`, `StaminaMinHandler` – these check various conditions related to the player's inventory, scene state, or player stats.
    *   **Action Handlers**: `PrintNarrativeHandler`, `PrintSystemHandler`, `AddItemHandler`, `RemoveItemHandler`, `RemoveKeywordHandler`, `UpdateStateHandler`, `MoveSceneHandler`, `GameEndHandler`, `ModifyStaminaHandler`, `SaveCheckpointHandler`, `ReloadCheckpointHandler`, `ShowStaminaUIHandler`, `RequestConfirmationHandler` – these perform various game operations like displaying text, modifying inventory, changing scene/game state, managing player stats, or handling user confirmations.
*   **`CONDITION_HANDLERS` & `ACTION_HANDLERS`**: Dictionaries that map `ConditionType` and `ActionType` enums (defined in `const.py`) to their respective handler instances. This allows the game engine to dynamically select the correct handler based on the `type` specified in the `Condition` and `Action` data models.

### `scene.py`

This file defines the `Scene` class, which represents a single game scene and manages its specific logic and state.

*   **`Scene` Class**:
    *   Holds `SceneData` and optional `ChapterData` objects, which contain the static definition of the scene and chapter.
    *   Manages the dynamic `state` of the current scene.
    *   Provides methods for `on_enter` (actions when entering the scene) and `on_redisplay` (when the scene text is shown again, e.g., "look around").
    *   Handles `resolve_alias` for keywords.
    *   Contains `process_keyword` and `process_combination` methods to interpret user input. `process_combination` also handles chapter-wide combinations.
    *   Uses `_check_conditions` and `_execute_actions` internally, delegating to the handlers defined in `logic_handlers.py`. `_execute_actions` will stop if a scene transition occurs.
    *   Manages keyword discovery and visibility (`_discover_keyword`, `_check_keyword_visible`).

### `scene_manager.py`

This file contains `SceneFactory` and `SceneManager` classes, responsible for creating and managing game scenes.

*   **`SceneFactory`**:
    *   Registers `SceneData` and optional `ChapterData` with their corresponding `Scene` classes.
    *   Creates `Scene` instances on demand, injecting necessary dependencies (`game`, `ui`, `inventory`, `player`) and `ChapterData`.
*   **`SceneManager`**:
    *   Manages the active `Scene` instance and a cache of created scenes.
    *   Handles switching between scenes (`switch_scene`) and resetting the cache for checkpoint loads (`reset_scene`).
    *   Acts as the primary command processor (`process_command`), parsing user input to differentiate between keyword interactions, combinations (`+`), password inputs (`:`), and confirmation responses (`예`/`아니오`).
    *   Delegates the parsed command to the `current_scene` for logical processing.

### `ui.py`

This file manages all user interface interactions, abstracting away the details of the HTML DOM manipulation.

*   **`UIManager` Class**:
    *   Provides methods to update various UI elements: main text output, inventory, location name, stamina, and sight status.
    *   `update_sight_status` displays keywords based on their state (e.g., `[keyword]` for `DISCOVERED`, `[?]` for `HIDDEN`).
    *   `update_stamina_status` and `toggle_stamina_ui` manage the player's stamina display.
    *   Handles printing narrative text, system messages, and user input logs.
    *   Includes a `scroll_to_bottom` method to ensure the latest text is always visible.
*   **`get_josa` Function**: A utility function to correctly append Korean particles (josa) based on the preceding word's last character.

### `entity.py`

This file defines the base `Entity` class and specific game entities like `Item`, `Inventory`, and `Player`.

*   **`Entity`**: A base class for game objects, providing a way to set a global `UIManager` for all entities to interact with the UI.
*   **`Item`**: Represents an item in the game, with a `name` and `description`. It can display its description via the `UIManager`.
*   **`Inventory`**: Manages a collection of `Item` objects for the player. It can add, remove, check for, and retrieve items, and updates the UI's inventory status.
*   **`Player`**: Manages player-specific data, such as stamina.

### `const.py`

This file defines various `StrEnum` classes that serve as constants throughout the game.

*   **`ChapterID`**: Unique identifiers for each chapter.
*   **`SceneID`**: Unique identifiers for each scene.
*   **`KeywordId`**: Unique identifiers for interactive keywords within scenes.
*   **`KeywordState`**: Defines possible states for keywords (e.g., `HIDDEN`, `DISCOVERED`, `INACTIVE`).
*   **`ConditionType`**: Defines types of conditions that can be checked (e.g., `HAS_ITEM`, `STATE_IS`).
*   **`ActionType`**: Defines types of actions that can be executed (e.g., `PRINT_NARRATIVE`, `ADD_ITEM`, `MOVE_SCENE`).
*   **`KeywordType`**: Categorizes keywords (e.g., `ITEM`, `OBJECT`, `NPC`, `PORTAL`, `ALIAS`).
*   **`CommandType`**: Defines special commands recognized by the game (e.g., `INVENTORY`, `WAKE_UP`, `LOOK_AROUND`).
*   **`CombinationType`**: Defines types for keyword combinations (e.g., `DEFAULT`, `PASSWORD`).

### `test.py`

This file provides a testing utility to automate game command sequences.

*   **`TestRunner`**:
    *   Contains predefined sequences of commands for different scenes.
    *   Can execute these sequences to simulate player input for testing purposes.
    *   Integrates with the `Game` class to process commands.

### `main.py`

This is the entry point of the application logic.

*   It initializes the core components (`UIManager`, `Inventory`, `Player`, `TestRunner`).
*   It then creates the main `Game` instance, injecting these dependencies.
*   This file is executed by PyScript when the `index.html` page is loaded.

### `game.py`

This file acts as the central orchestrator of the game, tying all the other components together. It serves as the "Composition Root" of the application.

*   **`Game` Class**:
    *   **Initialization**: In its `__init__`, it takes dependencies like `UIManager`, `Inventory`, `Player`, and `TestRunner`. It creates the `SceneFactory` and `SceneManager`.
    *   **Scene Registration**: It's responsible for registering all `SceneData` from the `story/` modules with the `SceneFactory`.
    *   **Event Handling**: It binds to HTML input elements and handles raw user input events (`_handle_click`, `_handle_enter`), passing the commands to `process_command`.
    *   **Command Processing**: It serves as the first layer of command processing. It checks for global commands (like `LOOK_AROUND` or viewing an inventory item's description) before delegating the command to the active `SceneManager`.
    *   **Game Flow**: It manages the overall game flow, including running the intro sequence (`run_intro`), starting the game (`start_game`), and handling checkpoints (`save_checkpoint`, `load_checkpoint`).

### Scene Data Files (e.g., `story/chapter0/scene0.py`)

These files contain the actual game content, defined as instances of `SceneData` using the schemas from `schemas.py`.

*   Each file typically defines one or more `SceneData` objects.
*   They populate the `SceneData` fields with specific narrative text, initial states, and detailed `KeywordData` objects, including their `interactions` (conditions and actions).
*   This separation allows game designers to create and modify game content without touching the core game logic.

### `index.html` and `pyscript.toml`

These files are responsible for the web-based execution of the game.

*   **`index.html`**: The main HTML file that defines the structure of the web page, including the UI elements for the game. It loads the PyScript library and specifies that `main.py` should be executed.
*   **`pyscript.toml`**: A configuration file for PyScript. It can be used to declare Python package dependencies or specify which local files are needed for the application to run.

## How it all connects

1.  **Application Startup (`index.html` -> `main.py`)**: A user opens `index.html` in their browser. The page loads the PyScript engine, which in turn executes the `main.py` script.
2.  **Game Initialization (`main.py` -> `game.py`)**: The `main.py` script initializes essential services like `UIManager`, `Inventory`, `Player`, and `TestRunner`. It then creates the central `Game` object, injecting these services as dependencies.
3.  **Game Setup (`game.py`)**: The `Game` class is instantiated. It sets up the `SceneFactory` and `SceneManager`, registering all available `SceneData` objects (loaded from `story/chapterX/sceneY.py` files) with the `SceneFactory`. It also binds to HTML elements for user input and configures the initial UI state.
4.  **Intro Sequence (`game.py`)**: The `Game` class displays an intro sequence using the `UIManager`. User input is disabled until the intro concludes.
5.  **Game Start (`game.py` -> `scene_manager.py`)**: Once the player issues the `WAKE_UP` command (defined in `const.py`), `game.start_game()` is called. This instructs the `SceneManager` to switch to the initial scene (e.g., `CH0_SCENE0`).
6.  **Scene Entry (`scene_manager.py` -> `scene.py`)**:
    *   When `SceneManager.switch_scene()` is called, it either retrieves an existing `Scene` instance from its cache or creates a new one using the `SceneFactory`.
    *   The `SceneManager` then calls the `Scene` instance's `on_enter()` method.
    *   The `Scene.on_enter()` method displays the scene's initial narrative text, updates the UI's location name, and executes any `on_enter_actions`.
7.  **User Input Processing (`game.py` -> `scene_manager.py` -> `scene.py`)**:
    *   The `Game` class listens for user input via HTML event handlers.
    *   When a command is entered, `game.process_command()` is called. It first checks for global commands before delegating to the `SceneManager`.
    *   The `SceneManager` then parses the command, checking for special formats (`+`, `:`) or confirmation states, before passing it to the active `Scene`'s `process_keyword` or `process_combination` methods.
8.  **Scene Logic Execution (`scene.py` -> `logic_handlers.py`)**:
    *   The `Scene` instance attempts to match the user's input to a `Keyword` or `Combination`.
    *   For each potential `Interaction`, it checks `conditions` using the `CONDITION_HANDLERS`.
    *   If conditions are met, it executes `actions` using the `ACTION_HANDLERS`. The action execution will be halted if any action causes a scene change (e.g., `MOVE_SCENE` or player death).
9.  **Dynamic Behavior**: This architecture allows for flexible, data-driven game logic. New content, conditions, or actions can be added by defining new data objects or handler classes without modifying the core engine.

This modular design ensures that the game logic is separated from the game content, making it easier to develop, maintain, and extend the game.
