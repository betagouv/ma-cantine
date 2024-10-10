FROM node:lts

ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /app

# only copy the dependencies file first to make sure the step is only
# ran if either of these files explicitly change.
COPY package.json package-lock.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
