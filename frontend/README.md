# GPT API Proxy Frontend

Фронтенд-приложение для работы с различными GPT API (OpenAI, Grok, DeepSeek).

## Технологии

- Vue 3 с Composition API
- Vite для сборки
- Tailwind CSS для стилей
- Axios для HTTP-запросов
- Docker для контейнеризации

## Установка и запуск

### Локальная разработка

1. Установите зависимости:
```bash
npm install
```

2. Запустите сервер разработки:
```bash
npm run dev
```

Приложение будет доступно по адресу http://localhost:5173

### Сборка для продакшена

```bash
npm run build
```

### Запуск в Docker

```bash
# Сборка и запуск всех сервисов
docker compose up --build

# Только фронтенд
docker build -t gpt-proxy-frontend .
docker run -p 80:80 gpt-proxy-frontend
```

## Структура проекта

```
frontend/
├── src/              # Исходный код
│   ├── App.vue       # Главный компонент
│   └── main.js       # Точка входа
├── public/           # Статические файлы
├── Dockerfile        # Конфигурация Docker
├── nginx.conf        # Конфигурация Nginx
└── package.json      # Зависимости и скрипты
```

## Конфигурация

- Бэкенд API доступен через `/api` прокси
- Все запросы к API автоматически проксируются через Nginx
- Поддерживаются все основные модели от OpenAI, Grok и DeepSeek

## Разработка

1. Создайте новую ветку для ваших изменений
2. Внесите изменения
3. Запустите линтер и тесты
4. Создайте pull request

## Лицензия

MIT
