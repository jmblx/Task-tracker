# Rinh-hack. RNDSOFT
## Процесс разработки
### Создания виртуального окружения
```shell
python -m venv venv
venv\Scripts\activate
```
### Установка зависимостей
```shell
pip install -r requirements\dev.txt
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