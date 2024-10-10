FROM node:lts-slim

# the below env variable is sadly required because of some hashing
# functions that have disappeared in OpenSSL and Node wants them: see
#
# https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported
#
# for a list of vague reasons and fixes. Ideally the dependencies
# would be upgraded (Webpack is the one causing the error) but this is
# legacy stuff so it will hopefully disappear of its own.

ENV NODE_OPTIONS=--openssl-legacy-provider

WORKDIR /app

# only copy the dependencies file first to make sure the step is only
# ran if either of these files explicitly change.
COPY package.json package-lock.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "serve"]
