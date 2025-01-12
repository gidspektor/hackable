import api from '../../../shared/api.js'
import { BASE_ROUTE } from '../../../shared/constants.js'

export default class PostsService {
  async GetPosts() {
    return await api.GET(`${BASE_ROUTE}/posts/`)
  }

  async GetPost(id) {
    return await api.GET(`${BASE_ROUTE}/posts/${id}`)
  }
}
