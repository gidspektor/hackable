<template>
	<div class="image">
		<form :class="userImageUrl ? 'image-uploaded' : 'image-not-uploaded'" @click="() => $refs.media.click()">
			<img
				v-if="userImageUrl"
				:src="userImageUrl"
				width="150"
			/>
			<input
				type="file"
				id="media"
				accept="image/*"
				@change="(event) => handelFileUpload(event)"
				ref="media"
			/>
			<p v-if="!userImageUrl">Upload a user profile image</p>
		</form>
	</div>
	<div class="section">
		<h6>Username</h6>
		<div class="col-sm-9 text-secondary">
			{{ user.username }}
		</div>
	</div>

	<div class="section">
		<h6 class="mb-0">Admin user</h6>
		<div class="col-4 text-secondary">
			{{ user.is_admin }}
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
				Your comments
			</i>
			<div>
				<router-link
					v-for="userComment in userComments"
					:key="userComment.id"
					:to="{ name: 'article', params: { id: userComment.article_id } }"
					class="post-item"
				>
					{{ userComment.comment }}
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
const userComments = computed(() => articlesStore.userComments);
const userImageUrl = computed(() => hackableStore.userImageUrl);

const getUserArticles = async () => {
	try {
		await articlesStore.getUserArticles();
	} catch (error) {
		console.error('Failed to fetch user articles:', error);
	}
};

const getUserComments = async () => {
	try {
		await articlesStore.getUserComments();
	} catch (error) {
		console.error('Failed to fetch user comments:', error);
	}
};

const getUserImage = async () => {
	try {
		await hackableStore.getUserImage();
	} catch (error) {
		console.error('Failed to fetch user image:', error);
	}
};

const handelFileUpload = async (event: Event) => {
	const target = event.target as HTMLInputElement;
	const file = target.files?.[0];
	if (!file) {
		return;
	}

	try {
		await hackableStore.uploadUserImage(file);
	} catch (error) {
		console.error('Failed to upload user image:', error);
	}
};

onMounted(async () => {
	await getUserComments();
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

img {
	border-radius: 20px;
}

.image-not-uploaded {
  width: 500px !important;
  height: 100%;
  border-radius: 5px;
  border: 1.5px dashed #a0a0a0;
  cursor: pointer;
}

.image-uploaded {
	width: 150px;
	height: 100%;
	border-radius: 5px;
	border: none;
	cursor: pointer;
}

form input {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  outline: none;
  opacity: 0;
}

form p {
	margin: 0;
	padding-bottom: 1rem;
	text-align: center;
	font-size: 1.5rem;
	color: #a0a0a0;
}
</style>
