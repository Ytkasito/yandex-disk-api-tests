# Автотесты API Яндекс.Диска

Проект автоматизированного тестирования REST API Яндекс.Диска с использованием Python, Pytest, Requests и Allure Report.

---

# Стек технологий

- Python 3
- Pytest
- Requests
- Allure Report
- JSON Schema
- Git
- GitHub Actions

---

# Структура проекта

```text
yandex-disk-api-tests
│
├── .github
│   └── workflows
│       └── tests.yml
│
├── schemas
│   ├── disk_info_schema.py
│   ├── error_schema.py
│   ├── link_schema.py
│   ├── operation_schema.py
│   └── resource_schema.py
│
├── test_data
│   └── hello.txt
│
├── tests
│   ├── crud
│   │   ├── test_create_resource.py
│   │   ├── test_delete_resource.py
│   │   ├── test_get_disk_info.py
│   │   ├── test_get_resource_metadata.py
│   │   └── test_update_resource_metadata.py
│   │
│   ├── lifecycle
│   │   ├── test_copy_resource.py
│   │   ├── test_download_file.py
│   │   ├── test_move_resource.py
│   │   ├── test_publish_resource.py
│   │   ├── test_restore_from_trash.py
│   │   └── test_upload_file.py
│   │
│   └── negative
│       └── test_resource_negative_cases.py
│
├── utils
│   ├── assertions.py
│   ├── client.py
│   └── logger.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# Реализованные проверки

## CRUD операции
- Создание папок
- Получение метаданных ресурса
- Удаление ресурсов
- Загрузка файлов
- Скачивание файлов
- Обновление пользовательских метаданных

## Lifecycle сценарии
- Копирование ресурсов
- Перемещение ресурсов
- Восстановление из корзины
- Публикация и снятие публичного доступа

## Негативные сценарии
- Запросы без авторизации
- Работа с несуществующими ресурсами
- Создание уже существующих ресурсов
- Некорректные параметры запросов
- Ошибки удаления ресурсов

---

# Возможности проекта

- Проверка status code
- Проверка структуры JSON-ответов
- JSON Schema validation
- Логирование запросов и ответов
- Allure-отчеты
- Автоматическая очистка тестовых данных
- Работа с асинхронными операциями
- Кастомные assertions

---

# Установка проекта

Клонирование репозитория:

```bash
git clone https://github.com/YOUR_USERNAME/yandex-disk-api-tests.git
```

Создание виртуального окружения:

```bash
python -m venv venv
```

Активация виртуального окружения:

## Windows

```bash
venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

---

# Настройка переменных окружения

Создать файл `.env`:

```env
BASE_URL=https://cloud-api.yandex.net
TOKEN=your_oauth_token
```

---

# Запуск тестов

Запуск всех тестов:

```bash
pytest -v
```

Запуск отдельных групп тестов:

```bash
pytest tests/crud -v
pytest tests/lifecycle -v
pytest tests/negative -v
```

---

# Allure Report

Генерация отчета:

```bash
allure serve allure-results
```

---

