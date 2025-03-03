import { defineStore } from 'pinia'
import ArticlesService from './articlesService.js'
import { reactive, computed } from 'vue'

export const useArticlesStore = defineStore('articles', () => {
	const state = reactive({
		articles: [],
		selectedArticle: [],
		selectedArticleComments: [],
		userArticles: [],
		userCommentedOnArticles: [],
		featuredArticles: [],
		commentsOffset: 0,
	})

	return {
		articles: computed(() => state.articles),
		selectedArticle: computed(() => state.selectedArticle),
		userArticles: computed(() => state.userArticles),
		userCommentedOnArticles: computed(() => state.userCommentedOnArticles),
		selectedArticleComments: computed(() => state.selectedArticleComments),
		featuredArticles: computed(() => state.featuredArticles),
		getArticlePreviews,
		getArticle,
		getArticleComments,
		createComment,
		createArticle,
		getUserArticles,
		getUserCommentedOnArticles,
		getFeaturedArticles,
	}

	async function getArticlePreviews() {
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

		// state.articles = await ArticlesService.getArticlePreviews()
	}

	async function getArticle(articleId) {
		state.selectedArticle = {
			id: 1,
			userId: 1,
			user: 'user1',
			title: 'pies are ok',
			body: 'but not cats'
		}
		// state.selectedArticle = await ArticlesService.getArticle(articleId)
	}

	async function getArticleComments(articleId) {
		state.selectedArticleComments =  [
			{
				id: 1,
				articleId: 1,
				userId: 1,
				user: 'user1',
				body: 'I love cats',
			},
			{
				id: 2,
				articleId: 1,
				userId: 2,
				user: 'user2',
				body: 'I love dogs',
			},
		]
		// state.selectedArticleComments = await ArticlesService.getArticleComments(articleId, state.commentsOffset)
		// state.commentsOffset += state.selectedArticleComments.length + 1
	}

	async function getFeaturedArticles() {
		state.featuredArticles = [
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
		// const response = await ArticlesService.getFeaturedArticles()
		// response.length = 3 ? state.featuredArticles = response : state.featuredArticles = response.slice(0, 3)
	}

	async function createComment(articleId, comment) {
		// return response = await ArticlesService.createComment({'id': postId, 'body': comment})
		// await getArticleComments(articleId)
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
		state.userArticles = [
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
		// state.userArticles = await ArticlesService.getUserArticles()
	}

	async function getUserCommentedOnArticles() {
		state.userCommentedOnArticles = [
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
		// state.userCommentedOnArticles = await ArticlesService.getUserCommentedOnArticles()
	}
},
	{
		persist: true,
	}
)
