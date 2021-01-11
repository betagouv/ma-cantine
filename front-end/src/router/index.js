import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/views/LandingPage.vue';
import KeypointsPage from '@/views/KeypointsPage.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
  {
    path: '/mesures-phares',
    name: 'KeypointsPage',
    component: KeypointsPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
