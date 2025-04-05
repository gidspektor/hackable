import api from '@/shared/api.js'
import { BASE_ROUTE } from '@/shared/constants.js'

class ArticlesService {
	async getArticlePreviews() {
		return await api.GET(`${BASE_ROUTE}/v1/article_previews/`, '', true)
	}

	async getArticle(id) {
		return await api.GET(`${BASE_ROUTE}/v1/article/${id}/`, '', true)
	}

	async createArticle(params) {
		return await api.POST(`${BASE_ROUTE}/v1/article/`, params)
	}

	async createComment(params) {
		return await api.POST(`${BASE_ROUTE}/v1/comment/`, params)
	}

	async getUserArticles() {
		return await api.GET(`${BASE_ROUTE}/v1/user/articles/`)
	}

	async getUserComments() {
		return await api.GET(`${BASE_ROUTE}/v1/user/comments/`)
	}

	async getFeaturedArticles() {
		return await api.GET(`${BASE_ROUTE}/v1/articles/featured/`, '', true)
	}

	async getArticleComments(id, offset) {
		return await api.GET(`${BASE_ROUTE}/v1/article/${id}/comments/${offset}/`)
	}
}

export default new ArticlesService()
