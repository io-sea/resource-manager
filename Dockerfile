# syntax=docker/dockerfile:1

FROM python:3.10-slim

WORKDIR /RM

RUN apt-get -y update
RUN apt-get -y install nano

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "src/resource_manager/run.py"]
#ENTRYPOINT ["python3", "src/resource_manager/run.py"]


