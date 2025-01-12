import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/blogs',
      name: 'blogs',
      component: () => import('@blog/views/BlogHomeView.vue'),
    },
    {
      path: '/post/:id',
      name: 'post',
      component: () => import('@blog/views/PostView.vue'),
    },
    {
      path: '/walkthrough',
      name: 'walkthrough',
      component: () => import('@blog/views/WalkthroughView.vue'),
    },
  ],
})

export default router
