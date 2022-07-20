FROM python:3.9-buster

VOLUME [ "/root", "/app" ]

COPY ./requirements.txt /tmp

# RUN python -m venv /root/venv && \
#     . /root/venv/bin/activate

# SHELL ["/bin/bash", "-c"] 
# RUN python -m venv /root/venv && \
#     source /root/venv/bin/activate

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# RUN python -m venv /root/venv
# RUN /root/venv/bin/pip install --upgrade pip && \
#     /root/venv/bin/pip install -r /tmp/requirements.txt && \
#     rm /tmp/requirements.txt

CMD tail -f /dev/null
