FROM node:22-alpine

WORKDIR /frontend

COPY . /frontend

RUN npm install -g @angular/cli && npm install

CMD ["ng", "serve", "--host", "0.0.0.0"]

