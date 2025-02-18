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
			path: '/articles',
			children: [
				{ path: '', name: 'articles', component: () => import('@articles/views/ArticleHomeView.vue') },
				{
					path: 'create',
					name: 'create-article',
					component: () => import('@articles/views/CreateArticleView.vue'),
				},
				{
					path: 'article/:id',
					name: 'article',
					component: () => import('@articles/views/ArticleView.vue'),
				}
			],
		},
		{
			path: '/account',
			name: 'account',
			component: () => import('@/views/AccountView.vue'),
		},
		{
			path: '/walkthrough',
			name: 'walkthrough',
			component: () => import('@/views/WalkthroughView.vue'),
		},
	],
})

export default router
