<template>
    <div v-if="isLoading">
        <p class="green">Loading post...</p>
    </div>
    <div v-else class="posts-container">
        <div class="post">
           <Post :post="post" />
        </div>
        <div class="comments">
            <div v-for="comment in post.comments" :key="comment.id" class="comment">
                <Comment :comment="comment" />
            </div>
        </div>
        <!-- if logged in add comment form -->
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import Post from '../components/Post.vue';
import Comment from '../components/Comment.vue';
import { useRoute } from 'vue-router';
import { usePostsStore } from '../shared/postsStore';

const route = useRoute();
const postsStore = usePostsStore();

const postId = ref(route.params.id);
const isLoading = ref(false);
const post = computed(() => postsStore.selectedPost);

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
    console.log('pie')
    await getPost();
});
</script>

<style>
/* Comments Styling */
.comments {
    margin-top: 2rem; /* Add spacing between the post and comments */
}

.comment {
    margin-bottom: 1rem; /* Add spacing between comments */
}
</style>
