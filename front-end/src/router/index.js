import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/views/LandingPage';
import DiagnosticPage from '@/views/DiagnosticPage';
import KeyMeasuresPage from '@/views/KeyMeasuresPage';
import KeyMeasuresHome from '@/views/KeyMeasuresPage/KeyMeasuresHome';
import KeyMeasurePage from '@/views/KeyMeasuresPage/KeyMeasurePage';
import PublishPage from '@/views/PublishPage';
import CanteenInfo from '@/views/PublishPage/CanteenInfo';
import PublishMeasurePage from '@/views/PublishPage/PublishMeasurePage';
import SubmitPublicationPage from '@/views/PublishPage/SubmitPublicationPage';
import GeneratePosterPage from '@/views/GeneratePosterPage';
import CanteensPage from '@/views/CanteensPage';
import CanteensHome from '@/views/CanteensPage/CanteensHome';
import CanteenPage from '@/views/CanteensPage/CanteenPage';
import LegalNotices from '@/views/LegalNotices';
import ConnectPage from '@/views/ConnectPage';
import LoginPage from '@/views/ConnectPage/LoginPage';
import SignUpPage from '@/views/ConnectPage/SignUpPage';
import AccountSummaryPage from '@/views/ConnectPage/AccountSummaryPage';
import BlogsPage from '@/views/BlogsPage';
import BlogsHome from '@/views/BlogsPage/BlogsHome';
import BlogPage from '@/views/BlogsPage/BlogPage';
import StatsPage from '@/views/StatsPage';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
  {
    path: '/diagnostic',
    name: 'DiagnosticPage',
    component: DiagnosticPage,
    meta: {
      title: "M'auto-évaluer",
    },
  },
  {
    path: '/creation-affiche',
    name: 'GeneratePosterPage',
    component: GeneratePosterPage,
    meta: {
      title: "Générez votre affiche",
    },
  },
  {
    path: '/mesures-phares',
    name: 'KeyMeasuresPage',
    component: KeyMeasuresPage,
    meta: {
      title: "Les 5 mesures phares de la loi EGAlim",
    },
    children: [
      {
        path: '',
        name: 'KeyMeasuresHome',
        component: KeyMeasuresHome,
      },
      {
        path: ':id',
        name: 'KeyMeasurePage',
        component: KeyMeasurePage,
        props: true,
      },
    ],
  },
  {
    path: '/publication',
    name: 'PublishPage',
    component: PublishPage,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        name: 'CanteenInfo',
        component: CanteenInfo,
        meta: {
          title: "Cantine information - Publication",
        },
      },
      {
        path: ':id',
        name: 'PublishMeasurePage',
        component: PublishMeasurePage,
        props: true,
      },
      {
        path: 'validation',
        name: 'SubmitPublicationPage',
        component: SubmitPublicationPage,
        meta: {
          title: "Validation - Publication",
        },
      }
    ]
  },
  {
    path: '/nos-cantines',
    name: 'CanteensPage',
    component: CanteensPage,
    meta: {
      title: "Nos cantines",
    },
    children: [
      {
        path: '',
        name: 'CanteensHome',
        component: CanteensHome,
      },
      {
        path: ':id',
        name: 'CanteenPage',
        component: CanteenPage,
        props: true,
      },
    ],
  },
  {
    path: '/mentions-legales',
    name: 'LegalNotices',
    component: LegalNotices,
    meta: {
      title: "Mentions légales",
    }
  },
  {
    name: 'ConnectPage',
    component: ConnectPage,
    children: [
      {
        path: '/connexion',
        name: 'LoginPage',
        component: LoginPage,
        meta: {
          title: "Connecter"
        }
      },
      {
        path: '/inscription',
        name: 'SignUpPage',
        component: SignUpPage,
        meta: {
          title: "Créer mon compte"
        }
      },
      {
        path: '/mon-compte',
        name: 'AccountSummaryPage',
        component: AccountSummaryPage,
        meta: {
          title: "Mon compte"
        }
      }
    ]
  },
  {
    path: '/blog',
    name: 'BlogsPage',
    component: BlogsPage,
    meta: {
      title: "Blog",
    },
    children: [
      {
        path: '',
        name: 'BlogsHome',
        component: BlogsHome,
      },
      {
        path: ':id',
        name: 'BlogPage',
        component: BlogPage,
        props: true,
      },
    ],
  },
  {
    path: '/stats',
    name: 'StatsPage',
    component: StatsPage,
    meta: {
      title: "Statistiques",
    }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
      return {
        el: to.hash,
        top: 80,
      };
    } else {
      return {
        top: 0,
      };
    }
  },
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth) && !localStorage.getItem('jwt')) {
    next({ path: '/connecter' });
  }

  next();
})

export default router;
