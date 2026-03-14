ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nginx python3

COPY rootfs/ /
COPY www/ /var/www/html/
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod a+x /etc/services.d/pac/run
