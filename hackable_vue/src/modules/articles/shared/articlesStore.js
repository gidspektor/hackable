import { defineStore } from 'pinia'
import ArticlesService from './articlesService.js'
import { reactive, computed } from 'vue'

export const useArticlesStore = defineStore('articles', () => {
	const state = reactive({
		articles: [],
		selectedArticle: [],
		selectedArticleComments: [],
		userArticles: [],
		userComments: [],
		featuredArticles: [],
		commentsOffset: 0,
	})

	return {
		articles: computed(() => state.articles),
		selectedArticle: computed(() => state.selectedArticle),
		userArticles: computed(() => state.userArticles),
		userComments: computed(() => state.userComments),
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
		const response = await ArticlesService.getArticlePreviews()
		state.articles = response?.data
	}

	async function getArticle(articleId) {
		const response = await ArticlesService.getArticle(articleId)
		state.selectedArticle = response?.data
	}

	async function getArticleComments(articleId) {
		const response = await ArticlesService.getArticleComments(articleId, state.commentsOffset)

		state.selectedArticleComments = response?.data

		updateCommentsOffset(state.commentsOffset + state.selectedArticleComments.length)
	}

	function updateCommentsOffset(offset) {
		state.commentsOffset = offset
	}

	async function getFeaturedArticles() {
		const response = await ArticlesService.getFeaturedArticles()
		state.featuredArticles = response.length = 3 ? response?.data : response?.data.slice(0, 3)
	}

	async function createComment(comment) {
		const response = await ArticlesService.createComment({'id': postId, 'body': comment})
		state.selectedArticleComments.push(response?.data)

		updateCommentsOffset(state.commentsOffset + 1)
	}

	async function createArticle(title, body, isFeatured) {
		const response = await ArticlesService.createArticle({'body': body, 'title': title, 'featured': isFeatured})

		return response?.data
	}

	async function getUserArticles() {
		const response = await ArticlesService.getUserArticles()
		state.userArticles = response?.data
	}

	async function getUserCommentedOnArticles() {
		const response = await ArticlesService.getUserCommentedOnArticles()
		state.userComments = response?.data
	}
},
	{
		persist: true,
	}
)
