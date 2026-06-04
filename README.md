# HW9 for SpringData2026

Добавить в корень репозитория:
- `.dockerignore`
- `Dockerfile`
- `docker-compose.yaml`
- `.env.example`

Локальный `.env`:
```env
POSTGRES_DB=urban_data
POSTGRES_USER=urban_user
POSTGRES_PASSWORD=urban_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+psycopg://urban_user:urban_password@db:5432/urban_data
```

Запуск:
```bash
docker compose up --build
```

Проверка:
```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

Swagger UI:
- http://127.0.0.1:8000/docs
