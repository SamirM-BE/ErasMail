docker build -t edgargevorgyan/erasmail_nginx -f ./nginx/Dockerfile .
docker push edgargevorgyan/erasmail_nginx

cd back-end/erasmail
docker build -t edgargevorgyan/erasmail_web .
docker push edgargevorgyan/erasmail_web

# docker-compose -f docker-compose.prod.yml up -d --build
# docker-compose -f docker-compose.prod.yml down -v