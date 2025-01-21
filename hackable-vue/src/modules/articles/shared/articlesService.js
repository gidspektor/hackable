import api from '../../../shared/api.js'
import { BASE_ROUTE } from '../../../shared/constants.js'

export default class ArticlesService {
	async getArticles() {
		return await api.GET(`${BASE_ROUTE}/articles/`)
	}

	async getArticle(id) {
		return await api.GET(`${BASE_ROUTE}/posts/${id}`)
	}

	async createArticle(params) {
		return await api.POST(`${BASE_ROUTE}/posts/`, params)
	}

	async createComment(params) {
		return await api.POST(`${BASE_ROUTE}/comment/`, params)
	}
}
