<template>
    <div class="comment">
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
    }>,
}>()

</script>

<style>

</style>
