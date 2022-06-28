FROM python:3.8-alpine
MAINTAINER Gabriell Vig <gabriell.vig@sesam.io>


RUN apk update
RUN apk add tzdata
RUN apk add openssh
RUN rm -f /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Oslo /etc/localtime
RUN pip3 install --upgrade pip

COPY ./requirements.txt /service/requirements.txt
RUN pip3 install -r /service/requirements.txt
COPY ./service /service

WORKDIR /service

EXPOSE 5000/tcp

CMD ["sh", "/service/setup_cron.sh"]
