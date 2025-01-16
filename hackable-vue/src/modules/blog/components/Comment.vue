<template>
	<div class="comment">
		<p class="comment-user">{{ comment.user }}</p>
		<p>{{ comment.body }}</p>
	</div>
</template>

<script setup lang="ts">
defineProps<{
	comment: array<{
		id: number
		userId: number
		user: string
		body: string
	}>
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
