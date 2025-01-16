import { defineStore } from 'pinia'
import PostsService from './postsService.js'
import { reactive, computed } from 'vue'

export const usePostsStore = defineStore('posts', () => {
	const state = reactive({
		posts: [],
		selectedPost: [],
	})

	return {
		posts: computed(() => state.posts),
		selectedPost: computed(() => state.selectedPost),
		getPosts,
		getPost,
		createComment,
		createPost,
	}

	async function getPosts() {
		state.posts = [
			{
				id: 1,
				title: 'pies are ok',
				body: 'but not cats',
			},
			{
				id: 2,
				title: 'cats are better',
				body: 'but not dogs',
			},
			{
				id: 3,
				title: 'dogs are the best',
				body: 'but not cats',
			},
		]
		// state.posts = await PostsService.getPosts()
	}

	async function getPost(id) {
		state.selectedPost = {
			id: 1,
			userId: 1,
			user: 'user1',
			title: 'pies are ok',
			body: 'but not cats',
			comments: [
				{
					id: 1,
					userId: 1,
					user: 'user1',
					body: 'I love cats',
				},
				{
					id: 2,
					userId: 2,
					user: 'user2',
					body: 'I love dogs',
				},
			],
		}
		// state.selectedPost = await PostsService.getPost(id)
	}

	async function createComment(postId, comment) {
		// return response = await PostsService.createComment({'id': postId, 'body': comment})
	}

	async function createPost(userId, title, body) {
		// return response = await PostsService.createPost({'user_id': userId, 'body': body, 'title': title})
	}
})
