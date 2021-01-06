import { createRouter, createWebHistory } from 'vue-router';
import Landing from '@/views/Landing.vue';
import Keypoints from '@/views/Keypoints.vue';

const routes = [
  {
    path: '/',
    name: 'landing',
    component: Landing,
  },
  {
    path: '/mesures-phares',
    name: 'keypoints',
    component: Keypoints,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
