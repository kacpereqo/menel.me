FROM ubuntu

# RUN apt-get install -y libffi-dev

FROM python:3.8-slim-buster

WORKDIR /

# RUN apt-get install -y python-qt4
# RUN apt-get install -y python-pyside
# RUN apt-get install -y python-pip
# RUN apt-get install -y python3-pip
# RUN apt-get install -y python3-pyqt5
# RUN apt-get install -y libffi-dev

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "main.py"]
