<div align="center">

# Автотесты REST API Яндекс.Диска

<div align="center">

# Yandex Disk API Tests

Полноценный framework для автоматизированного тестирования REST API сервиса Яндекс.Диск.

Проект демонстрирует навыки построения API automation framework с использованием Python, Pytest, Requests, Allure Report и CI/CD.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0.3-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Requests](https://img.shields.io/badge/Requests-HTTP_Client-black)](https://requests.readthedocs.io/)
[![Allure](https://img.shields.io/badge/Allure-2.16.0-orange)](https://allurereport.org/)
[![CI](https://github.com/Ytkasito/yandex-disk-api-tests/actions/workflows/api-tests.yml/badge.svg)](https://github.com/Ytkasito/yandex-disk-api-tests/actions/workflows/api-tests.yml)

</div>

---

# Live Allure Report

https://ytkasito.github.io/yandex-disk-api-tests/

---

# Allure Report

## Overview

<img width="100%" src="images/allure-overview.png" alt="Allure Overview">

---

## Detailed Test Execution

<img width="100%" src="images/allure-test.png" alt="Allure Detailed Test">

---

# CI/CD Pipeline

<img width="100%" src="images/github-actions.png" alt="GitHub Actions Pipeline">

---

# Key Features

- REST API testing
- CRUD operations coverage
- Lifecycle testing
- Negative testing
- JSON Schema validation
- Reusable API client
- Request/response logging
- Custom assertions
- Allure reporting
- GitHub Actions CI/CD
- Live Allure Report via GitHub Pages
- Scalable test architecture

---

## О проекте

Проект представляет собой полноценный framework для автоматизированного тестирования REST API Яндекс.Диска.

Основная цель проекта — покрытие ключевых пользовательских сценариев API:

- CRUD-операции с ресурсами
- загрузка и скачивание файлов
- работа с публичными ссылками
- проверка асинхронных операций
- негативные сценарии
- валидация JSON-схем
- логирование запросов и ответов
- генерация детализированных Allure-отчётов

Проект построен с упором на:

- читаемость тестов
- переиспользуемость кода
- масштабируемость
- поддержку CI/CD
- удобство анализа результатов тестирования

---

# Технологический стек

| Технология | Назначение |
|---|---|
| Python 3.12 | Основной язык разработки |
| Pytest | Фреймворк для запуска тестов |
| Requests | HTTP-клиент для API-запросов |
| Allure Report | Генерация HTML-отчётов |
| JSON Schema | Валидация структуры ответов |
| python-dotenv | Работа с переменными окружения |
| GitHub Actions | CI/CD пайплайн |
| GitHub Pages | Публикация Allure Report |

---

# Архитектура проекта

```text
yandex-disk-api-tests
│
├── .github
│   └── workflows
│       └── api-tests.yml
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
│   ├── conftest.py
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

# Установка проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/Ytkasito/yandex-disk-api-tests.git
cd yandex-disk-api-tests
```

---

## 2. Создание виртуального окружения

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## 4. Настройка переменных окружения

Создать файл `.env` в корне проекта:

```env
BASE_URL=https://cloud-api.yandex.net
TOKEN=your_oauth_token
```

Получить OAuth-токен можно через:

https://oauth.yandex.ru/

---

# Запуск тестов

## Запуск всех тестов

```bash
pytest
```

---

## Запуск с Allure

```bash
pytest -v --alluredir=allure-results
allure serve allure-results
```

---

## Запуск по маркерам

### CRUD

```bash
pytest -m crud
```

### Lifecycle

```bash
pytest -m lifecycle
```

### Negative

```bash
pytest -m negative
```

---

# CI/CD

Проект автоматически запускает тесты через GitHub Actions.

Pipeline выполняет:

1. Установку зависимостей
2. Запуск тестов
3. Генерацию Allure Report
4. Публикацию отчёта на GitHub Pages

Workflow запускается:

- при push в ветку `main`
- при Pull Request

---

# Настройка GitHub Secrets

Для работы CI необходимо добавить секрет:

```text
TOKEN
```

Путь:

```text
Settings → Secrets and variables → Actions → New repository secret
```

---

# Что демонстрирует проект

Проект демонстрирует навыки:

- API Testing
- REST Architecture
- Python Automation
- Pytest Framework
- Работа с HTTP
- JSON Schema Validation
- Работа с фикстурами
- Построение тестовой архитектуры
- CI/CD интеграция
- Работа с Allure Report
- Git/GitHub

---


# Автор

Проект разработан как pet-project для практики автоматизированного тестирования REST API и демонстрации навыков QA Automation.

---

# Контакты

GitHub:

https://github.com/Ytkasito

Telegram:

@Inckavo

Mail:

kira090801@mail.ru