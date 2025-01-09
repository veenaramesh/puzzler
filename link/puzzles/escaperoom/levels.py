from abc import ABC, abstractmethod
from typing import Dict, Tuple, List
from link.puzzles.escaperoom.entities import GridPuzzle, Door, Button, Rock

class BaseLevel(ABC):
    def __init__(self):
        self.puzzle: GridPuzzle = None
        self.available_actions: Dict[str, str] = {}
        self.prerequisites: List[BaseLevel] = []
        self._setup_puzzle()
        self._setup_actions()

    @abstractmethod
    def _setup_puzzle(self):
        pass

    @abstractmethod
    def _setup_actions(self):
        pass

    def get_level(self) -> Tuple[GridPuzzle, Dict[str, str]]:
        return self.puzzle, self.available_actions

    @property
    def grid_size(self) -> Tuple[int, int]:
        return self.puzzle.grid_size if self.puzzle else (0, 0)

    def validate_solution(self) -> bool:
        return self.puzzle.is_solved()

class LevelOne(BaseLevel):
    def __init__(self):
        super().__init__()
        
    def _setup_puzzle(self):
        self.puzzle = GridPuzzle((3, 3))
        
        door = Door((2, 0))
        button = Button((1, 1), [door], weight_threshold=90)
        rock = Rock((0, 2), weight=100)
        
        self.puzzle.add_object(door)
        self.puzzle.add_object(button)
        self.puzzle.add_object(rock)

    def _setup_actions(self):
        self.available_actions = {
            "puzzle.get_status()": "Shows position, inventory items, and steps",
            "puzzle.is_solved()": "Checks if puzzle is solved",
            "puzzle.move_player('up')": "Move up one space",
            "puzzle.move_player('down')": "Move down one space",
            "puzzle.move_player('left')": "Move left one space",
            "puzzle.move_player('right')": "Move right one space",
            "puzzle.equip('rock')": "Pick up rock if at same position",
            "puzzle.drop('rock')": "Drop currently held rock"
        }

    def get_solution(self): 
        return "Move to the rock, pick it up, move to the button, drop the rock on the button to keep the button pressed, move to the door" 
    
    
class LevelTwo(BaseLevel):
    def _setup_puzzle(self):
        puzzle = GridPuzzle((4, 4))  # Larger grid for more complexity

        # Create objects
        door = Door((3, 3))
        button1 = Button((1, 1), [door], weight_threshold=90)  # Connected to the door
        button2 = Button((2, 2), [], weight_threshold=90)  # Not connected to anything
        rock1 = Rock((0, 2), weight=100)

        # Add objects to the puzzle
        puzzle.add_object(door)
        puzzle.add_object(button1)
        puzzle.add_object(button2)
        puzzle.add_object(rock1)

    def _setup_actions(self):
        self.available_actions = {
            "puzzle.get_status()": "Will not impact number of steps. Shows you position, inventory items, and number of steps so far", 
            "puzzle.is_solved()": "Will not impact number of steps. Checks if it is solved.",
            "puzzle.move_player('up')": "Will increase y coordinate by 1", 
            "puzzle.move_player('down')": "Will decrease y coordinate by 1", 
            "puzzle.move_player('left')": "Will decrease x coordinate by 1", 
            "puzzle.move_player('right')": "Will increase x coordinate by 1", 
            "puzzle.equip('rock')": "Will allow player to equip rock.", 
            "puzzle.drop('rock')": "Will allow player to unequip rock."
            }



def get_level(level_number: int) -> BaseLevel:
    levels = {
        1: LevelOne,
        2: LevelTwo
    }

    if level_number not in levels:
        raise ValueError(f"Level {level_number} does not exist. ")
    return levels[level_number]()