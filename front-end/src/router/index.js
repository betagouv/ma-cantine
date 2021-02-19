import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/views/LandingPage';
import KeyMeasuresPage from '@/views/KeyMeasuresPage';
import DiagnosticPage from '@/views/DiagnosticPage';

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
    meta: {
      title: "Les 5 mesures phares de la loi EGAlim"
    }
  },
  {
    path: '/auto-evaluer',
    name: 'DiagnosticPage',
    component: DiagnosticPage,
    meta: {
      title: "M'auto-évaluer"
    }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return {
        el: to.hash,
        top: 80
      }
    } else {
      return {
        top: 0
      };
    }
  }
});

export default router;
