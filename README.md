# THE PUZZLER LLM EVALS 
### Objective
A framework for evaluating how well Large Language Models can handle puzzle-solving tasks. The goal of this project is to not only understand how LLMs perform at a single level, but understand how the solution to one puzzle can influence the solution to a next puzzle. 

We currently only have two puzzles. 

### Quick Start
We use `aisuite` in the backend to define the LLM interactions. Therefore, we are currently limited by the models currently offered through the `aisuite` package. To understand how to authenticate and define the models, please look at the [aisuite package](https://github.com/andrewyng/aisuite/tree/main/aisuite). 

```
from link.puzzles.escaperoom.play import play

# Test multiple models on multiple levels
play(
    models=["openai:gpt-4o", "anthropic:claude-3-5-sonnet-20240620"],
    puzzles=[1, 2],
    max_iterations=30 # max iterations per model before timing out
)
```

### How to: 
The LLM gets a description of the puzzle rules and state (current locations of the objects in the puzzle, etc.) We ask the LLM to respond with pre-defined available actions, like moving around the grid, equipping and unequipping up objects, and checking the state of the grid. 

After a run, we write everything to a CSV file, so you can compare and analyze solution paths. There is a lot of room to improve here; currently, its fairly naive (we write the entire conversation history down with some basic metadata). More updates to come. 

