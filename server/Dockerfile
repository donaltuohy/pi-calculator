FROM ubuntu:16.04

WORKDIR /app

EXPOSE 5000

COPY requirements.txt requirements.txt

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    apt-get install -y iputils-ping

RUN apt-get update && apt-get install -y g++

# RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python" ]

CMD [ "routes.py" ]