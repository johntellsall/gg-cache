# FROM python:3.7
FROM ubuntu:18.04

RUN apt update && apt install -y python3-pip

WORKDIR /code


ADD requirements.txt /tmp/
RUN pip3 install -qr /tmp/requirements.txt

ADD requirements.txt *.py /code/

# ENTRYPOINT ["python"]
# CMD ["server.py"]
