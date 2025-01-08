import api from '../../../shared/api.js'

const BASE_ROUTE = 'hackable'

export default class PostsService {
  async GetPosts() {
    return await api.GET(`${BASE_ROUTE}/posts/`)
  }
}
