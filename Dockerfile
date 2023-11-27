FROM ubuntu:22.04

USER root

RUN apt-get update && apt-get -y install python3 python3-pip vim git curl wget 

USER root

RUN mkdir -p /app/fresco-api

ADD ./files /app/fresco-api

WORKDIR /app/fresco-api

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["python3","-m","uvicorn","main:app","--host","0.0.0.0","--port","5000"]

