FROM node:15.13.0-alpine

# make the 'app' folder the current working directory
WORKDIR /app
COPY package*.json ./
RUN npm i

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./ .