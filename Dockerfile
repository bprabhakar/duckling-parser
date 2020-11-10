FROM python:3.6

ENV LANG=C.UTF-8

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y swig curl libpcre3 libpcre3-dev && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    curl -sSL https://get.haskellstack.org/ | sh && \
    cd /home && \
    git clone https://github.com/facebook/duckling.git && \
    cd /home/duckling && \
    stack build

RUN pip install flask flask-cors gevent requests pendulum

EXPOSE 8001

COPY . /home/aarzoo-mvp

WORKDIR /home/aarzoo-mvp

CMD ["stack", "exec", "duckling-example-exe"]
