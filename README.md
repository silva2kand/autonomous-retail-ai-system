# ai thatsilva

A universal, multilingual, spec-native AI IDE wi## Troubleshooting

If you get "Sorry, I encountered an error. Please try again.":

1. **Check Settings**: Ensure API provider and keys are set in VS Code Settings > "Spect Sun Armies Kit".
   - For OpenAI: API key required.
   - For Local/Ollama: Server must be running.
2. **Reload Extension**: Ctrl+Shift+P > "Developer: Reload Window".
3. **Debug Console**: Check for errors in Debug Console (F5 debug mode).
4. **For Sherpa**: Configure its own API settings separately.

The chat now provides detailed error messages and re-initializes the client on each request.

If "nothing working":

1. **Extension Not Loading**: Press F5 in VS Code to run in debug mode. Check the Debug Console for any errors during activation.
2. **Command Not Found**: Ensure the extension is activated. Check Output > Log (Window) for activation messages.
3. **API Errors**: Verify settings in VS Code Settings > Extensions > Spect Sun Armies Kit.
   - For OpenAI: Set API key.
   - For Local: Ensure server is running (e.g., `ollama serve`).
4. **Client Not Configured**: The extension will show an error if no valid config.
5. **Recompile**: Run `npm run compile` after changes.

For local models:erarchy.

## Features Implemented

- **Master Assistant AI**: Human interface for interpreting user input.
- **Master Agent**: Validates and orchestrates specs.
- **Manager Agent**: Breaks specs into modules.
- **Submanager Agents**: Handle domains like UI, backend.
- **Team Leader Agents**: Lead execution teams.
- **Mini AI Armies**: Execute features dynamically.
- **Notebook Memory System**: Logs all actions for context.
- **Auto-Scanning & Self-Healing**: Agents log and dissolve after tasks.
- **MCP Server**: Exposes agent tools via Model Context Protocol for integration with AI Toolkit.
- **VS Code Extension**: Spect Sun Armies Kit extension that transforms the editor into a runtime environment for the agent hierarchy.

## Setup

1. Install AI Toolkit extension in VS Code.
2. Set up Python environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set GITHUB_TOKEN environment variable.
6. Run standalone: `python main.py`
7. For MCP: Configure in AI Toolkit to use this server.
8. For VS Code Extension: Run `npm install` then `npm run compile`, then install the extension via VS Code (F5 to debug or package it).

## MCP Configuration

To integrate with AI Toolkit:

- Point AI Toolkit to `mcp_server.py` as the MCP server.
- Tools available: interpret_user_input, validate_spec, break_into_modules, spawn_submanager, spawn_team_leader, spawn_mini_army, execute_feature, get_notebook_logs.

## How to Test the Extension

Since this is a development version:

1. Open the extension folder in VS Code: `c:\Users\Siva\Documents\GitHub\ai-thatsilva`
2. Press **F5** to launch Extension Development Host
3. A new VS Code window opens with the extension loaded
4. In the new window:
   - Open Chat (Ctrl+Alt+I)
   - Select "Spect-Army-Kit" from participants
   - Chat should work now

If not working in the main window, it's because the extension isn't installed/published yet—F5 is required for testing.
- Configure APIs in VS Code Settings: Search for "Spect Sun Armies Kit"
  - Choose provider: OpenAI, Azure, Local (Ollama), GPT4All, Ollama
  - Set API keys, endpoints, models as needed
  - For local/GPT4All/Ollama: Ensure the server is running on the specified endpoint

## Supported APIs

- **OpenAI**: Standard API with custom base URL
- **Azure**: Azure AI endpoints
- **Local/Ollama**: OpenAI-compatible local servers (default port 11434)
- **GPT4All**: Local API (default port 4891)
- **Docker Small Models**: Run models in Docker containers and point to local endpoints

### Running Local Models with Docker

1. **Ollama in Docker**:

   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
   docker exec ollama ollama pull llama2  # or other small models
   ```

   Set provider to "ollama", endpoint to `http://localhost:11434/v1`

2. **GPT4All in Docker**: Check GPT4All docs for Docker setup, typically on port 4891.

## Troubleshooting

If "nothing working":

1. **Extension Not Loading**: Press F5 in VS Code to run in debug mode. Check Debug Console for errors.
2. **Command Not Found**: Ensure the extension is activated. Check Output > Log (Window) for activation messages.
3. **API Errors**: Verify settings in VS Code Settings > Extensions > Spect Sun Armies Kit.
   - For OpenAI: Set API key.
   - For Local: Ensure server is running (e.g., `ollama serve`).
4. **Client Not Configured**: The extension will show an error if no valid config.
5. **Recompile**: Run `npm run compile` after changes.

For local models:

- Ollama: Install Ollama, run `ollama serve`, pull a model.
- GPT4All: Install and start the API server.

If issues persist, check VS Code Developer Console (Help > Toggle Developer Tools) for errors.

## Usage

Modify `main()` in `main.py` to input your spec.

Supports all program types, languages, and features as per vision.
