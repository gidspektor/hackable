<template>
	<nav>
		<p v-if="user" class="sidebar-link">
			<router-link
				:to="{ name: 'create-article' }"
			>
				Create Article
			</router-link>
		</p>
		<p v-if="user" class="sidebar-link" @click="">
			<router-link
				:to="{ name: 'account' }"
			>
				My Account
			</router-link>
		</p>
	</nav>

	<main class="main-content">
		<p>Featured</p>
		<div class="top-boxes">
			<router-link
				v-for="featuredArticle in featuredArticles"
				:key="featuredArticle.id"
				:to="{ name: 'article', params: { id: featuredArticle.id } }"
				class="box"
			>
				<ArticlePreview :title="featuredArticle.title" :body="featuredArticle.body" />
			</router-link>
		</div>
		<div v-if="isLoading">
			<p class="green loading">Loading posts...</p>
		</div>
		<div v-else class="posts-container">
			<div class="posts">
				<router-link
					v-for="article in articlesPreviews"
					:key="article.id"
					:to="{ name: 'article', params: { id: article.id } }"
					class="post-item"
				>
					<ArticlePreview :title="article.title" :content="article.content" />
				</router-link>
			</div>
			<router-view></router-view>
		</div>
	</main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';

import { useArticlesStore } from '@articles/shared/articlesStore';
import { useHackableStore } from '@/shared/hackableStore'
import ArticlePreview from '@articles/components/ArticlePreview.vue';

const hackableStore = useHackableStore()
const articlesStore = useArticlesStore();

const user = computed(() => hackableStore.user)
const articlesPreviews = computed(() => articlesStore.articlesPreviews);
const featuredArticles = computed(() => articlesStore.featuredArticles);
const isLoading = ref<boolean>(false);

const getArticlePreviews = async () => {
	isLoading.value = true;
	try {
		await articlesStore.getArticlePreviews();
	} catch (error) {
		console.error('Failed to fetch articles:', error);
	} finally {
		isLoading.value = false;
	}
};

const getFeaturedArticles = async () => {
	try {
		await articlesStore.getFeaturedArticles();
	} catch (error) {
		console.error('Failed to fetch featured articles:', error);
	}
};

onMounted(async () => {
	try {
		await getArticlePreviews();
	} catch (error) {
		console.error('Failed to fetch articles:', error);
	}

	try {
		await getFeaturedArticles();
	} catch (error) {
		console.error('Failed to fetch featured articles:', error);
	}
});
</script>

<style scoped>
nav a {
	display: inline-block;
	padding: 0 1rem;
	border-left: 1px solid var(--color-border, #ddd);
}

nav a:first-of-type {
	border: none;
}

nav {
	width: 100%;
	background-color: none;
	display: flex;
	position: fixed;
	top: 7%;
	left: 40%;
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

.top-boxes {
	display: flex;
	justify-content: space-between;
	gap: 1rem;
	margin-bottom: 2rem;
	height: 200px;
}

.box {
	flex: 1;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 1.5rem;
	font-weight: bold;
	text-align: center;
	color: inherit;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.box:hover {
	background-color: transparent;
	opacity: 1;
}

p {
	font-size: 1.5rem;
	color: white;
	margin-bottom: 1rem;
}

@media (max-width: 768px) {
	.post-item {
		width: 100%;
	}
	.top-boxes {
		flex-direction: column;
	}
	nav {
		top: 15%;
		left: 30%;
	}
}

@media (max-width: 480px) {
	.sidebar {
		width: 150px;
	}

	.post-item {
		width: 100%;
	}
	nav {
		top: 15%;
	}
}
</style>
