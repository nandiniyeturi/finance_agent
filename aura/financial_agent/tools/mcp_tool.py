from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

# toolset = MCPToolset(
#     connection_params=StreamableHTTPConnectionParams(
#         url="http://localhost:8080/mcp/stream"
#     )
# )
# /Users/gowtham/Documents/Hackathon/aura/financial_agent/tools/mcp_tool.py

toolset = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://mcp.fi.money:8080/mcp/stream"
    )
)