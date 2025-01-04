from link.puzzles.escaperoom.entities import GridPuzzle
import link.puzzles.escaperoom.levels as levels 

from typing import Dict
import re 
import aisuite as ai
from link.puzzles.escaperoom.utils import print_puzzle_state, print_available_actions, print_object_state, print_player_state

SYSTEM_PROMPT = """Goal: Your goal is to reach and open the door ('D').

Rules:
    1. You can move on the grid using up/down/left/right actions. 
    2. You can only pick up or drop objects when you are at their position (same x,y coordinates). 
    3. Rocks ('R') can be equipped.
    4. A pressed button opens the door ('d' becomes 'D'). 
    5. Respond with one available action at a time. 
    6. Do not send any other information. Only send the available action. 

Hints: 
    1. Plan moves in advance. 
    2. Think about objects in the room. 
    3. Think about the order of actions.
"""

class Runner:
    def __init__(self: str = "", model: str = "openai:gpt-4o", puzzle_level: int=1):
        self.client = ai.Client() #OpenAI(api_key=api_key)
        self.model = model
        self.puzzle, self.available_actions = levels.get_puzzle(puzzle_level)
        self.system_prompt = self.get_prompt(self.puzzle, self.available_actions)
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]

    def get_prompt(self, puzzle: GridPuzzle, available_actions: Dict) -> str:
        return SYSTEM_PROMPT + '\n' + print_puzzle_state(puzzle) + '\n' + print_object_state(puzzle) + '\n' + print_player_state(puzzle) + '\n' + print_available_actions(available_actions)

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})
    
    def get_llm_response(self) -> str:
        messages = self.conversation_history
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages, 
            temperature=0.5
        )
        content = response.choices[0].message.content
        self.add_to_history("assistant", content)
        print(f"LLM: {content}")
        return content

    def send_message(self, message: str) -> str:
        print(f"PUZZLE: {message}")
        self.add_to_history("user", message)
        return self.get_llm_response()
        
    def interact_with_puzzle(self, response):
        matches = re.findall(r'puzzle\.[a-zA-Z_]+\([^)]*\)', response)
        for match in matches:
            try: 
                response = eval('self.' + match)
                return response
            except Exception as e: 
                raise ValueError("Invalid action encountered: " + match)
        return 0
    
    def should_continue(self) -> bool:
        return not self.puzzle.is_solved()
    
    def return_results(self, iteration):
        results = {
            'total_steps': self.puzzle.steps,
            'is_solved': self.puzzle.is_solved(),
            'num_iterations': iteration,
            'conversation': self.conversation_history
        }
        return results        
    
    def run_eval(self, max_iterations: int = 30) -> str:        
        iteration = 0
        response = self.get_llm_response()
        while iteration < max_iterations:
            # use latest response 
            description = self.interact_with_puzzle(response)
            #next_question = self.process_puzzle_state()
            response = self.send_message(description)
            if not self.should_continue():
                break
            iteration += 1
        #print(self.conversation_history)

        return self.return_results(iteration)
    
