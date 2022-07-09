FROM python:3.9-buster

VOLUME [ "/root", "/app" ]

COPY ./requirements.txt /tmp

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

CMD tail -f /dev/null
