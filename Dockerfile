#FROM ubuntu:22.04
FROM nginx

USER root

RUN apt-get update && apt-get -y install python3 python3-pip vim git curl wget nginx

USER root

COPY ./deployment/default /etc/nginx/sites-available/

RUN mkdir -p /app/fresco-api

ADD ./files /app/fresco-api

WORKDIR /app/fresco-api

RUN python3 -m pip install --break-system-packages -r requirements.txt

#EXPOSE 5000
EXPOSE 80

#CMD ["python3","-m","uvicorn","main:app","--host","0.0.0.0","--port","5000"]
CMD ["/bin/bash", "-c", "python3 -m uvicorn main:app --port 5000; nginx -g 'daemon off;'"]
