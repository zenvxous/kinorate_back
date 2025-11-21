# Тестирование проекта

## Установка зависимостей

Для установки зависимостей для тестирования:

```bash
uv pip install -e ".[test]"
```

или

```bash
pip install pytest pytest-asyncio pytest-cov pytest-mock httpx faker freezegun aiosqlite
```

## Запуск тестов

### Запуск всех тестов

```bash
pytest
```

### Запуск тестов с проверкой покрытия

```bash
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=80
```

или используйте скрипт:

```bash
chmod +x check_coverage.sh
./check_coverage.sh
```

### Запуск конкретных тестов

```bash
# Тесты для DAO
pytest tests/test_dao_*.py

# Тесты для контроллеров
pytest tests/test_controllers_*.py

# Тесты для утилит
pytest tests/test_utils_*.py
```

## Маркеры тестов

- `@pytest.mark.unit` - Unit тесты
- `@pytest.mark.integration` - Интеграционные тесты
- `@pytest.mark.slow` - Медленные тесты

Запуск тестов по маркерам:

```bash
pytest -m unit          # Только unit тесты
pytest -m "not slow"    # Все тесты кроме медленных
```

