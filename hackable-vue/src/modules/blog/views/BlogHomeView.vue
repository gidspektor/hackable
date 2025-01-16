<template>
	<aside class="sidebar">
		<a :href="createPostUrl" class="sidebar-link">
    	Create Post
  	</a>
		<p class="sidebar-link" @click="openLoginModal">
			Login/Sign Up
		</p>
	</aside>
	<main class="main-content">
		<div v-if="isLoading">
			<p class="green loading">Loading posts...</p>
		</div>
		<div v-else class="posts-container">
			<div class="posts">
				<router-link
					v-for="post in posts"
					:key="post.id"
					:to="{ name: 'post', params: { id: post.id } }"
					class="post-item"
				>
					<PostPreview :title="post.title" :body="post.body" />
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
import { useRouter } from 'vue-router'

import { usePostsStore } from '@blog/shared/postsStore';
import PostPreview from '@blog/components/PostPreview.vue';
import LoginSignupModal from '@blog/components/modals/LoginSignupModal.vue'

const router = useRouter()
const postsStore = usePostsStore();

const createPostUrl = router.resolve({ name: 'create-post' }).href
const posts = computed(() => postsStore.posts);
const isLoading = ref<boolean>(false);
const showModal = ref<boolean>(false)

const getPosts = async () => {
	isLoading.value = true;
	try {
		await postsStore.getPosts();
	} catch (error) {
		console.error('Failed to fetch posts:', error);
	} finally {
		isLoading.value = false;
	}
};

const openLoginModal = () => {
	showModal.value = true
}

onMounted(async () => {
	await getPosts();
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
