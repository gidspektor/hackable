<template>
	<div class="card-container">
		<h1 class="card-title">{{ title }}</h1>
		<p v-if="content" class="card-body">{{ content }}</p>
	</div>
</template>

<script setup lang="ts">
defineProps<{
	title: string
	content?: string
}>()
</script>

<style scoped>
.card-container {
	border: 1px solid white; /* Thin white border */
	border-radius: 12px; /* Rounded corners */
	background: transparent; /* Clear background */
	padding: 1.5rem; /* Spacing inside the container */
	width: 100%; /* Make it take up the full width */
	max-width: 100%; /* Ensure it doesn't exceed the full width */
	margin: 1rem 0; /* Center the container and give some spacing */
	height: 100%;
	text-align: center;
	transition:
		background 0.3s ease,
		opacity 0.3s ease;
}

.card-container:hover {
	background-color: rgba(255, 255, 255, 0.1); /* Slight opaque white on hover */
	opacity: 0.95; /* Slightly transparent effect on hover */
}

.card-title {
	font-size: 1.8rem;
	font-weight: 600;
	margin-bottom: 0.5rem;
	color: green; /* Green title color */
}

.card-body {
	font-size: 1rem;
	color: white; /* Ensure text is visible */
}
</style>
