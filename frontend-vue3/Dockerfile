FROM ma-cantine-server

WORKDIR /app/frontend-vue3

USER root

# NB: this wont reinstall on build, must rebuild server image first
RUN npm ci --ignore-scripts

EXPOSE 5173

CMD [ "npm", "run", "dev" ]
