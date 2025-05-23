import { createRouter, createWebHistory } from 'vue-router';
import Registration from '../components/Registration.vue';
import MainPage from '../components/MainPage.vue';
import PreliminaryQuiz from '../components/PreliminaryQuiz.vue';

const routes = [
  {
    path: '/register',
    name: 'Registration',
    component: Registration,
  },
  {
    path: '/quiz',
    name: 'PreliminaryQuiz',
    component: PreliminaryQuiz,
  },
  {
    path: '/main',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/',
    redirect: '/main',
  },
];

const router = createRouter({
  history: createWebHistory('/adir'),
  routes,
});

export default router;
