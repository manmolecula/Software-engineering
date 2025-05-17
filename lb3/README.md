# Лабораторная работа 3

## Усовершенствования сервисов

- Расширена модель пользователя: добавлены поля для инициалов, роли и статуса активности (в планах: реализация функционала блокировки пользователей).
- Внедрена поддержка асинхронных операций.
- Добавлена интеграция с PostgreSQL.

## Структура базы данных

Реализована работа с PostgreSQL. Созданы следующие таблицы:

```sql
CREATE TABLE public.projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(50) NOT NULL
);
CREATE INDEX idx_projects_name ON public.projects USING btree (name);

CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    initials VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('Guest', 'User', 'Admin')),
    disabled BOOLEAN NOT NULL DEFAULT false,
    password VARCHAR(255),
    hashed_password VARCHAR(255) NOT NULL
);
CREATE INDEX idx_users_username ON public.users USING btree (username);
```

При запуске сервисы автоматически создают необходимые таблицы, если они отсутствуют, а также добавляют тестовые данные и учетную запись администратора (аналогичную той, что была в ЛР2).

## Инструкция по запуску

Для запуска выполните команду `docker-compose up --build` из директории `lab3`.

Адреса сервисов:  
- Сервис аутентификации: `http://localhost:8000`  
- Сервис проектов: `http://localhost:8001`