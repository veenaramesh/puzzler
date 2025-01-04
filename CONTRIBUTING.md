# Contributing to THE PUZZLER. 

## Quick code requirements for 'Escape Room' puzzles. 

#### Action methods
All puzzle actions must return a string describing the result. We send this returned string back to the LLM. 

example: 
```python
def move_player(self, direction: str) -> str:
    old_position = self.player.position
    if self.player.move(direction, self.grid_size):
        self.steps += 1
        return self.handle_player_movement(old_position, self.player.position)
    return "Invalid move"

def equip(self, obj_name: str) -> str:
    obj = self.get_object_by_name(obj_name)
    if obj:
        if self.player.inventory:
            return "Your hands are full! Drop what you're carrying first."
        # ... rest of logic
        return f"You now have the item {obj_name} in your inventory."
    return "There is no object that you can equip."
```

#### Adding new game objects
All game objects must inherit the GameObject base class (located in `entities.py`). 

example: 
```python
class NewObject(GameObject):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        # Add object-specific attributes
```

Interactive objects must implement the methods: (1) activate (2) deactivate (3) interact. Check out the other objects to see how they are implemented. Sometimes, they are not useful functions (e.g. you cannot activate a rock). 

#### Creating new puzzle levels
Level functions are defined in `levels.py`. Level functions must return a tuple of `(puzzle, available_actions)`. 

```python
def new_level():
    puzzle = GridPuzzle((width, height))
    # Add objects ... 

    available_actions = {
        "puzzle.action_name()": "Description of what the action does"
    }
    return puzzle, available_actions
```

You will also need to add them in the function `get_puzzle()`.

```python
def get_puzzle(level: int):
    puzzles = {
        1: level_one,
        2: level_two,
        3: your_new_level  # Increment the level + add your level function here
    }
    return puzzles[level]()
```


#### Adding new features
Adding new object types may introduce a lot of new complications to the GridPuzzle object. We want to keep things as simple as possible, but feel free to add new functions to the Puzzle() object. This will require more testing with the basic levels as well to make sure nothing has broken. 

1. Define object behavior and interactions
2. Add display character for grid visualization
3. Update utils.py print functions
4. Document available actions

#### Common patterns
The button currently works via weight based interactions: 

```python 
def on_enter(self, obj):
    weight = getattr(obj, 'weight', 0)
    return self.add_weight(weight)

def on_leave(self, obj):
    weight = getattr(obj, 'weight', 0)
    return self.remove_weight(weight)
```

Ensure that when the player moves, the environment is acting accordingly to those changes!

#### Testing new contributions
Some testing here is a bit hand-wavy. We want to make sure that the instructions are clear but also do not give too much away. 

1. First test if your puzzle is solveable. We do not currently have unsolveable puzzles in our plans.

2. Verify that all actions return strings. 

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that
> you have the necessary rights to the content and that the content you contribute may be provided
> under the project license.


#### Contributing Workflow
We actively welcome your pull requests!

1. Please create a new branch from main in your forked repo, with your username and a feature description. e.g. user-123/add-new-level. 

2. If necessary, please update the documentation. 

3. Please make sure your code lints.


### Contributing to Documentation
We would love valuable contributions in the form of new documentation or revised documentation that provide
further clarity or accuracy! 

### Code style 
- Please add Type hints
- Use clear variable names

# Questions?? 
Feel free to open an issue for: 
- clarification on requirements
- discussion of new features
- bug reports
- general questions

Remember: All puzzles should be challenging but solvable, and all actions should provide clear feedback through return strings!