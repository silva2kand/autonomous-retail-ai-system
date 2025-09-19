import asyncio
import json
import os
from typing import Any, Sequence
from mcp import Tool
from mcp.server import Server
from mcp.types import TextContent, PromptMessage
import mcp.server.stdio

# Import our agents
from main import MasterAssistantAI, MasterAgent, ManagerAgent, SubmanagerAgent, TeamLeaderAgent, MiniAIArmy, notebook

server = Server("agentic-ide-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="interpret_user_input",
            description="Interpret user natural language input into a spec",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_input": {"type": "string"}
                },
                "required": ["user_input"]
            }
        ),
        Tool(
            name="validate_spec",
            description="Validate a spec for structure and feasibility",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec": {"type": "string"}
                },
                "required": ["spec"]
            }
        ),
        Tool(
            name="break_into_modules",
            description="Break spec into modules",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec": {"type": "string"}
                },
                "required": ["spec"]
            }
        ),
        Tool(
            name="spawn_submanager",
            description="Spawn a submanager for a domain",
            inputSchema={
                "type": "object",
                "properties": {
                    "domain": {"type": "string"}
                },
                "required": ["domain"]
            }
        ),
        Tool(
            name="spawn_team_leader",
            description="Spawn team leader for module",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string"}
                },
                "required": ["module_name"]
            }
        ),
        Tool(
            name="spawn_mini_army",
            description="Spawn mini AI army for feature",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature": {"type": "string"}
                },
                "required": ["feature"]
            }
        ),
        Tool(
            name="execute_feature",
            description="Execute a feature using mini army",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature": {"type": "string"}
                },
                "required": ["feature"]
            }
        ),
        Tool(
            name="get_notebook_logs",
            description="Get all logged actions from notebook memory",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    if name == "interpret_user_input":
        assistant = MasterAssistantAI()
        result = assistant.interpret_user_input(arguments["user_input"])
        assistant.dissolve()
        return [TextContent(type="text", text=result)]
    elif name == "validate_spec":
        master = MasterAgent()
        valid = master.validate_spec(arguments["spec"])
        master.dissolve()
        return [TextContent(type="text", text=str(valid))]
    elif name == "break_into_modules":
        manager = ManagerAgent()
        modules = manager.break_into_modules(arguments["spec"])
        manager.dissolve()
        return [TextContent(type="text", text=json.dumps(modules))]
    elif name == "spawn_submanager":
        submanager = SubmanagerAgent(arguments["domain"])
        return [TextContent(type="text", text=f"Spawned {submanager.name}")]
    elif name == "spawn_team_leader":
        team_leader = TeamLeaderAgent(arguments["module_name"])
        return [TextContent(type="text", text=f"Spawned {team_leader.name}")]
    elif name == "spawn_mini_army":
        mini_army = MiniAIArmy(arguments["feature"])
        return [TextContent(type="text", text=f"Spawned {mini_army.name}")]
    elif name == "execute_feature":
        mini_army = MiniAIArmy(arguments["feature"])
        result = mini_army.execute_feature()
        mini_army.dissolve()
        return [TextContent(type="text", text=result)]
    elif name == "get_notebook_logs":
        logs = notebook.get_history()
        return [TextContent(type="text", text=json.dumps(logs))]
    else:
        return [TextContent(type="text", text="Unknown tool")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())