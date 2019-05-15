FROM python:3.7

WORKDIR /code

ADD requirements.txt server.py /code/

RUN pip install -qr requirements.txt

ENTRYPOINT ["python"]
CMD ["server.py"]
