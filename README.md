# WorkHub_backend
## .env (must be in root directory)
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
HOST=
PORT=""
SECRET_MANAGER=""
SECRET_JWT_REFRESH=""
SECRET_JWT=""
```
## Launch for local development
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install -r .\requirements.txt
```
```
alembic revision --autogenerate
```
```
alembic upgrade head
```
```
uvicorn main:app --host 0.0.0.0 --port 8000
```
## Launch in docker
```
docker-compose up --build
```
## Used technologies
#### [FastApi](https://fastapi.tiangolo.com/)
#### [Sqlalchemy](https://www.sqlalchemy.org/)
#### [Alembic](https://alembic.sqlalchemy.org/en/latest/)
#### [Pydantic](https://docs.pydantic.dev/latest/)
#### [PostgreSQL](https://www.postgresql.org/)

# API Documentation
