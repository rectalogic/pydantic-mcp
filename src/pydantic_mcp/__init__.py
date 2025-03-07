# Copyright (C) 2025 Andrew Wason
# SPDX-License-Identifier: MIT

import typing as t

from mcp import ClientSession
from mcp.types import Tool as MCPTool
from pydantic_ai import RunContext, Tool
from pydantic_ai.tools import ToolDefinition


async def mcptools(session: ClientSession) -> list[Tool]:
    await session.initialize()
    return [
        _initialize_tool(session, tool)
        # list_tools returns a PaginatedResult, but I don't see a way to pass the cursor to retrieve more tools
        for tool in (await session.list_tools()).tools
    ]


def _initialize_tool(session: ClientSession, mcp_tool: MCPTool) -> Tool:
    async def prepare_tool(ctx: RunContext, tool_def: ToolDefinition) -> ToolDefinition | None:
        tool_def.parameters_json_schema = mcp_tool.inputSchema
        return tool_def

    async def execute_tool(**kwargs: t.Any) -> t.Any:
        return await session.call_tool(mcp_tool.name, arguments=kwargs)

    return Tool(
        execute_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        takes_ctx=False,
        prepare=prepare_tool,
    )
