FROM node:15.12.0-alpine3.10

# make the 'app' folder the current working directory
WORKDIR /app/

COPY package.json ./

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .
# expose port 8080 to the host
EXPOSE 8080
ENV VUE_APP_API_PORT='8000'

CMD ["sh", "start_dev.sh"]