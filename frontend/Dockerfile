FROM node:13.12.0-alpine

WORKDIR /usr/src/frontend

ENV PATH /usr/src/node_modules/.bin:$PATH

COPY package.json .

RUN npm install --silent

COPY . /usr/src/frontend

# RUN npm install react-scripts@3.0.1 -g --silent

EXPOSE 3000

CMD npm start