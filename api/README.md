# Rinh-hack. RNDSOFT
## Процесс разработки
### Создания виртуального окружения
#### win
```shell
python -m venv venv
venv\Scripts\activate
```
#### lin
```shell
python3 -m venv venv
source venv/bin/activate
```
### Установка зависимостей
```shell
poetry install
```
### Запустить сервер
```shell
cd src
uvicorn main:app --reload
```
### Миграции
```shell
alembic revision --autogenerate
alembic upgrade head
```
### Реформат кода по pep8
```shell
black --config pyproject.toml . 
```
## Продакшн
### Развертывание всех контейнеров:
```shell
docker-compose up -d
```
## ER-диаграмма:
![ER Diagram](ER.jpg)
