# Yandex Disk API Tests

API test automation project for Yandex Disk REST API.

## Documentation

* API documentation: [https://yandex.ru/dev/disk/api/concepts/about-docpage/](https://yandex.ru/dev/disk/api/concepts/about-docpage/)
* Base URL: [https://cloud-api.yandex.net](https://cloud-api.yandex.net)

---

## Tech Stack

* Python 3
* Pytest
* Requests
* Allure Report
* python-dotenv

---

## Project Structure

```text
tests/
├── crud/
│   ├── test_create_resource.py
│   ├── test_delete_resource.py
│   ├── test_get_disk_info.py
│   └── test_get_resource_metadata.py
│
├── lifecycle/
│   ├── test_copy_resource.py
│   ├── test_move_resource.py
│   └── test_trash_restore.py
│
├── negative/
│   └── test_resource_negative_cases.py
│
└── conftest.py

utils/
└── client.py
```

---

## Covered Test Scenarios

### CRUD Tests

* Get disk information
* Create folder
* Get resource metadata
* Delete folder

### Lifecycle Tests

* Copy folder
* Move folder
* Restore folder from trash

### Negative Tests

* Create existing folder
* Get non-existing resource
* Request without OAuth token

---

## Installation

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create `.env` file in the project root:

```env
TOKEN=your_oauth_token
BASE_URL=https://cloud-api.yandex.net
```

`.env` file is ignored by Git and should not be pushed to GitHub.

---

## Running Tests

### Run all tests

```bash
pytest -v
```

### Run CRUD tests

```bash
pytest -m crud
```

### Run lifecycle tests

```bash
pytest -m lifecycle
```

### Run negative tests

```bash
pytest -m negative
```

---

## Allure Report

### Generate Allure results

```bash
pytest --alluredir=allure-results
```

### Open Allure report

```bash
allure serve allure-results
```

---

## Notes

* OAuth token should be generated for a separate test account
* Sensitive data is stored locally in the `.env` file
* `.env` file is excluded from Git using `.gitignore`
