FROM nginx

LABEL MAINTAINER="Ilya Alonov <i.alonov@innopolis.ru>"

RUN rm -rf /etc/nginx/conf.d/default.conf && \
    rm -rf /var/cache/apk/*

COPY conf.d/app.conf /etc/nginx/conf.d/app.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
