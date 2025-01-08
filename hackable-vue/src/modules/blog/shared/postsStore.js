import { defineStore } from 'pinia'
import PostsService from './postsService.js'

export const usePostsStore = defineStore('posts', {
  state: () => {
    return {
      posts: []
    }
  },

  actions: {
    async getPosts() {
      const mock = [
        {
          id: 1,
          title: 'pies are ok',
          body: 'but not cats'
        },
        {
          id: 2,
          title: 'cats are better',
          body: 'but not dogs'
        },
        {
          id: 3,
          title: 'dogs are the best',
          body: 'but not cats'
        }
      ]
      this.posts = mock
      // this.posts = await PostsService.getPosts()
    }
  },
})
