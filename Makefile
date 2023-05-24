yaml:
	yamllint -d '{"extends": "default", "ignore": ".venv"}' -s .

check-django:
	python manage.py check --fail-level WARNING
	DJANGO_ENV=production python manage.py check --deploy --fail-level WARNING

style:
	flake8 --format=nova .
	yamllint -d '{"extends": "default", "ignore": ".venv" }' -s .

pytest:
	pytest --dead-fixtures && pytest --junitxml=report.xml --cov=server \
	--cov=tests --cov-branch --cov-report=term-missing:skip-covered \
	--cov-fail-under=100 --cov-report xml:coverage.xml

ci-yaml:
	yamllint -d '{"extends": "default", "ignore": ".venv" }' -s .

ci-migrations:
	python manage.py lintmigrations \
	--exclude-apps axes sites filer easy_thumbnails actstream account \
	token_blacklist nova_quiz nova_device push_notifications \
	--warnings-as-errors

ci-mypy:
	mypy manage.py server $(find tests -name '*.py')

flake8:
	flake8 .

pytest-coverage:
	pytest --cov=server/apps --cov-branch --cov-report html

celery:
	celery -A server worker -l info --concurrency=4
