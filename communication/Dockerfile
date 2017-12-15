FROM python:2.7

RUN  pip install paho-mqtt

RUN pip install pika

RUN mkdir /communication

RUN mkdir /configbroker

ADD communication.py /communication

ADD configure.cfg /configbroker

WORKDIR /communication

VOLUME /configbroker

CMD python communication.py
