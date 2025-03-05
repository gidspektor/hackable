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
		response = await ArticlesService.getArticlePreviews()
		state.articles = response.data
	}

	async function getArticle(articleId) {
		response = await ArticlesService.getArticle(articleId)
		state.selectedArticle = response.data
	}

	async function getArticleComments(articleId) {
		response = await ArticlesService.getArticleComments(articleId, state.commentsOffset)

		state.selectedArticleComments = response.data

		updateCommentsOffset(state.commentsOffset + state.selectedArticleComments.length)
	}

	function updateCommentsOffset(offset) {
		state.commentsOffset = offset
	}

	async function getFeaturedArticles() {
		const response = await ArticlesService.getFeaturedArticles()
		response.length = 3 ? state.featuredArticles = response.data : state.featuredArticles = response.data.slice(0, 3)
	}

	async function createComment(comment) {
		response = await ArticlesService.createComment({'id': postId, 'body': comment})
		state.selectedArticleComments.push(response.data)

		updateCommentsOffset(state.commentsOffset + 1)
	}

	async function createArticle(title, body) {
		return await ArticlesService.createArticle({'body': body, 'title': title})
	}

	async function getUserArticles() {
		response = await ArticlesService.getUserArticles()
		state.userArticles = response.data
	}

	async function getUserCommentedOnArticles() {
		response = await ArticlesService.getUserCommentedOnArticles()
		state.userComments = response.data
	}
},
	{
		persist: true,
	}
)
