# AI Personal Assistant Agent

## Overview

This project implements an adaptive AI agent using the Google Gemini API.  
The agent runs in a command-line interface (CLI) and can understand user input, maintain conversation context, and decide when to use external tools.

The system is designed using software engineering principles such as separation of concerns and modular architecture.

## Features

- Natural language interaction with the user
- Maintains conversation memory within a session
- Uses external tools when needed
- Handles errors without crashing

## Architecture

The system is divided into the following components:

- `Agent` - controls the main loop (Reason -> Act -> Observe)
- `MemoryManager` - stores conversation history
- `ToolRegistry` - registers and executes tools
- `BaseTool` - defines a common interface for all tools

This structure follows SOLID principles and avoids tightly coupled code.

## Design Patterns Used

- `Strategy Pattern` - each tool acts as a strategy that can be selected dynamically
- `Registry Pattern` - tools are stored and accessed through a registry
- `ReAct Pattern` - the agent follows a reasoning loop:
  - Reason -> decide what to do
  - Act -> call tool if needed
  - Observe -> return result

## Tools Implemented

The agent supports the following tools:

- Calculator Tool - evaluates mathematical expressions
- Time Tool - returns current date and time
- Currency Tool - converts currencies using a public API
- Dictionary Tool - retrieves word meanings using an online dictionary API

## Installation

1. Install dependencies:

```bash
pip install google-genai requests python-dotenv
```

2. Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_api_key_here
```

3. Run the application:

```bash
python main.py
```

## Example Usage

```text
You: what is 5 + 3
Agent: 8

You: convert 100 USD to EUR
Agent: 92 EUR

You: define algorithm
Agent: a step-by-step procedure for solving a problem
```

## Notes

- The agent uses the Gemini API for reasoning and tool selection
- External APIs are used for real-time data such as currency conversion and dictionary lookup
- The system is designed to be easily extended with new tools

## Conclusion

This project demonstrates how AI agents can be built using structured software architecture, combining LLM reasoning with external tool execution in a modular and maintainable way.
