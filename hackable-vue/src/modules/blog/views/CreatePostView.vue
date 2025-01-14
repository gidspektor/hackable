<template>
    <div>
        <h1>Create a Post</h1>
        <input
        v-model="title"
        class="input-field"
        placeholder="Title"
        />
        <textarea
        v-model="body"
        class="input-field"
        placeholder="Body"
        ></textarea>
        <button @click="createPost" class="action-button">Create Post</button>
    </div>
</template>

<script lang="ts">

</script>

<style scoped>

</style>
