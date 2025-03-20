# AgentDir

AgentDir is an AI-powered file and directory management system built using the DSPy framework. It leverages Gemini 2.0 Flash LLM to understand natural language commands for file organization and management tasks.

## Features

- **Intelligent File Organization**: Process natural language commands to organize files and directories
- **Comprehensive File Operations**: Create, remove, copy, move, rename directories and files
- **Directory Navigation**: List directory contents with detailed information
- **Reactive Agent Design**: Uses DSPy's ReAct framework for reasoning and action execution

![alt text](images/image.png)

## Prerequisites

- Python 3.8+
- DSPy
- Google API key for Gemini 2.0 Flash

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/AgentDir.git
cd AgentDir
```

2. Install required dependencies:
```bash
pip install dspy-ai google-generativeai
```

3. Set up your Google API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/)
   - Add it to the configuration in main.py or set as environment variable

## Usage

Run the main script to start the agent:

```bash
python main.py
```

By default, the agent will:
1. Create a test environment directory
2. Change to that directory
3. Execute the task "organize all file in the directory"

### Example Commands

You can modify the `task` variable in `main.py` to perform different operations:

- "Create a new directory called 'documents'"
- "Move all text files to the documents folder"
- "List all files in the current directory"
- "Rename file1.txt to important_notes.txt"

## Project Structure

- **main.py**: Entry point for the application, configures DSPy and defines the AgentDIR class
- **agent_tools.py**: Contains utility functions for file and directory operations

## Available Tools

The agent has access to the following file operation tools:

| Function | Description |
|----------|-------------|
| `create_dir` | Create a directory (with parent directories as needed) |
| `remove_dir` | Remove a directory (with optional recursive deletion) |
| `list_dir` | List contents of a directory with detailed information |
| `get_current_dir` | Get the current working directory |
| `copy_file` | Copy a file or directory to a new location |
| `move_file` | Move a file or directory to a new location |
| `remove_file` | Delete a file from the filesystem |
| `rename` | Rename a file or directory |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [DSPy](https://github.com/stanfordnlp/dspy)
- [Google Gemini AI](https://deepmind.google/technologies/gemini/)
