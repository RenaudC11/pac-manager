ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nginx python3

COPY www/ /var/www/html/
COPY nginx.conf /etc/nginx/nginx.conf
COPY run.sh /etc/services.d/pac/run

RUN chmod a+x /etc/services.d/pac/run && \
    mkdir -p /etc/services.d/pac
