#!/bin/bash

# Базовый URL
BASE_URL="http://localhost:8000"

# Проверка работоспособности сервиса
echo "Testing service health..."
curl -X GET "${BASE_URL}/"

# # Пример запроса к OpenAI
# echo -e "\nTesting OpenAI API..."
# curl -X POST "${BASE_URL}/v1/chat/completions" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "messages": [
#       {"role": "user", "content": "Hello!"}
#     ],
#     "model": "gpt-3.5-turbo",
#     "provider": "openai",
#     "temperature": 0.7
#   }'

# # Пример запроса к Grok
# echo -e "\nTesting Grok API..."
# curl -X POST "${BASE_URL}/v1/chat/completions" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "messages": [
#       {"role": "user", "content": "Hello!"}
#     ],
#     "model": "grok-1",
#     "provider": "grok",
#     "temperature": 0.7
#   }'

# Пример запроса к DeepSeek
echo -e "\nTesting DeepSeek API..."
curl -X POST "${BASE_URL}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "model": "deepseek-chat",
    "provider": "deepseek",
    "temperature": 0.7
  }' 