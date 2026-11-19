from dotenv import load_dotenv
import sys, os
from pathlib import Path
import litellm
from ddgs import DDGS
from ddgs.exceptions import DDGSException
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import(
    StdioConnectionParams,
    StreamableHTTPConnectionParams
)
from mcp import StdioServerParameters

load_dotenv()

litellm.drop_params = True  # Strips unsupported reasoning_content on follow-up turns

github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError("Add GITHUB_TOKEN to .env file ")

folder = Path(__file__).parent.joinpath("files").resolve()
folder.mkdir(exist_ok=True)
npx_cmd = "npx.cmd" if sys.platform == "win32" else "npx"


def web_search(query: str, max_results: int = 3) -> list[dict]:
    """Search the web for current information, news, and facts.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")[:250],
            }
            for r in results
        ]
    except DDGSException as e:
        return [{"error": f"Search failed: {e}. Try a broader query."}]
    except Exception as e:
        return [{"error": f"Unexpected search error: {e}"}]


root_agent = Agent(
    model=LiteLlm(model="openrouter/openrouter/free"),
    name="github_publisher",
    instruction=f"""
        You have access to filesystem and Github MCP servers.
        Use their tools to manage local files and handle Github workflows.
        Local files are located in {folder}. Use absolute paths for filesystem operations.
        """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                timeout=30.0,
                server_params=StdioServerParameters(
                    command=npx_cmd,
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        str(folder),
                    ],
                ),
            ),
        ),
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {github_token}",
                }
            )
        ),
        web_search,
    ],
)