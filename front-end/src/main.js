import { createApp } from 'vue';
import VueMatomo from "vue-matomo";
import App from './App.vue';
import router from './router';
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

let app = createApp(App);

app.use(VueMatomo, {
  host: "https://stats.data.gouv.fr/",
  siteId: 162,
  router: router,
});

app.use(router).mount('#app');
