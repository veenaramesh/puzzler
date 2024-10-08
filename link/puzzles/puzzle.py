from typing import Dict, Tuple, List, Optional
from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, position: Tuple[int, int]):
        self.position = position

    @abstractmethod
    def interact(self, player):
        pass

class Button(GameObject):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.pressed = False

    def interact(self, player):
        self.pressed = True
        return "Button pressed"

    def unpress(self):
            if self.pressed:
                self.pressed = False
                return "Button unpressed"
            return "Button was not pressed"


class Door(GameObject):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.open = False

    def interact(self, player):
        if self.open:
            return "Door is already open"
        self.open = True
        return "Door opened"

class Laser(GameObject):
    def __init__(self, position: Tuple[int, int], direction: str):
        super().__init__(position)
        self.direction = direction

    def interact(self, player):
        return f"Laser pointing {self.direction}"

class Player:
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        self.inventory: List[str] = []

    def move(self, direction: str, grid_size: Tuple[int, int]):
        x, y = self.position
        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < grid_size[1] - 1:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < grid_size[0] - 1:
            x += 1
        else:
            return False
        self.position = (x, y)
        return True

class GridPuzzle:
    def __init__(self, grid_size: Tuple[int, int]):
        self.grid_size = grid_size
        self.player = Player((0, 0))
        self.objects: Dict[str, GameObject] = {}
        self.steps = 0

    def add_object(self, name: str, obj: GameObject):
        self.objects[name] = obj

    def move_player(self, direction: str):
        if self.player.move(direction, self.grid_size):
            self.steps += 1
            return self.check_position()
        return "Invalid move"

    def check_position(self):
        for name, obj in self.objects.items():
            if obj.position == self.player.position:
                return f"You are at {name}. {obj.interact(self.player)}"
            
            return f"You are at position {self.player.position}"

    def interact(self, object_name: str):
        obj = self.objects.get(object_name)
        if obj and obj.position == self.player.position:
            return obj.interact(self.player)
        return f"Cannot interact with {object_name}"

    def is_solved(self):
        door = next((obj for obj in self.objects.values() if isinstance(obj, Door)), None)
        return door and door.open and self.player.position == door.position

    def get_status(self):
        return f"Player at {self.player.position}, Inventory: {self.player.inventory}, Steps: {self.steps}"

# Example usage:
puzzle = GridPuzzle((3, 3))
puzzle.player.position = (2, 0)  # 1C in the original puzzle
puzzle.add_object("button", Button((1, 0)))  # 1B
puzzle.add_object("door", Door((2, 1)))  # 3B
puzzle.add_object("laser", Laser((0, 0), "up"))  # 1A

# Solve the puzzle
print(puzzle.player.position)
print(puzzle.move_player('left'))  # Move to 1B

print(puzzle.player.position)
print(puzzle.interact('button'))

print(puzzle.player.position)
print(puzzle.move_player('down'))  # Move to 2B

print(puzzle.player.position)
print(puzzle.move_player('down'))  # Move to 3B

print(puzzle.player.position)
print(puzzle.interact('door'))

print(puzzle.player.position)
print(puzzle.is_solved())

print(puzzle.player.position)
print(puzzle.get_status())