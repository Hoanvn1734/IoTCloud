FROM python:2.7

RUN pip install pika

RUN pip install influxdb

RUN mkdir /writeDB

RUN mkdir /configwdb

ADD writeDB.py /writeDB

ADD configure.cfg /configwdb

WORKDIR /writeDB

VOLUME /configwdb

CMD python writeDB.py
