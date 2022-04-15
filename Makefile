MANAGE := python manage.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv install

freeze: ## Pin current dependencies
	pipenv lock -r > requirements.txt

migrate: ## Make and run migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

collectstatic: ## Run collectstatic
	$(MANAGE) collectstatic --noinput

changepassword: ## Change password superuser
	$(MANAGE) changepassword flavien-hugs

.PHONY: test
test: ## Run tests
	$(MANAGE) --verbosity=0 --parallel --failfast

.PHONY: createsuperuser
createsuperuser: ## Create super-user
	$(MANAGE) createsuperuser --username="valereobei@pm.me" --email="valereobei@pm.me"

.PHONY: tox-test
tox-test: ## test with tox
	flake8 core --ignore=E501
	coverage run --branch --source=core $(MANAGE) test --settings=core.settings core

dumpdata: ## dump data
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json sites.site > fixtures/site_domain.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json blog.category > fixtures/categories.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json blog.post > fixtures/articles.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json course.course > fixtures/courses.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json course.book > fixtures/books.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json checkout.checkout > fixtures/checkout_book.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json checkout.registercourse > fixtures/register_course.json
	$(MANAGE) dumpdata --indent=4 --natural-foreign --natural-primary -e contenttypes --format=json flatpages.flatpage > fixtures/pages.json

loaddata: ## load data
	$(MANAGE) loaddata fixtures/*.json

haystack-rebuild-index: ## haystack rebuild index
	$(MANAGE) rebuild_index

haystack-update-index: ## haystack update index
	$(MANAGE) update_index

.PHONY: crontabadd
crontabadd: ## Add all defined jobs from CRONJOB to crontab
	$(MANAGE) crontab add

.PHONY: crontabshow
crontabshow: ## Show current active jobs of this project
	$(MANAGE) crontab show

.PHONY: celery-worker
celery-worker: ## Starting the worker process
	celery -A core worker -l INFO --logfile=logs/celery.log

.PHONY: flower
flower: ## Starting monitoring
	celery -A core flower --port=5555 --broker=redis://redis:6379/1

.PHONY: coverage
coverage: ## Test with coverage and generate htmlcov
	coverage run --source "blog,course" manage.py test -v 2
	coverage html
	coverage report
