# Copyright (C) 2024 Andrew Wason
# SPDX-License-Identifier: MIT

import asyncio
import pathlib
import sys
import typing as t

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic_ai import Agent, Tool

from pydantic_mcp import MCPToolkit


async def run(tools: list[Tool], prompt: str) -> str:
    agent = Agent(model="groq:llama-3.1-8b-instant", tools=tools)  # requires GROQ_API_KEY
    result = await agent.run(prompt)
    return result.data


async def main(prompt: str) -> None:
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", str(pathlib.Path(__file__).parent.parent)],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            toolkit = MCPToolkit()
            tools = await toolkit.initialize(session)
            response = await run(tools, prompt)
            print(response)


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Read and summarize the file ./LICENSE"
    asyncio.run(main(prompt))
