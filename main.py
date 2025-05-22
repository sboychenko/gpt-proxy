from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv
from middleware import rate_limit_middleware

# Загрузка переменных окружения
load_dotenv()

app = FastAPI(title="GPT API Proxy")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Добавляем rate limiting middleware
app.middleware("http")(rate_limit_middleware)

class ChatRequest(BaseModel):
    messages: list[Dict[str, str]]
    model: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    provider: str  # openai, grok, deepseek

@app.get("/")
async def root():
    return {"message": "GPT API Proxy is running"}

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    try:
        # Определяем API ключ и URL в зависимости от провайдера
        provider_config = {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": "https://api.openai.com/v1"
            },
            "grok": {
                "api_key": os.getenv("GROK_API_KEY"),
                "base_url": "https://api.grok.ai/v1"
            },
            "deepseek": {
                "api_key": os.getenv("DEEPSEEK_API_KEY"),
                "base_url": "https://api.deepseek.com/v1"
            }
        }

        if request.provider not in provider_config:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {request.provider}")

        config = provider_config[request.provider]
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json"
            }

            print(f"use {config['api_key']} for {request.provider}");

            async with session.post(
                f"{config['base_url']}/chat/completions",
                headers=headers,
                json=request.dict(exclude={'provider'})
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Provider API error: {error_text}"
                    )
                
                return await response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 