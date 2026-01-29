import asyncio
import os
import sys
import ollama

from mcp.server import FastMCP
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters




mcp = FastMCP("CodeExplainerTool")

@mcp.tool()
def read_code_file(path: str) -> str:
    """Read a code file and return its content."""

    # Normalize Windows path issues
    path = path.strip().replace("\\", "/")

    if not os.path.isfile(path):
        return f"Error: File not found -> {path}"

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


# -------------------- CLIENT LOGIC --------------------

async def run_client():
    print("Starting MCP client...\n")

    server_params = StdioServerParameters(
        command="python",
        args=[__file__, "server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            file_path = input("Enter full file path to explain: ").strip()

            result = await session.call_tool(
                "read_code_file",
                {"path": file_path}
            )

            code_content = result.content[0].text

            if code_content.startswith("Error"):
                print(code_content)
                return

            prompt = f"""
You are a senior software engineer.

Explain the following code LINE BY LINE in simple terms.
Mention line numbers.

CODE:
{code_content}
"""

            print("\nSending to LLM...\n")

            response = ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )

            print("\n========== CODE EXPLANATION ==========\n")
            print(response["message"]["content"])


# -------------------- ENTRY POINT --------------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        mcp.run()
    else:
        asyncio.run(run_client())
