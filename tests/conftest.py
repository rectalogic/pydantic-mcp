# Copyright (C) 2025 Andrew Wason
# SPDX-License-Identifier: MIT

from unittest import mock

import pytest
from mcp import ClientSession, ListToolsResult, Tool
from mcp.types import CallToolResult, TextContent

from pydantic_mcp import mcptools


@pytest.fixture
def session(request):
    session_mock = mock.AsyncMock(spec=ClientSession)
    session_mock.list_tools.return_value = ListToolsResult(
        tools=[
            Tool(
                name="read_file",
                description=(
                    "Read the complete contents of a file from the file system. Handles various text encodings "
                    "and provides detailed error messages if the file cannot be read. "
                    "Use this tool when you need to examine the contents of a single file. "
                    "Only works within allowed directories."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                    "additionalProperties": False,
                    "$schema": "http://json-schema.org/draft-07/schema#",
                },
            )
        ]
    )
    session_mock.call_tool.return_value = CallToolResult(
        content=[TextContent(type="text", text="MIT License\n\nCopyright (c) 2025 Andrew Wason\n")],
        isError=False,
    )
    yield session_mock


@pytest.fixture
async def tools(session):
    yield await mcptools(session)
    session.call_tool.assert_called_with("read_file", arguments={"path": "a"})
