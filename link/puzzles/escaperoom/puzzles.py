from escaperoom import GridPuzzle, Door, Button, Rock

# Function to display the puzzle state
def display_puzzle_state(puzzle):
    grid = [['.' for _ in range(puzzle.grid_size[0])] for _ in range(puzzle.grid_size[1])]

    for obj in puzzle.objects:
        if isinstance(obj, Door):
            grid[obj.position[1]][obj.position[0]] = 'D' if obj.open else 'd'
        elif isinstance(obj, Button):
            grid[obj.position[1]][obj.position[0]] = 'B' if obj.pressed else 'b'
        elif isinstance(obj, Rock):
            grid[obj.position[1]][obj.position[0]] = 'R'

    grid[puzzle.player.position[1]][puzzle.player.position[0]] = 'P'

    for row in reversed(grid):
        print(' '.join(row))
    print(puzzle.get_status())

def level_one(): 
    # Solution:
    # print(puzzle.move_player('up'))
    # print(puzzle.move_player('up'))
    # print(puzzle.equip(rock))
    # print(puzzle.move_player('right')) 
    # print(puzzle.move_player('down'))    
    # puzzle.drop(rock)
    # print(puzzle.move_player('right'))
    # print(puzzle.move_player('down'))     
    # print(puzzle.interact(door))      

    door = Door((2, 0))
    button = Button((1, 1), [door], weight_threshold=90)  # Will stay pressed with rock, but not just player
    rock = Rock((0, 2), weight=100)

    puzzle = GridPuzzle((3, 3))
    puzzle.add_object(door)
    puzzle.add_object(button)
    puzzle.add_object(rock)
    
    available_actions = {
        "puzzle.get_status()": "Will not impact number of steps. Shows you position, inventory items, and number of steps so far", 
        "puzzle.is_solved()": "Will not impact number of steps. Checks if it is solved.",
        "puzzle.move_player('up')": "Will move player one spot forward in the y axis.", 
        "puzzle.move_player('down')": "Will move player one spot backward in the y axis.", 
        "puzzle.move_player('left')": "Will move player one spot forward in the x axis.", 
        "puzzle.move_player('right')": "Will move player one spot backward in the x axis.", 
        "puzzle.equip(rock)": "Will allow player to equip rock.", 
        "puzzle.drop(rock)": "Will allow player to unequip rock."
    }
    return puzzle, available_actions

def level_two(): 
    # Solution: 

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

    available_actions = {
        "puzzle.get_status()": "Will not impact number of steps. Shows you position, inventory items, and number of steps so far", 
        "puzzle.is_solved()": "Will not impact number of steps. Checks if it is solved.",
        "puzzle.move_player('up')": "Will move player one spot forward in the y axis.", 
        "puzzle.move_player('down')": "Will move player one spot backward in the y axis.", 
        "puzzle.move_player('left')": "Will move player one spot forward in the x axis.", 
        "puzzle.move_player('right')": "Will move player one spot backward in the x axis.", 
        "puzzle.equip(rock)": "Will allow player to equip rock.", 
        "puzzle.drop(rock)": "Will allow player to unequip rock."
    }

    return puzzle, available_actions

