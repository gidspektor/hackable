import { defineStore } from 'pinia'
import ArticlesService from './articlesService.js'
import { reactive, toRefs, shallowRef } from 'vue'

export const useArticlesStore = defineStore('articles', () => {
	const state = reactive({
		selectedArticle: [],
		selectedArticleComments: [],
		userArticles: [],
		userComments: [],
		featuredArticles: [],
		commentsOffset: 0,
	})

	const articlesPreviews = shallowRef([])

	return {
		...toRefs(state),
		articlesPreviews,
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
		articlesPreviews.value = response?.data?.articles
	}

	async function getArticle(articleId) {
		const response = await ArticlesService.getArticle(articleId)
		state.selectedArticle = response?.data
	}

	async function getArticleComments(articleId) {
		const response = await ArticlesService.getArticleComments(articleId, state.commentsOffset)

		state.selectedArticleComments = response?.data?.comments

		updateCommentsOffset(state.selectedArticleComments.length)
	}

	function updateCommentsOffset(offset) {
		state.commentsOffset = offset
	}

	async function getFeaturedArticles() {
		const response = await ArticlesService.getFeaturedArticles()
		state.featuredArticles = response?.data?.length === 3 ? response?.data?.articles : response?.data?.articles.slice(0, 3)
	}

	async function createComment(articleId, comment) {
		const response = await ArticlesService.createComment({'article_id': articleId, 'comment': comment})
		state.selectedArticleComments.push(response?.data?.comments)

		updateCommentsOffset(state.commentsOffset + 1)
	}

	async function createArticle(title, body, isFeatured) {
		const response = await ArticlesService.createArticle({'content': body, 'title': title, 'featured': isFeatured})

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
