FROM ma-cantine-server

WORKDIR /app/2024-frontend

USER root

# NB: this wont reinstall on build, must rebuild server image first
RUN npm install

EXPOSE 5173

CMD [ "npm", "run", "dev" ]
