FROM docker.io/nginx:1.31.2-alpine3.23-slim

RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/default.conf