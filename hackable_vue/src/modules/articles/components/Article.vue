<template>
	<div class="post">
		<h1 class="post-title" v-html="article.title"></h1>
		<p class="post-content" v-html="article.content"></p>
		<p class="post-user">{{ article.username }}</p>
	</div>
</template>

<script setup lang="ts">
defineProps<{
	article: {
		title: string
		content: string
		username: string
	}
}>()

</script>

<style scoped>
/* Post Styling */
.post {
	border-bottom: 1px solid white; /* Thin white border at the bottom */
	padding: 1rem 2rem; /* Add spacing inside the post */
	color: white; /* Default text color for content */
	position: relative; /* To position user text at bottom-left */
}

/* Title Styling */
.post-title {
	font-size: 1.8rem;
	font-weight: bold;
	color: green; /* Title is green */
	margin-bottom: 1rem; /* Add spacing after the title */
	text-align: center; /* Center the title */
}

/* Content Styling */
.post-content {
	margin-bottom: 2rem; /* Add spacing after the content */
	text-align: center; /* Center the title */
}

/* User Styling */
.post-user {
	position: absolute;
	bottom: 1rem; /* Position user at the bottom */
	left: 2rem; /* Align user to the left */
	font-size: 0.9rem;
	opacity: 0.8; /* Slightly faded user info */
}
</style>
