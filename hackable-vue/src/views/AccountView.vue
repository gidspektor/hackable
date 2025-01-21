<template>
    <main class='container-fluid mt-5 mb-5 pt-5'>
      <div class='main-body pt-5'>
        <div class='row gutters-sm'>
          <div class='col-md-4 mb-3'>
            <div class='card'>
              <div class='card-body'>
                <div class='text-center'>
                  <img src='~@/assets/img/user.svg' alt='Admin' class='rounded-circle' width='150'>
                  <div class='mt-3'>
                    <h4>{{user.first_name}} {{user.last_name}}</h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class='col-md-8'>
            <div class='card mb-3'>
              <div class='card-body'>
                <div class='row'>
                  <div class='col-sm-3'>
                    <h6 class='mb-0'>Full Name</h6>
                  </div>
                  <div class='col-sm-9 text-secondary'>
                    {{user.first_name}} {{user.last_name}}
                  </div>
                </div>
                <hr>
                <div class='row'>
                  <div class='col-sm-3'>
                    <h6 class='mb-0'>Email</h6>
                  </div>
                  <div class='col-4 text-secondary'>
                    {{user.email}}
                  </div>
                  <a class='col-4' href='#/Account' @click='resetEmail'>Click to receive an email reset link</a>
                </div>
                <hr>
                <div class='row'>
                  <div class='col-sm-3'>
                    <h6 class='mb-0'>Update Password?</h6>
                  </div>
                  <a href='#/Account' @click='resetPassword'>Click to receive reset link via email</a>
                </div>
              </div>
            </div>
            <div class='row gutters-sm'>
              <div class='col-sm-6 mb-3'>
                <div class='card h-100'>
                  <div class='card-body'>
                    <i class='d-flex align-items-center mb-3 material-icons text-info mr-2'>Events coming up</i>
                    <small
                      class='d-block'
                      v-for='(futureEvent, index) in futureEvents'
                      :key='index'
                    >
                      {{futureEvent}}
                    </small>
                  </div>
                </div>
              </div>
              <div class='col-sm-6 mb-3'>
                <div class='card h-100'>
                  <div class='card-body'>
                    <i class='d-flex align-items-center mb-3 material-icons text-info mr-2'>Past Events</i>
                    <small
                      class='d-block'
                      v-for='(pastEvent, index) in pastEvents'
                      :key='index'
                    >
                      {{pastEvent}}
                    </small>
                  </div>
                </div>
              </div>
            </div>
            <div class='row gutters-sm'>
              <div class='col-sm-6 mb-3'>
                <div class='card h-100'>
                  <div class='card-body'>
                    <i class='d-flex align-items-center mb-3 material-icons text-info mr-2'>Your posts</i>
                    <small
                      class='d-block clickable'
                      v-for='(userPost, index) in userPosts'
                      :key='index'
                      @click='goToPost(userPost)'
                    >
                      {{userPost.title}}
                    </small>
                  </div>
                </div>
              </div>
              <div class='col-sm-6 mb-3'>
                <div class='card h-100'>
                  <div class='card-body'>
                    <i class='d-flex align-items-center mb-3 material-icons text-info mr-2'>Posts you've commented on</i>
                    <small
                      class='d-block clickable'
                      v-for='(userCommentedOnPost, index) in userCommentedOnPosts'
                      :key='index'
                      @click='goToPost(userCommentedOnPost.post)'
                    >
                      {{userCommentedOnPost.post.title}}
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <script>
  import {get} from '../../http-common'
  import store from '../../store'
  
  export default {
    data () {
      return {
        user: '',
        futureEvents: [],
        pastEvents: [],
        userPosts: {},
        userCommentedOnPosts: {}
      }
    },
  
    async created () {
      this.user = store.state.user
  
      let userEvents = await get(`user-events`)
  
      this.futureEvents = userEvents.data.future_events.filter((event, index, self) => {
        return self.indexOf(event) === index
      })
  
      this.pastEvents = userEvents.data.past_events.filter((event, index, self) => {
        return self.indexOf(event) === index
      })
  
      let userCommentedOnPostsResponse = await get('user-comments')
  
      let seen = []
      this.userCommentedOnPosts = userCommentedOnPostsResponse.data.filter(comment => {
        return seen.includes(comment.post.id) ? false : seen.push(comment.post.id)
      })
  
      let userPostsResponse = await get('user-posts')
      this.userPosts = userPostsResponse.data.data
    },
  
    methods: {
      goToPost (post) {
        this.$store.dispatch('selectPost', post)
        this.$router.push('/Post')
      },
      resetPassword () {
        alert(`A password reset link has been sent to ${this.user.email}`)
      },
      resetEmail () {
        alert(`An email reset link has been sent to ${this.user.email}`)
      }
    }
  }
  </script>
  
  <style scoped>
  body{
    margin-top:20px;
    color: #1a202c;
    text-align: left;
    background-color: #e2e8f0;
  }
  .main-body {
    padding: 15px;
  }
  .card {
    box-shadow: 0 1px 3px 0 rgba(0,0,0,.1), 0 1px 2px 0 rgba(0,0,0,.06);
  }
  
  .card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 0 solid rgba(0,0,0,.125);
    border-radius: .25rem;
  }
  
  .card-body {
    flex: 1 1 auto;
    min-height: 1px;
    padding: 1rem;
  }
  
  .gutters-sm {
    margin-right: -8px;
    margin-left: -8px;
  }
  
  .gutters-sm>.col, .gutters-sm>[class*=col-] {
    padding-right: 8px;
    padding-left: 8px;
  }
  .mb-3, .my-3 {
    margin-bottom: 1rem!important;
  }
  
  .bg-gray-300 {
    background-color: #e2e8f0;
  }
  
  .h-100 {
    height: 100%!important;
  }
  
  .shadow-none {
    box-shadow: none!important;
  }
  
  .clickable {
    cursor: pointer;
  }
  
  .clickable:hover {
    color: aqua;
  }
  </style>
  