FROM python:3.11-slim-buster AS builder

WORKDIR /.

RUN apt-get update && apt-get install -y procps && pip install -U pip && rm /etc/localtime && ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime

COPY ./requirements.txt /requirements.txt

RUN pip install -r ./requirements.txt


COPY ./api.py /api.py
COPY ./x_encode.pkl /x_encode.pkl

EXPOSE 5050
CMD ["uvicorn","api:app", "--host", "0.0.0.0", "--port", "5050"]
#