import api from '../../../shared/api.js'
import { BASE_ROUTE } from '../../../shared/constants.js'

export default class PostsService {
  async getPosts() {
    return await api.GET(`${BASE_ROUTE}/posts/`)
  }

  async getPost(id) {
    return await api.GET(`${BASE_ROUTE}/posts/${id}`)
  }

  async createPost(params) {
    return await api.POST(`${BASE_ROUTE}/posts/`, params)
  }
}
