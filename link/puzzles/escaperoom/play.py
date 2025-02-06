from link.puzzles.escaperoom.runner import Runner

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import fire 

def write_results_to_csv(results_list: List[Dict], output_dir: Path = Path("results")):
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = output_dir / f"puzzle_results_{timestamp}.csv"
    
    fieldnames = ['model', 'puzzle_level', 'total_steps', 'is_solved', 'num_iterations', 'conversation']
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_list)
    
    return filepath

def pretty_print_messages(messages: List[Dict[str, Any]]) -> None: 
    for message in messages: 
        print(f"Role: {message['role']}")
        content = message['content']
        print("-"*20) 

        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        print(f"Content: {content}")


def play(models: List[str] = ["openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"], puzzles: List[int] = [1], max_iterations:int=30, print_results=False): 
    all_results = []

    for model in models: 
        print(f"Testing {model}... ")
        for level in puzzles: 
            sess = Runner(model=model, puzzle_level=level)
            results = sess.run_eval(max_iterations=max_iterations)
            results.update({'model': model, 'puzzle_level': level})
            if print_results: 
                pretty_print_messages(results['conversation'])
            all_results.append(results)
    
    output_file = write_results_to_csv(all_results)
    print(f"Results written to {output_file}")
    return 

if __name__ == '__main__': 
    fire.Fire(play)
