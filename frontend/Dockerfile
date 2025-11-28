
FROM node:lts-slim

# the following NODE_OPTIONS are required because:
#
# https://github.com/django-webpack/webpack-bundle-tracker/tree/master?tab=readme-ov-file#compatibility

ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /app

# only copy the dependencies file first to make sure the step is only
# ran if either of these files explicitly change.
COPY package.json package-lock.json ./

RUN npm ci --ignore-scripts

COPY . .

CMD ["npm", "run", "serve"]
