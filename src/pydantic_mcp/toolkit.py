# Copyright (C) 2025 Andrew Wason
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

import pydantic_core
import typing_extensions as t
from mcp import ClientSession
from mcp.types import EmbeddedResource, ImageContent, TextContent
from mcp.types import Tool as MCPTool
from pydantic_ai import RunContext, Tool
from pydantic_ai.tools import ToolDefinition


class MCPToolkit:
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
            return ToolDefinition(
                name=mcp_tool.name, description=mcp_tool.description or "", parameters_json_schema=mcp_tool.inputSchema
            )

        async def execute(*args, **kwargs):
            result = await session.call_tool(mcp_tool.name, arguments=kwargs)
            if result.isError:
                # XXX how to handle errors?
                raise RuntimeError(pydantic_core.to_json(result.content).decode())
            text_content = [block for block in result.content if isinstance(block, TextContent)]
            artifacts = [block for block in result.content if not isinstance(block, TextContent)]
            return pydantic_core.to_json(text_content).decode(), artifacts

        return Tool(
            execute, name=mcp_tool.name, description=mcp_tool.description or "", takes_ctx=False, prepare=prepare
        )
