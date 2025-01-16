<template>
	<div class="container">
		<div class="post-box">
			<input v-model="title" class="title-input" placeholder="Click Bait Title" />
			<textarea v-model="body" class="body-input" placeholder="What's on your mind?"></textarea>
			<div v-if="error" class="error-message">{{ error }}</div>
			<div class="button-container">
				<button @click="cancelPost" class="cancel-button">Cancel</button>
				<button @click="createPost" class="submit-button">Submit</button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePostsStore } from '@blog/shared/postsStore'
import { useHackableStore } from '@/shared/hackableStore'
import { useRouter } from 'vue-router'

const postsStore = usePostsStore()
const hackableStore = useHackableStore()

const router = useRouter()

const title = ref<string>('')
const body = ref<string>('')
const error = ref<string>('')
const user = computed(() => hackableStore.user)

const cancelPost = () => {
	title.value = ''
	body.value = ''
	router.push({ name: 'blogs' })
}

const createPost = async () => {
	if (title.value && body.value) {
		const response = await postsStore.createPost(user.value.id, title.value, body.value)

		if (response.error) {
			error.value = response.error
		} else {
			title.value = ''
			body.value = ''
			router.push({ name: 'blogs' })
		}
	}
}
</script>

<style scoped>
.container {
	display: flex;
	justify-content: center;
	align-items: flex-start;
	height: 100vh;
	padding-top: 10%;
}

.post-box {
	width: 100%;
	max-width: 1000px;
	padding: 20px;
	border: 1px solid gray;
	border-radius: 3%;
	box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
}

.title-input,
.body-input {
	width: 100%;
	color: white;
	background-color: transparent;
	border: none;
	border-radius: 5px;
	padding: 10px;
	font-size: 16px;
	margin-bottom: 20px;
}

.title-input::placeholder,
.body-input::placeholder {
	color: rgba(255, 255, 255, 0.6);
}

.title-input {
	font-size: 20px;
	color: #4caf50; /* Green color for title text */
	font-weight: bold;
	border-bottom: 1px solid grey;
}

.body-input {
	height: 300px;
	resize: none;
	width: 100%;
	border-bottom: 1px solid grey;
}

.button-container {
	display: flex;
	justify-content: space-between;
}

.cancel-button,
.submit-button {
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	font-size: 16px;
	cursor: pointer;
}

.cancel-button {
	background-color: #e53935; /* Red */
	color: white;
}

.cancel-button:hover {
	background-color: #d32f2f;
}

.submit-button {
	background-color: #4caf50; /* Green */
	color: white;
}

.submit-button:hover {
	background-color: #43a047;
}
</style>
