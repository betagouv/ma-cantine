import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/views/LandingPage.vue';
import KeyMeasuresPage from '@/views/KeyMeasuresPage.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
  {
    path: '/mesures-phares',
    name: 'KeyMeasuresPage',
    component: KeyMeasuresPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior (to) {
    if (to.hash) {
      return {
        el: to.hash
      }
    } else {
      return {
        top: 0
      }
    }
  }
});

export default router;
