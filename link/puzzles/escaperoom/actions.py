from enum import Enum 
from dataclasses import dataclass
from typing import Dict, Callable, Optional, Any
from link.puzzles.escaperoom.entities import GridPuzzle 

class ActionType(Enum):
    MOVE = "move"
    PICK_UP = "pick_up" # only objects
    DROP = "drop" # only objects
    
class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
        
@dataclass
class Action:
    type: ActionType
    params: Dict[str, Any]
    
    @classmethod
    def parse(cls, action_str: str) -> Optional['Action']:
        try:
            parts = action_str.lower().strip().split()
            if not parts:
                return None
                
            if parts[0] == ActionType.MOVE.value and len(parts) > 1:
                direction = Direction(parts[1])
                return cls(ActionType.MOVE, {"direction": direction})
                
            elif parts[0] == ActionType.PICK_UP.value and len(parts) > 1:
                object_name = parts[1]
                return cls(ActionType.PICK_UP, {"object": object_name})
                
            elif parts[0] == ActionType.DROP.value and len(parts) > 1:
                object_name = parts[1]
                return cls(ActionType.DROP, {"object": object_name})
                
        except (ValueError, IndexError):
            return None
        
        return None

    def __str__(self) -> str:
        if self.type == ActionType.MOVE:
            return f"move {self.params['direction'].value}"
        elif self.type in (ActionType.PICK_UP, ActionType.DROP):
            return f"{self.type.value} {self.params['object']}"
        return "invalid action"


class ActionHandler: 
    def __init__(self, puzzle: GridPuzzle): 
        self.puzzle = puzzle 
        self._setup_action_handlers()

    def _setup_action_handlers(self): 
        self.handlers: Dict[ActionType, Callable] = {
            ActionType.MOVE: self._handle_move, 
            ActionType.PICK_UP: self._handle_pick_up, 
            ActionType.DROP: self._handle_drop
        }
    
    def _handle_move(self, params: Dict[str, Any]) -> str: 
        direction = params['direction']
        return self.puzzle.move_player(direction.value)

    def _handle_pick_up(self, params: Dict[str, Any]) -> str: 
        object_name = params['object']
        return self.puzzle.equip(object_name)
    
    def _handle_drop(self, params: Dict[str, Any]) -> str: 
        object_name = params['object']
        return self.puzzle.drop(object_name)
    
    def execute(self, action_str: str) -> str: 
        action = Action.parse(action_str)

        if action is None: 
            return f"Invalid action format: {action_str}\n{self.get_action_help()}"
    
        if action.type not in self.handlers:
            return f"Unsupported action type {action.type}" 
    
        return self.handlers[action.type](action.params)
    
    def get_available_actions(self) -> list[str]: # maybe just reg str 
        current_objects = [obj.__class__.__name__.lower() for obj in self.puzzle.get_objects_at(self.puzzle.player)]

        inventory_object = (self.puzzle.player.inventory.__class__.__name__.lower() if self.puzzle.player.inventory else None)

        actions = []

        for direction in Direction: 
            actions.append(f"move {direction.value}")
        
        for obj in current_objects: 
            actions.append(f"pick_up {obj}")
        
        if inventory_object: 
            actions.append(f"drop {inventory_object}")
        
        return actions

    def get_action_help(self) -> str: 
        return """
Available actions: 
1. Movement: "move <direction>" where direction is up/down/left/right.
2. Pick up: "pick_up <object>" where same position as object.
3. Drop: "drop <object>" for object in inventory.

Examples: 
- move up 
- pick_up rock
- drop rock
"""