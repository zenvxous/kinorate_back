echo "Запуск тестов с проверкой покрытия..."
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml --cov-fail-under=80 -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Покрытие кода >= 80%"
    echo "HTML отчет доступен в папке htmlcov/index.html"
else
    echo ""
    echo "❌ Покрытие кода < 80% или тесты не прошли"
    exit 1
fi

