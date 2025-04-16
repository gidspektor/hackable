<template>
	<div v-if="isLoading">
		<p class="green">Loading article...</p>
	</div>
	<div v-else class="posts-container">
		<div class="post">
			<Article :article="article" />
		</div>
		<CreateComment :articleId="article.id" @login="openLoginModal" class="create-comment" />
		<div v-if="isLoadingComments">
			<p class="green">Loading comments...</p>
		</div>
		<div v-else class="comments">
			<div v-for="comment in articleComments" :key="comment.id" class="comment">
				<Comment :comment="comment" />
			</div>
		</div>
	</div>
	<div class="overlay" v-show="showModal">
		<transition name="fade">
			<LoginSignupModal id="modal" class="myModal" v-show="showModal" @close="showModal = false" />
		</transition>
	</div>
</template>

<script setup lang="ts">
	import { ref, onMounted, computed } from 'vue'
	import { useRoute } from 'vue-router'
	import { useArticlesStore } from '@articles/shared/articlesStore'

	import Article from '@articles/components/Article.vue'
	import Comment from '@articles/components/Comment.vue'
	import CreateComment from '@articles/components/CreateComment.vue'
	import LoginSignupModal from '@/components/modals/LoginSignupModal.vue'

	const route = useRoute()
	const showModal = ref<boolean>(false)
	const articlesStore = useArticlesStore()

	const articleId = ref<number>(Number(route.params.id))
	const isLoading = ref<boolean>(false)
	const isLoadingComments = ref<boolean>(false)
	const article = computed(() => articlesStore.selectedArticle)
	const articleComments = computed(() => articlesStore.selectedArticleComments)

	const openLoginModal = () => {
		showModal.value = true
	}

	const getArticle = async () => {
		isLoading.value = true
		try {
			await articlesStore.getArticle(articleId.value)
		} catch (error) {
			console.error('Failed to fetch article:', error)
		} finally {
			isLoading.value = false
		}
	}

	const getArticleComments = async () => {
		isLoadingComments.value = true

		try {
			await articlesStore.getArticleComments(articleId.value)
		} catch (error) {
			console.error('Failed to fetch comments:', error)
		} finally {
			isLoadingComments.value = false
		}
	}

	onMounted(async () => {
		articlesStore.updateCommentsOffset(0)
		articlesStore.setSelectedArticleComments()
		await getArticle()
		await getArticleComments()
	})
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

/* Comments Styling */
.comments {
	margin-top: 2rem; /* Add spacing between the post and comments */
}

.comment {
	margin-bottom: 1rem; /* Add spacing between comments */
}

.post {
	margin-bottom: 2rem; /* Add spacing between the post and create comment */
}
</style>
