# pydantic-mcp

![PyPI - Version](https://img.shields.io/pypi/v/pydantic-mcp)

[Model Context Protocol](https://modelcontextprotocol.io) tool calling support in [Pydantic AI](https://ai.pydantic.dev/).

Create a `pydantic_mcp.Toolkit` and initialize it
`tools = await toolkit.initialize(session)` with an `mcp.ClientSession`
to get a list of `pydantic_mcp.Tool` instances for the supported tools.

Example:

https://github.com/rectalogic/pydantic-mcp/blob/09ddba23118e74003821dd996b094e8b92f79a36/tests/demo.py#L15-L26

## Demo

You can run the demo against [Groq](https://groq.com/) `llama-3.1-8b-instant`:
```sh-session
$ export GROQ_API_KEY=xxx
$ uv run tests/demo.py "Read and summarize the file ./LICENSE"
Secure MCP Filesystem Server running on stdio
Allowed directories: [ '/users/aw/projects/rectalogic/langchain-mcp' ]
The file ./LICENSE is a MIT License agreement. It states that the software is provided "as is" without warranty and that the authors and copyright holders are not liable for any claims, damages, or other liability arising from the software or its use.
```
