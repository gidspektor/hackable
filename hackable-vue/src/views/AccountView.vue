<template>
	<div class="image">
		<img
			:src="userImageUrl"
			class="rounded-circle"
			width="150"
		/>
	</div>
	<div class="section">
		<h6>Full Name</h6>
		<div class="col-sm-9 text-secondary">
			{{ user.first_name }} {{ user.last_name }}
		</div>
	</div>
	
	<div class="section">
		<h6 class="mb-0">Email</h6>
		<div class="col-4 text-secondary">
			{{ user.email }}
		</div>
	</div>

	<div class="section">
		<h6 class="mb-0">Update Password?</h6>
		<div class="col-4 text-secondary">
			<a href="#/Account" @click="updatePassword">Click to update password</a>
		</div>
	</div>

	<div class="section router-links">
		<div class="router-section">
			<i>
				Your Articles
			</i>
			<div>
				<router-link
					v-for="article in userArticles"
					:key="article.id"
					:to="{ name: 'article', params: { id: article.id } }"
					class="article-item"
				>
					{{ article.title }}
				</router-link>
			</div>
		</div>

		<div class="router-section">
			<i>
				Articles You've Commented On
			</i>
			<div>
				<router-link
					v-for="userCommentedOnArticle in userCommentedOnArticles"
					:key="userCommentedOnArticle.id"
					:to="{ name: 'article', params: { id: userCommentedOnArticle.id } }"
					class="post-item"
				>
					{{ userCommentedOnArticle.title }}
				</router-link>
			</div>
		</div>
	</div>
</template>

<script setup lang='ts'>
import { onMounted, computed } from 'vue';

import { useArticlesStore } from '@articles/shared/articlesStore';
import { useHackableStore } from '@/shared/hackableStore';

const articlesStore = useArticlesStore();
const hackableStore = useHackableStore();

const user = computed(() => hackableStore.user);
const userArticles = computed(() => articlesStore.userArticles);
const userCommentedOnArticles = computed(() => articlesStore.userCommentedOnArticles);
const userImageUrl = computed(() => hackableStore.userImageUrl);

const getUserArticles = async () => {
	try {
		await articlesStore.getUserArticles();
	} catch (error) {
		console.error('Failed to fetch user articles:', error);
	}
};

const getUserCommentedOnArticles = async () => {
	try {
		await articlesStore.getUserCommentedOnArticles();
	} catch (error) {
		console.error('Failed to fetch user commented on articles:', error);
	}
};

const getUserImage = async () => {
	try {
		await hackableStore.getUserImage();
	} catch (error) {
		console.error('Failed to fetch user image:', error);
	}
};

onMounted(async () => {
	await getUserCommentedOnArticles();
	await getUserArticles();
	await getUserImage();
});
</script>

<style scoped>
.section {
	border-bottom: 1px solid white;
	margin-bottom: 1rem;
}

.router-links {
	display: flex;
	justify-content: space-between;
}

.router-section {
	width: 48%;
}

.article-item,
.post-item {
	display: block;
	margin-bottom: 0.5rem;
}

.image {
	margin-bottom: 2rem;
}
</style>
