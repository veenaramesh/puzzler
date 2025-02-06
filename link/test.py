from typing import List
import argparse
import os 

from link.puzzles.escaperoom.play import play

CURRENT_PUZZLES = ['escaperoom']

def main(tests: List[str], model: List[str], print_results:bool):
    for test in tests:
        if test == "escaperoom":
            play(models=model, print_results=print_results)
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests')
    parser.add_argument('--tests', nargs='+', default=["escaperoom"], choices=CURRENT_PUZZLES, help="Tests that we currently have available to run.")
    parser.add_argument('--models', nargs='+', default=["openai:gpt-4o"], help="Models to test. Current models are limited by models provided by andrewyng/aisuite.")
    parser.add_argument('--print', action='store_true', help="Set if you want to print out conversations. Useful for debugging.")
    args = parser.parse_args()
    main(args.tests, args.models, args.print)
    #main(["escaperoom"], ["openai:gpt-4o"])