import { defineStore } from 'pinia'
import ArticlesService from './articlesService.js'
import { reactive, computed } from 'vue'

export const useArticlesStore = defineStore('articles', () => {
	const state = reactive({
		articles: [],
		selectedArticle: [],
		userArticles: [],
		userCommentedOnArticles: [],
	})

	return {
		articles: computed(() => state.articles),
		selectedArticle: computed(() => state.selectedArticle),
		getArticles,
		getArticle,
		createComment,
		createArticle,
		getUserArticles,
		getUserCommentedOnArticles,
	}

	async function getArticles() {
		state.articles = [
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

		// state.articles = await ArticlesService.getArticles()
	}

	async function getArticle(id) {
		state.selectedArticle = {
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
		// state.selectedArticle = await ArticlesService.getArticle(id)
	}

	async function createComment(postId, comment) {
		// return response = await ArticlesService.createComment({'id': postId, 'body': comment})
	}

	async function createArticle(userId, title, body) {
		// state.selectedArticle = {
		// 	id: 1,
		// 	userId: 1,
		// 	user: 'user1',
		// 	title: title,
		// 	body: body,
		// 	comments: [
		// 		{
		// 			id: 1,
		// 			userId: 1,
		// 			user: 'user1',
		// 			body: 'I love cats',
		// 		},
		// 		{
		// 			id: 2,
		// 			userId: 2,
		// 			user: 'user2',
		// 			body: 'I love dogs',
		// 		},
		// 	],
		// }
		// return response = await ArticlesService.createArticle({'user_id': userId, 'body': body, 'title': title})
	}

	async function getUserArticles() {
		// state.articles = await ArticlesService.getUserArticles()
	}

	async function getUserCommentedOnArticles() {
		// state.userCommentedOnArticles = await ArticlesService.getUserCommentedOnArticles()
	}
})
