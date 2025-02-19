from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json

app = FastAPI()

# a workaround to get rid of CORS issues on localhost, do not use in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple server that streams text from a chat model. Make sure you have Ollama installed, and running "deepseek-r1:7b".
@app.post("/api/prompt")
async def chat(prompt: str = Body(..., embed=True)):
    async def stream_response():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", "http://localhost:11434/api/chat", json={
                "model": "deepseek-r1:7b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }) as response:
                async for line in response.aiter_lines():
                    if line:
                        yield json.dumps(json.loads(line)) + "\n"
    return StreamingResponse(stream_response(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)