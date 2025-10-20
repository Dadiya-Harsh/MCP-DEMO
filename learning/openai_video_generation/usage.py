from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
from typing_extensions import NotRequired, List
import  io
import json

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

async def main():
    
    video = await client.videos.create(
        prompt = "Create 10 an ad for new webseries on Mahabhart(Indian Epic) showcasing and teasing epic battle between 2 warriors **Karan** and **Arjun**",
        model= "sora-2",
        seconds="12"
    )

    if video.status == "completed":
        print(f"Video successfully completed: {video}")

    else: 
        print(f"Video Generation has failed see this is the stataus: {video.status} \n \n  whole object: {video}")
    # sample output
    # (mcp-demo) voldemort@LAPTOP-CBGPH8CF:~/learning/MCP-DEMO$ python -m learning.openai_video_generation.usage
    # Video Generation has failed see this is the stataus: queued 
    
    # whole object: Video(id='video_68e9f9f8ea388191bf9008c0c55c8bd30088c84410625cbe', completed_at=None, created_at=1760164345, error=None, expires_at=None, model='sora-2', object='video', progress=0, remixed_from_video_id=None, seconds='12', size='720x1280', status='queued')
    # (mcp-demo) voldemort@LAPTOP-CBGPH8CF:~/learning/MCP-DEMO$ 

async def download_video(video_id: str):
    response = await client.videos.download_content(
        video_id="video_68e9f9f8ea388191bf9008c0c55c8bd30088c84410625cbe"
    )
    print(response)
    
    async with client.videos.with_streaming_response.download_content(video_id=video_id) as response:
        http_response =  response.http_response
        # Stream to file manually
        with open(f"{video_id}.mp4", "wb") as f:
            async for chunk in http_response.aiter_bytes():
                f.write(chunk)
    print(f"✅ Streamed and saved {video_id}.mp4")




if __name__ == "__main__":
    asyncio.run(download_video("video_68e9f9f8ea388191bf9008c0c55c8bd30088c84410625cbe"))
