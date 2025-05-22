from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import redis
import time
from config import get_settings

settings = get_settings()

# Инициализация Redis клиента с расширенными настройками
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    ssl=settings.REDIS_SSL,
    retry_on_timeout=settings.REDIS_RETRY_ON_TIMEOUT,
    socket_timeout=settings.REDIS_SOCKET_TIMEOUT,
    socket_connect_timeout=settings.REDIS_SOCKET_CONNECT_TIMEOUT,
    decode_responses=True
)

async def rate_limit_middleware(request: Request, call_next):
    try:
        # Пропускаем rate limiting для health check
        if request.url.path == "/":
            return await call_next(request)
        
        # Получаем IP адрес клиента
        client_ip = request.client.host
        
        # Создаем ключ для Redis
        key = f"rate_limit:{client_ip}"
        
        # Получаем текущее количество запросов
        current = redis_client.get(key)
        
        if current is None:
            # Если ключа нет, создаем его с TTL 60 секунд
            redis_client.setex(key, 60, 1)
        else:
            current = int(current)
            if current >= settings.RATE_LIMIT_PER_MINUTE:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Too many requests",
                        "detail": f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_PER_MINUTE} requests per minute."
                    }
                )
            # Увеличиваем счетчик
            redis_client.incr(key)
        
        # Продолжаем обработку запроса
        return await call_next(request)
    except redis.RedisError as e:
        # В случае ошибки Redis, логируем её и пропускаем rate limiting
        print(f"Redis error: {str(e)}")
        return await call_next(request) 