# Dockerfile -- GG Cache appserver
# This is a "fat" container, with developer tools.
# TODO: move to production container, e.g. "FROM python:3.7"
# 
FROM ubuntu:18.04

RUN apt update && apt install -y python3-pip

WORKDIR /code

ADD requirements.txt /tmp/
RUN pip3 install -qr /tmp/requirements.txt

ADD requirements.txt *.py /code/

EXPOSE 5000

# Heroku runs as non-root, do that here to help flush out bugs
RUN useradd -ms /bin/bash ggcache
USER ggcache 

ENTRYPOINT ["python3"]
CMD ["server.py"]
