# Expose the main components you want accessible when someone imports escaperoom
from .entities import GridPuzzle, Door, Button, Rock
from .runner import Runner  # assuming we renamed puzzle_session.py to runner.py
from .play import play
from .levels import *  

# This allows users to do:
# from link.puzzles.escaperoom import GridPuzzle, play
