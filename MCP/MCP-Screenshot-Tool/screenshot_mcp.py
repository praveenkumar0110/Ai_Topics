import asyncio
import sys
import os
from datetime import datetime

from mcp.server import FastMCP
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from playwright.async_api import async_playwright




mcp = FastMCP("ScreenshotTool")


@mcp.tool()
async def take_screenshot(url: str) -> str:
    """Open a website and take full page screenshot"""

    os.makedirs("screenshots", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/screenshot_{timestamp}.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()

    return f"Screenshot saved at: {screenshot_path}"




async def run_client():
    print("Starting MCP client...\n")

    server_params = StdioServerParameters(
        command="python",
        args=[__file__, "server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            while True:
                url = input("\nEnter website URL (or 'exit'): ").strip()

                if url.lower() == "exit":
                    break

                result = await session.call_tool(
                    "take_screenshot",
                    {"url": url}
                )

                print(result.content[0].text)



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        mcp.run()
    else:
        asyncio.run(run_client())
