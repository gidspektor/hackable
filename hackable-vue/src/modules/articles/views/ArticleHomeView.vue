<template>
	<aside class="sidebar">
		<p class="sidebar-link">
			<router-link
				:to="{ name: 'create-article' }"
			>
				Create Article
			</router-link>
		</p>
		<p v-if="true" class="sidebar-link" @click="">
			<router-link
				:to="{ name: 'account' }"
			>
				My Account
			</router-link>
		</p>
		<p v-else class="sidebar-link" @click="openLoginModal">
			<router-link
				to="#"
			>
				Login/Sign Up
			</router-link>
		</p>
	</aside>
	<main class="main-content">
		<div v-if="isLoading">
			<p class="green loading">Loading posts...</p>
		</div>
		<div v-else class="posts-container">
			<div class="posts">
				<router-link
					v-for="article in articles"
					:key="article.id"
					:to="{ name: 'article', params: { id: article.id } }"
					class="post-item"
				>
					<ArticlePreview :title="article.title" :body="article.body" />
				</router-link>
			</div>
			<router-view></router-view>
		</div>
	</main>
	<div class="overlay" v-show="showModal">
		<transition name="fade">
			<LoginSignupModal id="modal" class="myModal" v-show="showModal" @close="showModal = false" />
		</transition>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

import { useArticlesStore } from '@articles/shared/articlesStore';
import { useHackableStore } from '@/shared/hackableStore'
import ArticlePreview from '@articles/components/ArticlePreview.vue';
import LoginSignupModal from '@articles/components/modals/LoginSignupModal.vue'

const hackableStore = useHackableStore()
const articlesStore = useArticlesStore();

const user = computed(() => hackableStore.user)
const articles = computed(() => articlesStore.articles);
const isLoading = ref<boolean>(false);
const showModal = ref<boolean>(false)

const getArticles = async () => {
	isLoading.value = true;
	try {
		await articlesStore.getArticles();
	} catch (error) {
		console.error('Failed to fetch articles:', error);
	} finally {
		isLoading.value = false;
	}
};

const openLoginModal = () => {
	showModal.value = true
}

onMounted(async () => {
	await getArticles();
});
</script>

<style scoped>
.overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
	background-color: rgba(128, 128, 128, 0.5);
}

.myModal {
	z-index: 1000;
	position: fixed;
	top: 40%;
	left: 50%;
	width: 30em;
	height: 18em;
	margin-top: -9em;
	margin-left: -15em;
}

.sidebar {
	width: 250px;
	background-color: none;
	padding: 1rem;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	position: absolute;
	left: 10%;
}

.sidebar-link {
	text-decoration: none;
	color: green;
	font-size: 1.2rem;
	font-weight: bold;
	margin-bottom: 1rem;
}

.sidebar-link:hover {
	background: none;
	cursor: pointer;
}

.main-content {
	flex: 1;
	padding: 1rem;
	overflow-y: auto;
}

.loading {
	width: 100%;
	padding: 1rem;
	display: flex;
	justify-content: center;
}

.posts-container {
	width: 100%;
	padding: 1rem;
	display: flex;
	justify-content: center;
}

.posts {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1.5rem;
	width: 100%;
	max-width: 800px;
}

.post-item {
	width: 100%;
	box-sizing: border-box;
	text-decoration: none;
	color: inherit;
	transition: none;
}

.post-item:hover {
	background-color: transparent;
	opacity: 1;
}

@media (max-width: 1030px) {
	.sidebar {
		left: 0;
	}
}

@media (max-width: 768px) {
	.sidebar {
		width: 200px;
	}

	.post-item {
		width: 100%;
	}
}

@media (max-width: 480px) {
	.sidebar {
		width: 150px;
	}

	.post-item {
		width: 100%;
	}
}
</style>
