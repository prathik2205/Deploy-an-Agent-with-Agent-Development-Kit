"""Chainlit front end that queries the agent deployed on Agent Runtime."""
import os

import chainlit as cl
import vertexai
from dotenv import load_dotenv

load_dotenv()

client = vertexai.Client(
    project=os.environ["GOOGLE_CLOUD_PROJECT"],
    location=os.environ["GOOGLE_CLOUD_LOCATION"],
)
agent = client.agent_engines.get(name=os.environ["AGENT_RESOURCE_NAME"])


@cl.on_chat_start
async def start():
    session = await agent.async_create_session(user_id="web-user")
    cl.user_session.set("session_id", session["id"])
    await cl.Message("Welcome to Cymbal Shops Paint Dept. Say hello to begin!").send()


@cl.on_message
async def main(message: cl.Message):
    reply = cl.Message(content="")
    async for event in agent.async_stream_query(
        user_id="web-user",
        session_id=cl.user_session.get("session_id"),
        message=message.content,
    ):
        for part in (event.get("content") or {}).get("parts", []):
            if part.get("text"):
                await reply.stream_token(part["text"])
    await reply.send()
