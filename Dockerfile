FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install python3.12 -y && apt-get install python3-pip pipenv -y

RUN mkdir /FinMindProject
COPY . /FinMindProject/
WORKDIR /FinMindProject/



RUN pipenv sync

RUN VERSION=RELEASE python3 genenv.py
