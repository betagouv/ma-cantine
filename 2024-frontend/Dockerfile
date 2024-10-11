FROM ma-cantine-server

WORKDIR /app/2024-frontend

# only copy the dependencies file first to make sure the step is only
# ran if either of these files explicitly change.
# COPY package.json package-lock.json ./
USER root

RUN npm install

CMD [ "npm", "run", "dev" ]