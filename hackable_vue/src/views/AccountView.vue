<template>
	<div class="image">
		<form :class="userImageUrl ? 'image-uploaded' : 'image-not-uploaded'" @click="() => $refs.media.click()">
			<img
				v-if="userImageUrl"
				:src="userImageUrl"
				width="150"
			/>
			<input
				type="file"
				id="media"
				accept="image/*"
				@change="(event) => handelFileUpload(event)"
				ref="media"
			/>
			<p v-if="!userImageUrl">Upload a user profile image</p>
		</form>
	</div>
	<div class="section">
		<h6>Username</h6>
		<div class="col-sm-9 text-secondary">
			{{ user.username }}
		</div>
	</div>

	<div class="section">
		<h6 class="mb-0">Admin user</h6>
		<div class="col-4 text-secondary">
			{{ user.is_admin }}
		</div>
	</div>

	<div class="section">
		<h6 class="mb-0">Update Password?</h6>
		<div class="col-4 text-secondary">
			<a href="#/Account" @click="openPasswordModal">Click to update password</a>
		</div>
	</div>

	<div class="section router-links">
		<div class="router-section">
			<i>
				Your Articles
			</i>
			<div>
				<router-link
					v-for="article in userArticles"
					:key="article.id"
					:to="{ name: 'article', params: { id: article.id } }"
					class="article-item"
				>
					{{ article.title }}
				</router-link>
			</div>
		</div>

		<div class="router-section">
			<i>
				Your comments
			</i>
			<div>
				<router-link
					v-for="userComment in userComments"
					:key="userComment.id"
					:to="{ name: 'article', params: { id: userComment.article_id } }"
					class="post-item"
				>
					{{ userComment.comment }}
				</router-link>
			</div>
		</div>
	</div>
	<div v-if="isAdmin" class="section">
		<div class="form-group">
			<input
				v-model="articleKeyword"
				type="articleKeyword"
				class="input-field"
				placeholder="articleKeyword"
			/>
			<button @click="searchArticles" class="action-button">Search articles by title</button>
			<div>
				<router-link
					v-for="article in searchedArticles"
					:key="article.id"
					:to="{ name: 'article', params: { id: article.id } }"
					class="article-item"
				>
					{{ article.title }}
				</router-link>
			</div>
   		</div>
	</div>
	<div>
		{{ error }}
	</div>
	<div class="overlay" v-show="showModal">
		<transition name="fade">
			<UpdatePasswordModal id="modal" class="myModal" v-show="showModal" @close="showModal = false" />
		</transition>
	</div>
</template>

<script setup>
	import { onMounted, computed, ref } from 'vue'

	import { useArticlesStore } from '@articles/shared/articlesStore'
	import { useHackableStore } from '@/shared/hackableStore'

	import UpdatePasswordModal from '@/components/modals/UpdatePasswordModal.vue'

	const articlesStore = useArticlesStore()
	const hackableStore = useHackableStore()

	const user = computed(() => hackableStore.user);
	const userArticles = computed(() => articlesStore.userArticles)
	const userComments = computed(() => articlesStore.userComments)
	const userImageUrl = computed(() => hackableStore.userImageUrl)
	const showModal = ref(false)
	const searchedArticles =  computed(() => articlesStore.searchedArticles)
	const articleKeyword = ref('')
	const isAdmin = ref(false)
	const error = ref('')

	const openPasswordModal = () => {
		showModal.value = true
	}

	const getUserArticles = async () => {
		try {
			await articlesStore.getUserArticles()
		} catch (error) {
			console.error('Failed to fetch user articles:', error)
		}
	};

	const getUserComments = async () => {
		try {
			await articlesStore.getUserComments()
		} catch (error) {
			error.value = 'Failed to fetch user comments: ' + error.message
		}
	};

	const getUserImage = async () => {
		try {
			await hackableStore.getUserImage()
		} catch (error) {
			error.value = 'Failed to fetch user image: ' + error.message
		}
	};

	const handelFileUpload = async (event) => {
		const target = event.target
		const file = target && target.files && target.files[0]
		if (!file) {
			return
		}

		try {
			await hackableStore.uploadUserImage(file)
		} catch (error) {
			error.value = 'Failed to upload image: ' + error.message
		}
	};

	const searchArticles = async () => {
        try {
			await articlesStore.searchArticles(articleKeyword.value)
		} catch (error) {
			error.value = 'Failed to search articles: ' + error.message
		}
    }

    const handleKeyPress = (event) => {
		if (event.key === 'Enter') {
			search(username.value)
		}
	}

	document.addEventListener('keydown', handleKeyPress)

	// Broken access control
	const getIsAdmin = () => {
		return document.cookie
		.split('; ')
		.find((row) => row.startsWith('is_admin='))
		?.split("=")[1] == 'true'
	}

	onMounted(async () => {
		await getUserComments()
		await getUserArticles()
		await getUserImage()
		isAdmin.value = await getIsAdmin()
	});
</script>

<style scoped>
.overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
	background-color: rgba(128, 128, 128, 0.5);
}

.myModal {
	z-index: 1000;
	position: fixed;
	top: 40%;
	left: 50%;
	width: 30em;
	height: 18em;
	margin-top: -9em;
	margin-left: -15em;
}

.section {
	border-bottom: 1px solid white;
	margin-bottom: 1rem;
}

.router-links {
	display: flex;
	justify-content: space-between;
}

.router-section {
	width: 48%;
}

.article-item,
.post-item {
	display: block;
	margin-bottom: 0.5rem;
}

.image {
	margin-bottom: 2rem;
}

img {
	border-radius: 20px;
	height: 100px;
}

.image-not-uploaded {
  width: 500px !important;
  height: 100%;
  border-radius: 5px;
  border: 1.5px dashed #a0a0a0;
  cursor: pointer;
}

.image-uploaded {
	width: 150px;
	height: 100%;
	border-radius: 5px;
	border: none;
	cursor: pointer;
}

form input {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  outline: none;
  opacity: 0;
}

form p {
	margin: 0;
	padding-bottom: 1rem;
	text-align: center;
	font-size: 1.5rem;
	color: #a0a0a0;
}
</style>
