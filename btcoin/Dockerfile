FROM ubuntu:16.04

MAINTAINER zhoujunqian <zjqzero@gmail.com>

ADD . /home
RUN apt update
RUN apt install -y python3 \
                   python3-dev \
                   python3-pip

RUN pip3 install --no-cache-dir -r /home/requirements.txt
RUN apt purge -y python3-dev
RUN rm -rf /var/lib/apt/lists/* 
RUN rm -rf /tmp/*

CMD python3 /home/run.py
