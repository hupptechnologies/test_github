import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def stream_chat_completion(user_message: str):
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content 