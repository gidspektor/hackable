<template>
	<div v-if="isLoading">
		<p class="green">Loading post...</p>
	</div>
	<div v-else class="posts-container">
			<div class="post">
				<Post :post="post" />
			</div>
			<CreateComment :postId="post.id" @login="openLoginModal" class="create-comment" />
			<div class="comments">
				<div v-for="comment in post.comments" :key="comment.id" class="comment">
					<Comment :comment="comment" />
				</div>
			</div>
	</div>
	<div class='overlay' v-show='showModal'>
		<transition name='fade'>
			<LoginSignupModal
				id='modal'
				class='myModal'
				v-show='showModal'
				@close="showModal = false"
			/>
		</transition>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { usePostsStore } from '../shared/postsStore';

import Post from '@blog/components/Post.vue';
import Comment from '@blog/components/Comment.vue';
import CreateComment from '@blog/components/CreateComment.vue';
import LoginSignupModal from '@blog/components/modals/LoginSignupModal.vue';

const route = useRoute();
const showModal = ref<boolean>(false);
const postsStore = usePostsStore();

const postId = ref<int>(route.params.id);
const isLoading = ref<boolean>(false);
const post = computed(() => postsStore.selectedPost);

const openLoginModal = () => {
    showModal.value = true;
};

const getPost = async () => {
    isLoading.value = true;
    try {
        await postsStore.getPost(postId.value);
    } catch (error) {
        console.error('Failed to fetch posts:', error);
    } finally {
        isLoading.value = false;
    }
}

onMounted(async () => {
  await getPost();
});
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(128,128,128,0.5);
}

.myModal {
  z-index: 1000;
  position: fixed;
  top: 40%;
  left: 50%;
  width:30em;
  height:18em;
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
