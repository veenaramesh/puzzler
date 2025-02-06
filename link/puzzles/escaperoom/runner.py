from link.puzzles.escaperoom.actions import ActionHandler
from link.puzzles.escaperoom.entities import GridPuzzle
import link.puzzles.escaperoom.levels as levels 

from typing import Dict
import re 
import aisuite as ai
from link.puzzles.escaperoom.utils import print_puzzle_state, print_available_actions, print_object_state, print_player_state

SYSTEM_PROMPT = """Goal: Your goal is to reach and open the door.

Rules:
    1. You can move on the grid using the 'move' command followed by a direction (up/down/left/right)
    2. You can pick up objects when you are at their position using 'pick_up' followed by the object name
    3. You can drop objects from your inventory using 'drop' followed by the object name
    4. A pressed button opens the door
    5. Respond with one available action at a time
    6. Only send the available action

Example actions:
    - move up
    - move down
    - pick_up rock
    - drop rock

Currently available actions:
{available_actions}

Current State:
{state}
"""

class Runner:
    def __init__(self: str = "", model: str = "openai:gpt-4o", puzzle_level: int=1):
        self.client = ai.Client() #OpenAI(api_key=api_key)
        self.model = model
        self.level = levels.get_level(puzzle_level)
        self.puzzle, self.available_actions = self.level.get_level()
        self.action_handler = ActionHandler(self.puzzle)
        self.conversation_history = []
        self._initialize_conversation() 
    
    def _initialize_conversation(self): 
        # could also reset conversation if needed
        initial_state = self._get_current_state()
        system_message = SYSTEM_PROMPT.format(
            available_actions=self.action_handler.get_available_actions(), 
            state=initial_state
        )
        self.conversation_history = [{"role": "system", "content": system_message}]

    def _get_current_state(self): 
        return "\n".join([
            print_puzzle_state(self.puzzle), 
            print_object_state(self.puzzle), 
            print_player_state(self.puzzle)
        ])
    
    def get_llm_response(self) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history, 
            temperature=0.5
        )
        content = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": content})
        print(f"LLM Action: {content}")
        return content

    def send_message(self, message: str) -> str:
        print(f"Game State update: {message}")
        self.conversation_history.append({"role": "assistant", "content": message})
        return self.get_llm_response()
             
    
    def run_eval(self, max_iterations: int = 30) -> dict:        
        iteration = 0
        action = self.get_llm_response()
        while iteration < max_iterations:
            result = self.action_handler.execute(action)

            if self.puzzle.is_solved(): 
                break 

            action = self.send_message(result)
            iteration += 1
        #print(self.conversation_history)

        return {
            'total_steps': self.puzzle.steps, 
            'is_solved': self.puzzle.is_solved(), 
            'num_iterations': iteration, 
            'conversation': self.conversation_history
        }
    
