<template>
	<div class="comment">
		<p class="comment-user">{{ comment.username }}</p>
		<p>{{ comment.comment }}</p>
	</div>
</template>

<script setup lang="ts">
defineProps<{
	comment: {
		id: number
		username: string
		comment: string
	}
}>()
</script>

<style scoped>
.comment-user {
	top: 1rem;
	left: 2rem; /* Align user to the left */
	font-size: 0.9rem;
	opacity: 0.8; /* Slightly faded user info */
}
.comment {
	padding-bottom: 1rem;
	border-bottom: 1px solid white;
}
</style>
