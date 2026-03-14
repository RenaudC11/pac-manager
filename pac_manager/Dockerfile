ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nginx python3

COPY www/ /var/www/html/
COPY nginx.conf /etc/nginx/nginx.conf
COPY run.sh /run.sh

RUN chmod +x /run.sh

CMD ["/run.sh"]
