FROM ubuntu:16.04

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python" ]

CMD ["routes.py"]