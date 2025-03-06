# Copyright (C) 2025 Andrew Wason
# SPDX-License-Identifier: MIT
# type: ignore

from datetime import timezone

from dirty_equals import IsNow
from mcp.types import CallToolResult, TextContent
from pydantic_ai import Agent, capture_run_messages
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)
from pydantic_ai.models.test import TestModel


async def test_read_file(tools):
    agent = Agent(model=TestModel(), tools=tools)
    with capture_run_messages() as messages:
        await agent.run("Summarize the file a")

    expected = [
        ModelRequest(
            parts=[
                UserPromptPart(
                    content="Summarize the file a",
                    timestamp=IsNow(tz=timezone.utc),
                    part_kind="user-prompt",
                )
            ],
            kind="request",
        ),
        ModelResponse(
            parts=[ToolCallPart(tool_name="read_file", args={"path": "a"}, tool_call_id=None, part_kind="tool-call")],
            model_name="test",
            timestamp=IsNow(tz=timezone.utc),
            kind="response",
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name="read_file",
                    content=CallToolResult(
                        content=[
                            TextContent(
                                type="text", text="MIT License\n\nCopyright (c) 2025 Andrew Wason\n", annotations=None
                            )
                        ],
                        isError=False,
                    ),
                    tool_call_id=None,
                    timestamp=IsNow(tz=timezone.utc),
                    part_kind="tool-return",
                )
            ],
            kind="request",
        ),
        ModelResponse(
            parts=[
                TextPart(
                    content='{"read_file":{"_meta":null,"content":[{"type":"text","text":"MIT '
                    "License\\n\\nCopyright (c) 2025 Andrew "
                    'Wason\\n","annotations":null}],"isError":false}}',
                    part_kind="text",
                )
            ],
            model_name="test",
            timestamp=IsNow(tz=timezone.utc),
            kind="response",
        ),
    ]

    assert messages == expected
