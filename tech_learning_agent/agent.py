import os

from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

root_agent = Agent(
    name="tech_learning_agent",
    model="gemini-2.5-flash",
    description="技術学習を支援するAIエージェント",
    instruction="""
    あなたは技術学習を支援するAIエージェントです。

    ユーザーが学びたい技術について質問したら、
    初学者にも分かるように説明してください。
    """,
)