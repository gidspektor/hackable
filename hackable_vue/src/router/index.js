import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useHackableStore } from '@/shared/hackableStore'

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
					meta: { requiresAdmin: true },
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
			meta: { requiresUser: true },
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('@/views/LoginSignUpView.vue'),
		}
	],
})

router.beforeEach((to, from, next) => {
	if (to.meta.requiresAdmin) {
		const admin = document.cookie
			.split('; ')
			.find((row) => row.startsWith('is_admin='))
			?.split("=")[1];

		if (admin !== 'true') {
			alert('You must be an admin to access this page!');
			return next('/');
		}
	} else if (to.meta.requiresUser) {
		const hackableStore = useHackableStore()

		if (!hackableStore.getJwtToken()) {
			return next('/');
		}
	}
	next();
});

export default router
