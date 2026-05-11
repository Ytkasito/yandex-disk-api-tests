# Автотесты API Яндекс.Диска

Проект автоматизированного тестирования REST API Яндекс.Диска с использованием Python, Pytest, Requests и Allure Report.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pytest](https://img.shields.io/badge/Pytest-9.0.3-blue)
![Allure](https://img.shields.io/badge/Allure-2.16.0-orange)
![CI](https://github.com/Ytkasito/yandex-disk-api-tests/actions/workflows/api-tests.yml/badge.svg)

---

## Стек технологий

- **Python 3.12** — язык разработки
- **Pytest** — фреймворк для тестирования
- **Requests** — HTTP-клиент
- **Allure Report** — отчёты о прохождении тестов
- **JSON Schema** — валидация структуры ответов
- **python-dotenv** — управление переменными окружения
- **GitHub Actions** — CI/CD и публикация отчётов на GitHub Pages

---

## Структура проекта

```text
yandex-disk-api-tests
│
├── .github
│   └── workflows
│       └── api-tests.yml       # CI/CD пайплайн
│
├── schemas
│   ├── disk_info_schema.py
│   ├── error_schema.py
│   ├── link_schema.py
│   ├── operation_schema.py
│   └── resource_schema.py
│
├── test_data
│   └── hello.txt               # Файл для тестов загрузки
│
├── tests
│   ├── conftest.py             # Общие фикстуры
│   │
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
│   ├── assertions.py           # Кастомные проверки и Allure-вложения
│   ├── client.py               # HTTP-клиент Яндекс.Диска
│   └── logger.py               # Логирование запросов
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Реализованные проверки

### CRUD операции
- Создание папок (в том числе вложенных)
- Получение метаданных ресурса с фильтрацией полей
- Удаление ресурсов (в корзину и безвозвратно)
- Обновление пользовательских метаданных

### Lifecycle сценарии
- Загрузка и скачивание файлов
- Копирование и перемещение ресурсов
- Восстановление из корзины
- Публикация и снятие публичного доступа
- Работа с асинхронными операциями

### Негативные сценарии
- Некорректные параметры запросов (400)
- Запросы без авторизации (401)
- Работа с несуществующими ресурсами (404)
- Создание уже существующих ресурсов (409)
- Ошибки удаления ресурсов

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Ytkasito/yandex-disk-api-tests.git
cd yandex-disk-api-tests
```

### 2. Создание и активация виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создать файл `.env` в корне проекта:

```env
BASE_URL=https://cloud-api.yandex.net
TOKEN=your_oauth_token
```

Получить OAuth-токен можно в [кабинете разработчика Яндекса](https://oauth.yandex.ru/).

---

## Запуск тестов

Запуск всех тестов (результаты Allure сохраняются автоматически в `allure-results`):

```bash
pytest
```

Запуск отдельных групп по маркерам:

```bash
pytest -m crud
pytest -m lifecycle
pytest -m negative
```

Запуск конкретной директории:

```bash
pytest tests/crud
pytest tests/lifecycle
pytest tests/negative
```

---

## Allure Report

Открыть интерактивный отчёт после запуска тестов:

```bash
allure serve allure-results
```

Сгенерировать статичный HTML-отчёт:

```bash
allure generate allure-results --clean -o allure-report
```

---

## CI/CD

При каждом пуше в ветку `main` и при открытии Pull Request автоматически:

1. Запускаются все тесты
2. Генерируется Allure-отчёт
3. Отчёт публикуется на **GitHub Pages**

Для работы CI необходимо добавить секрет `TOKEN` в настройках репозитория:  
`Settings → Secrets and variables → Actions → New repository secret`

---

## Возможности проекта

- Проверка статус-кодов HTTP
- Валидация структуры JSON-ответов через JSON Schema
- Логирование всех запросов и ответов
- Детальные Allure-отчёты с вложениями (URL, метод, тело ответа)
- Автоматическая очистка тестовых данных через фикстуры
- Переиспользование HTTP-соединений через `requests.Session`
- Таймаут на все запросы (10 секунд)
