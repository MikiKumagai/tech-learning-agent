from mcp.server.mcpserver import MCPServer

mcp = MCPServer("tech-learning-server")


@mcp.tool()
def get_learning_topics() -> list[str]:
    """現在の学習候補となる技術を取得する。"""
    return [
        "dbt",
        "Apache Airflow",
        "Apache Kafka",
    ]


if __name__ == "__main__":
    mcp.run()