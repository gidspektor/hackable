<template>
    <div v-if="isLoading">
        <p class="green">Loading post...</p>
    </div>
    <div v-else class="posts-container">
        <div class="post">
           
        </div>
    </div>
</template>

<script setup lang="ts">
import PostPreview from '../components/PostPreview.vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const postId = ref(route.params.id);

const postsStore = usePostsStore();
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
</script>

<style>

</style>
