#!/bin/bash

# Базовый URL
BASE_URL="http://localhost:8000"

# Количество запросов для теста
REQUESTS=15

echo "Testing rate limiting with $REQUESTS requests..."

# Выполняем запросы в цикле
for i in $(seq 1 $REQUESTS); do
    echo -n "Request $i: "
    response=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -d '{
            "messages": [
                {"role": "user", "content": "Test message"}
            ],
            "model": "gpt-3.5-turbo",
            "provider": "openai",
            "temperature": 0.7
        }')
    
    # Получаем статус код из последней строки
    status_code=$(echo "$response" | tail -n1)
    
    # Выводим результат
    if [ "$status_code" = "429" ]; then
        echo "Rate limit exceeded (429)"
    elif [ "$status_code" = "200" ]; then
        echo "Success (200)"
    else
        echo "Error ($status_code)"
    fi
    
    # Небольшая задержка между запросами
    sleep 0.1
done 