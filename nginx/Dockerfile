FROM nginx:1.22.0-alpine


RUN apk add bash


RUN rm /etc/nginx/conf.d/default.conf
COPY ./default.conf /etc/nginx/conf.d
