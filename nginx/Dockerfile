FROM nginx:1.19.0-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./nginx/certs /etc/nginx/certs

COPY ./front-end/erasmail/dist /usr/share/nginx/html