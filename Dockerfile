# FROM python:3.7
FROM ubuntu:18.04

RUN apt update && apt install -y python3-pip

WORKDIR /code

ADD requirements.txt server.py /code/

RUN pip3 install -qr requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]
