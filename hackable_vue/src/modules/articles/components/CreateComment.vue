<template>
	<div v-if="active" class="text-box-container">
		<textarea
			v-model="comment"
			class="text-box"
			placeholder="Write your comment here..."
		></textarea>
		<div class="buttons-container">
			<button class="cancel-button" @click="cancelComment">Cancel</button>
			<button class="submit-button" @click="submitComment">Submit</button>
		</div>
	</div>
	<button v-else @click="openCommentBox" class="add-comment-button">Add Comment +</button>
</template>

<script setup>
import { useHackableStore } from '@/shared/hackableStore'
import { useArticlesStore } from '@articles/shared/articlesStore'
import { ref, computed } from 'vue'

const props = defineProps({
	articleId: {
		type: Number,
		required: true
	}
})

const articlesStore = useArticlesStore()
const hackableStore = useHackableStore()

const active = ref(false)
const comment = ref('')

const emit = defineEmits(['login'])
const user = computed(() => hackableStore.user)

const openCommentBox = () => {
	user.value ? (active.value = true) : emit('login')
}

const cancelComment = () => {
	active.value = false
}

const submitComment = async () => {
	if (comment.value) {
		await articlesStore.createComment(props.articleId, comment.value)
		active.value = false
	}
}
</script>

<style scoped>
.text-box-container {
	width: 100%;
	padding: 1rem;
	display: flex;
	flex-direction: column;
	gap: 1rem;
	background-color: #f8f8f8;
	border-radius: 8px;
}

.text-box {
	width: 100%;
	height: 150px;
	padding: 1rem;
	border: 2px solid white;
	border-radius: 8px;
	font-size: 1rem;
	color: black;
	background-color: #f8f8f8;
	resize: none;
	outline: none;
}

.buttons-container {
	display: flex;
	justify-content: space-between;
	width: 100%;
}

.cancel-button {
	background-color: red;
	color: white;
	border: none;
	border-radius: 8px;
	padding: 0.5rem 1rem;
	cursor: pointer;
	font-weight: bold;
	transition: background-color 0.3s;
}

.cancel-button:hover {
	background-color: darkred;
}

.submit-button {
	background-color: green;
	color: white;
	border: none;
	border-radius: 8px;
	padding: 0.5rem 1rem;
	cursor: pointer;
	font-weight: bold;
	transition: background-color 0.3s;
}

.submit-button:hover {
	background-color: darkgreen;
}

.add-comment-button {
	width: 100%;
	padding: 1rem;
	border: 2px solid white;
	border-radius: 12px;
	background: transparent;
	color: white;
	font-size: 1.2rem;
	font-weight: bold;
	text-align: center;
	cursor: pointer;
	transition:
		background-color 0.3s,
		color 0.3s;
}

.add-comment-button:hover {
	background-color: white;
	color: black;
}
</style>
