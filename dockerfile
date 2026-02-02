FROM python:3.14.2-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \ PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl

# UV,  Esta estructura reduce drásticamente la superficie de
# ataque y el tamaño de la imagen, mejorando la seguridad y 
#eficiencia en producción. 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY requirements.txt .
RUN uv pip install -r requirements.txt --system

COPY geek_commerce/ .

EXPOSE 8000

CMD ["./erntrypoint.sh"]