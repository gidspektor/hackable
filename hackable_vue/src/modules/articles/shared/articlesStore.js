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
		updateCommentsOffset,
	}

	async function getArticlePreviews() {
		state.articles = await ArticlesService.getArticlePreviews()
	}

	async function getArticle(articleId) {
		state.selectedArticle = await ArticlesService.getArticle(articleId)
	}

	async function getArticleComments(articleId) {
		state.selectedArticleComments = await ArticlesService.getArticleComments(articleId, state.commentsOffset)
		updateCommentsOffset(state.commentsOffset + state.selectedArticleComments.length)
	}

	function updateCommentsOffset(offset) {
		state.commentsOffset = offset
	}

	async function getFeaturedArticles() {
		const response = await ArticlesService.getFeaturedArticles()
		response.length = 3 ? state.featuredArticles = response : state.featuredArticles = response.slice(0, 3)
	}

	async function createComment(comment) {
		response = await ArticlesService.createComment({'id': postId, 'body': comment})
		state.selectedArticleComments.push(response)

		updateCommentsOffset(state.commentsOffset + 1)
	}

	async function createArticle(title, body) {
		return await ArticlesService.createArticle({'body': body, 'title': title})
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
