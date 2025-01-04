from typing import Tuple, List
from abc import ABC

class GameObject(ABC):
    def __init__(self, position: Tuple[int, int]):
        self.nickname = ""
        self.position = position

    def set_position(self, new_position): 
        self.position = new_position
        return self.position


class Door(GameObject):
    def __init__(self, position: Tuple[int, int]):
        super().__init__(position)
        self.open = False
        self.description = f"There is a simple door."

    def activate(self):
        self.open = True

    def deactivate(self):
        self.open = False

    def interact(self, player):
        if player.position == self.position: 
            if self.open:
                return "You pass through the open door."
            else:
                return "The door is closed. Find a way to open it."
        else: 
            return "You are too far away to interact with the door."

# interactables
class Button(GameObject):
    def __init__(self, position: Tuple[int, int], linked_objects: List[GameObject], weight_threshold: int = 50):
        super().__init__(position)
        self.pressed = False
        self.linked_objects = linked_objects
        self.weight_threshold = weight_threshold
        self.current_weight = 0
        self.description = "There is a button on the floor. You can press it"

    def add_weight(self, weight):
        self.current_weight += weight
        if not self.pressed and self.current_weight >= self.weight_threshold:
            return self.press()
        return None

    def remove_weight(self, weight):
        self.current_weight = max(0, self.current_weight - weight)
        if self.pressed and self.current_weight < self.weight_threshold:
            return self.unpress()
        return None

    def on_enter(self, obj):
        weight = getattr(obj, 'weight', 0)
        return self.add_weight(weight)
    
    def on_leave(self, obj):
        weight = getattr(obj, 'weight', 0)
        return self.remove_weight(weight)

    def press(self):
        if not self.pressed:
            self.pressed = True
            for obj in self.linked_objects:
                if hasattr(obj, 'activate'):
                    obj.activate()
            return "The button sinks under the weight. You hear a click. The button is pressed."
        return None

    def unpress(self):
        if self.pressed:
            self.pressed = False
            for obj in self.linked_objects:
                if hasattr(obj, 'deactivate'):
                    obj.deactivate()
            return "The button rises as the weight is removed. You hear another click. The button is unpressed."
        return None    

# Objects
class Rock(GameObject):
    def __init__(self, position: Tuple[int, int], weight: int = 100):
        super().__init__(position)
        self.weight = 100 # pounds

# Obstacle     
# class Laser(GameObject): 
#     def __init(self, position: Tuple[int, int], direction): 
#         super().__init__(position)
#         self.direction = direction 

#     def define_obstacle_path(self, grid_size, objects): 
#         for o in objects: 
#             if self.direction == "left": 
#                 impacted_points = [self.position.]

# Player
class Player:
    def __init__(self, position: Tuple[int, int]):
        self.position = position
        # later, we can have a maximum weight in inventory
        self.inventory: GameObject = None
        self.weight = 150

    def move(self, direction: str, grid_size: Tuple[int, int]):
        x, y = self.position
        if direction == 'up' and y < grid_size[1] - 1:
            y += 1
        elif direction == 'down' and y > 0:
            y -= 1
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
        self.objects: List[GameObject] = []
        self.steps = 0

    # set up puzzle 
    def add_object(self, obj: GameObject):
        self.objects.append(obj)

    def get_objects_at(self, position: Tuple[int, int]) -> List[GameObject]:
        return [obj for obj in self.objects if obj.position == position]

    def get_object_by_name(self, name: str): 
        if self.player.inventory and self.player.inventory.__class__.__name__.lower() == name.lower():
            return self.player.inventory
        
        # only looking at the player position: !!!
        return next((obj for obj in self.get_objects_at(self.player.position) 
                    if obj.__class__.__name__.lower() == name.lower()), None)

    # ACTIONS # 
    def equip(self, obj_name: str): 
        obj = self.get_object_by_name(obj_name)
        if obj: 
            for o in self.get_objects_at(self.player.position): 
                if isinstance(o, Button):
                    o.remove_weight(getattr(obj, 'weight', 0))

            if self.player.inventory:
                return "Your hands are full! Drop what you're carrying first."

            self.player.inventory = obj
            self.objects.remove(obj)

            return f"You now have the item {obj_name} in your inventory."
        else: 
            return "There is no object that you can equip. "

    def drop(self, obj_name: str): 
        if not self.player.inventory: 
            return "You are not carrying anything. "
        
        obj = self.get_object_by_name(obj_name)
        if self.player.inventory.__class__.__name__.lower() != obj_name.lower():
            return f"You aren't carrying a {obj_name}"
        
        for o in self.get_objects_at(self.player.position): 
            if isinstance(o, Button):
                o.add_weight(getattr(obj, 'weight', 0))

        self.player.inventory = None
        obj.set_position(self.player.position)
        self.objects.append(obj)
        return f"You have dropped the {obj_name}. It is no longer in your inventory. " 

    def move_player(self, direction: str):
        old_position = self.player.position
        if self.player.move(direction, self.grid_size):
            self.steps += 1
            return self.handle_player_movement(old_position, self.player.position)
        return "Invalid move"
        
    def handle_player_movement(self, old_position: Tuple[int, int], new_position: Tuple[int, int]):
        results = []

        # Handle leaving the old position
        for obj in self.get_objects_at(old_position):
            if hasattr(obj, 'on_leave'):
                result = obj.on_leave(self.player)
                if result:
                    results.append(result)

        # Handle entering the new position
        for obj in self.get_objects_at(new_position):
            if hasattr(obj, 'on_enter'):
                result = obj.on_enter(self.player)
                if result:
                    results.append(result)

        return "\n".join(results) if results else f"Moved to {new_position}"

    def interact(self, obj):
        return obj.interact(self.player)

    # check result 
    def is_solved(self):
        door = next((obj for obj in self.objects if isinstance(obj, Door)), None)
        return door and door.open and self.player.position == door.position

    def get_status(self):
        return f"Player at {self.player.position}, Steps: {self.steps}, Inventory: {self.player.inventory}"
    