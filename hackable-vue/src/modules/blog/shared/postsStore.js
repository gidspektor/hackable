import { defineStore } from 'pinia'
import PostsService from './postsService.js'

export const usePostsStore = defineStore('posts', {
  state: () => {
    return {
      posts: [],
      selectedPost: []
    }
  },

  actions: {
    async getPosts() {
      this.posts = [
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
      // this.posts = await PostsService.getPosts()
    },

    async getPost(id) {
      console.log('getPost', id)
      this.selectedPost = {
        id: 1,
        userId: 1,
        user: 'user1',
        title: 'pies are ok',
        body: 'but not cats',
        comments: [
          {
            id: 1,
            userId: 1,
            user: 'user1',
            body: 'I love cats'
          },
          {
            id: 2,
            userId: 2,
            user: 'user2',
            body: 'I love dogs'
          }
        ]
      }
      // this.selectedPost = await PostsService.getPost(id)

    }
  },
})
