FROM node:lts-slim

WORKDIR /app

# only copy the dependencies file first to make sure the step is only
# ran if either of these files explicitly change.
COPY package.json package-lock.json ./

RUN npm ci --ignore-scripts

COPY . .

CMD ["npm", "run", "dev"]
