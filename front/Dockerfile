FROM node:14

ARG BASE_URL

WORKDIR /usr/src/app

COPY . ./
RUN yarn

EXPOSE 8080

ENV HOST=0.0.0.0
ENV PORT=8080

RUN NUXT_ENV_BASE_URL=${BASE_URL} yarn build

CMD [ "yarn", "start" ]
