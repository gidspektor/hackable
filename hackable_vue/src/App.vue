<template>
	<div id="app">
		<header>
			<div class="wrapper">
				<nav>
					<RouterLink :to="{ name: 'home' }">Home</RouterLink>
					<RouterLink :to="{ name: 'articles' }">Articles</RouterLink>
					<RouterLink v-if="Object.keys(user).length == 0" :to="{ name: 'login' }">Login/Signup</RouterLink>
					<RouterLink v-if="Object.keys(user).length > 0" :to="{ name: 'account' }">My Account</RouterLink>
					<RouterLink v-if="admin" :to="{ name: 'create-article' }">Create Article</RouterLink>
					<a v-if="Object.keys(user).length > 0" @click="logout">Logout</a>
				</nav>
			</div>
		</header>
		<main>
			<RouterView />
		</main>
	</div>
</template>

<script setup>
	import { useHackableStore } from '@/shared/hackableStore'
	import { onMounted, computed } from 'vue'
	import { RouterLink, RouterView } from 'vue-router'

	const hackableStore = useHackableStore()

	const user = computed(() => hackableStore.user)

	const logout = async () => {
		await hackableStore.logout()
	}

	const admin = document.cookie
		.split('; ')
		.find((row) => row.startsWith('is_admin='))
		?.split("=")[1] == 'true';

	onMounted(async () => {
		try {
			await hackableStore.refreshToken()
			await hackableStore.getUser()
		} catch (error) {
			console.error('Failed to get user data:', error)
		}
	})
</script>

<style scoped>
#app {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
	width: 100vw;
}

header {
	line-height: 1.5;
	width: 100%;
	background: var(--color-background, #f8f9fa);
	padding: 1rem 0;
	border-bottom: 1px solid var(--color-border, #ddd);
}

header .wrapper {
	display: flex;
	justify-content: center;
	align-items: center;
}

nav {
	font-size: 14px;
	text-align: center;
}

nav a {
	display: inline-block;
	padding: 0 1rem;
	border-left: 1px solid var(--color-border, #ddd);
	text-decoration: none;
	color: var(--color-text, #333);
	cursor: pointer;
}

nav a:first-of-type {
	border: none;
}

nav a.router-link-exact-active {
	font-weight: bold;
	color: var(--color-primary, #42b983);
}

main {
	flex: 1;
	padding: 2rem;
	overflow-y: auto;
}
</style>
