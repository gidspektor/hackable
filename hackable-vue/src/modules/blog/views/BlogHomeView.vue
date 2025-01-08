<template>
  <div v-if="isLoading">
    <p class="green">Loading posts...</p>
  </div>
  <div v-else class="posts-container">
    <div class="posts">
      <router-link v-for="post in posts" :key="post.id" :to="`/post/${post.id}`" class="post-item">
        <PostPreview :title="post.title" :body="post.body" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { usePostsStore } from '../shared/postsStore';
import PostPreview from '../components/PostPreview.vue';

const postsStore = usePostsStore();

const posts = ref([]);
const isLoading = ref(false);

const getPosts = async () => {
  isLoading.value = true;
  try {
    await postsStore.getPosts();
    posts.value = postsStore.posts;
  } catch (error) {
    console.error('Failed to fetch posts:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  getPosts();
});
</script>

<style scoped>
.posts-container {
  width: 100%;
  padding: 1rem;
  display: flex;
  justify-content: center;
}

.posts {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  width: 100%;
  max-width: 800px; /* Optional: limit max width for better readability */
}

.post-item {
  width: 100%;
  box-sizing: border-box;
  text-decoration: none; /* Remove underline on links */
  color: inherit; /* Inherit color from parent */
  transition: none; /* Disable any transition effects */
}

.post-item:hover {
  background-color: transparent; /* Remove any hover effect */
  opacity: 1; /* Ensure no opacity change on hover */
}

@media (max-width: 768px) {
  .post-item {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .post-item {
    width: 100%;
  }
}
</style>
