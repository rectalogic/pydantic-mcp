# Copyright (C) 2025 Andrew Wason
# SPDX-License-Identifier: MIT

import typing as t

from mcp import ClientSession
from mcp.types import Tool as MCPTool
from pydantic_ai import RunContext, Tool
from pydantic_ai.tools import ToolDefinition


class Toolkit:
    """
    MCP server toolkit
    """

    async def initialize(self, session: ClientSession) -> list[Tool]:
        """Initialize the session and retrieve tools list"""
        await session.initialize()
        return [
            self._initialize_tool(session, tool)
            # list_tools returns a PaginatedResult, but I don't see a way to pass the cursor to retrieve more tools
            for tool in (await session.list_tools()).tools
        ]

    def _initialize_tool(self, session: ClientSession, mcp_tool: MCPTool) -> Tool:
        async def prepare(ctx: RunContext, tool_def: ToolDefinition) -> ToolDefinition | None:
            tool_def.parameters_json_schema = mcp_tool.inputSchema
            return tool_def

        async def execute(**kwargs) -> t.Any:
            return await session.call_tool(mcp_tool.name, arguments=kwargs)

        return Tool(
            execute, name=mcp_tool.name, description=mcp_tool.description or "", takes_ctx=False, prepare=prepare
        )
