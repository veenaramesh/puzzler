from link.puzzles.escaperoom.entities import GridPuzzle, Door, Button, Rock
from typing import List, Dict
import csv
import json 

# print functions to display the puzzle state
def print_puzzle_state(puzzle: GridPuzzle) -> str:
    display_str = []
    grid = [['.' for _ in range(puzzle.grid_size[0])] for _ in range(puzzle.grid_size[1])]

    for obj in puzzle.objects:
        if isinstance(obj, Door):
            grid[obj.position[1]][obj.position[0]] = 'D' if obj.open else 'd'
        elif isinstance(obj, Button):
            grid[obj.position[1]][obj.position[0]] = 'B' if obj.pressed else 'b'
        elif isinstance(obj, Rock):
            grid[obj.position[1]][obj.position[0]] = 'R'

    grid[puzzle.player.position[1]][puzzle.player.position[0]] = 'P'

    display_str.append("Puzzle State: ")
    display_str.append("Legend: P=Player, d=Closed Door, D=Open Door, b=Unpressed Button, B=Pressed Button, R=Rock")

    for row in reversed(grid):
        display_str.append(' '.join(row))

    return '\n'.join(display_str)

def print_object_state(puzzle: GridPuzzle) -> str: 
    display_str = []
    display_str.append("Objects in puzzle:")

    for obj in puzzle.objects: 
        if isinstance(obj, Door):
            display_str.append(f"- Door at {obj.position}: {'Open' if obj.open else 'Closed'}")
        elif isinstance(obj, Button):
            display_str.append(f"- Button at {obj.position}: {'Pressed' if obj.pressed else 'Unpressed'}")
            display_str.append(f"  Weight threshold: {obj.weight_threshold}")
        elif isinstance(obj, Rock):
            display_str.append(f"- Rock at {obj.position}: Weight={obj.weight}")
    
    return '\n'.join(display_str)

def print_player_state(puzzle: GridPuzzle) -> str: 
    display_str = []
    display_str.append("Player Status:")
    display_str.append(puzzle.get_status())

    return '\n'.join(display_str)

def print_available_actions(available_actions: Dict) -> str:
    display_str = [] 
    display_str.append('Available Actions:')
    for action, description in available_actions.items():
        display_str.append(f"- {action}: {description}")
    
    return "\n".join(display_str)
