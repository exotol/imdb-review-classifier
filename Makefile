PYTHON=3.9.13
PROJECT=imdb_review_classifier


python:
	@echo "Установка необходимой версии питона"
	pyenv install $(PYTHON); \

venv:
	@echo "Создание окружение"
	pyenv virtualenv $(PYTHON) $(PROJECT); \
	pyenv shell $(PROJECT); \
	pyenv local $(PROJECT); \

poetry:
	@echo "Установить poetry"
	pip install --upgrade pip; \
	pip install poetry


gen-req:
	@echo "Генерация зависимостей requirements/requirements.txt requirements/requirements-dev.txt"
	poetry export --without-hashes | grep -v "@ file" >> requirements/requirements.txt; \
	poetry export --with dev --without-hashes | grep -v "@ file" >> requirements/requirements-dev.txt; \



struct:
	@echo "Генерация структуры проекта"
	mkdir -p data/raw && touch data/raw/.gitkeep; \
	mkdir -p $(PROJECT) && touch $(PROJECT)/__init__.py; \
	mkdir -p requirements && make gen-req; \
	mkdir -p docker && touch docker/docker-compose.yaml; \
	mkdir -p tests && touch tests/.gitkeep; \
	mkdir -p configs && touch configs/baseline.yaml; \
	mkdir -p scripts && touch scripts/train.sh; \
	touch .gitignore; \
	git add data/raw/.gitkeep $(PROJECT)/__init__.py;\
	git add docker/docker-compose.yaml tests/.gitkeep; \
	git add requirements/requirements.txt requirements/requirements-dev.txt; \
	git add scripts/train.sh configs/baseline.yaml; \
	git add .gitignore; \


load:
	@echo "Загрузить данные с каггла"
	kaggle datasets download -d lakshmi25npathi/imdb-dataset-of-50k-movie-reviews -p data/raw; \
	unzip data/raw/imdb-dataset-of-50k-movie-reviews.zip -d data/raw/; \
	rm -rf data/raw/imdb-dataset-of-50k-movie-reviews.zip; \
