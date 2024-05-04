FROM python:3.11-slim-buster AS builder

WORKDIR /app

#De donde viene y a donde lo voy a enviar
COPY requirements.txt /code/requirements.txt

RUN apt-get update && apt-get install -y procps && pip install -U pip && rm /etc/localtime && ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime

COPY requirements.txt app/requirements.txt

RUN pip install -r app/requirements.txt

COPY app.py app/app.py

EXPOSE 8501

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]