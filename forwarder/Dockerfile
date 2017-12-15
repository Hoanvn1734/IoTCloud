FROM python:2.7

RUN pip install pika

RUN mkdir /forwarder

RUN mkdir /configfw

ADD forwarder.py /forwarder

ADD configure.cfg /configfw

WORKDIR /forwarder

VOLUME /configfw

CMD python forwarder.py
