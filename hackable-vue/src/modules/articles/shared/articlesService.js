import api from '@/shared/api.js'
import { BASE_ROUTE } from '@/shared/constants.js'

export default class ArticlesService {
	async getArticles() {
		return await api.GET(`${BASE_ROUTE}/articles/`)
	}

	async getArticle(id) {
		return await api.GET(`${BASE_ROUTE}/article/${id}`)
	}

	async createArticle(params) {
		return await api.POST(`${BASE_ROUTE}/article/`, params)
	}

	async createComment(params) {
		return await api.POST(`${BASE_ROUTE}/comment/`, params)
	}

	async getUserArticles() {
		return await api.GET(`${BASE_ROUTE}/user/articles`)
	}

	async getUserCommentedOnArticles() {
		return await api.GET(`${BASE_ROUTE}/user/commented/articles`)
	}

	async getArticleComments(id) {
		return await api.GET(`${BASE_ROUTE}/article/${id}/comments`)
	}
}
