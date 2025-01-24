import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'
import HackableService from './hackableService.js'

export const useHackableStore = defineStore('hackable', () => {
	const state = reactive({
		user: null,
		userImageUrl: null,
	})

	return {
		user: computed(() => state.user),
		userImageUrl: computed(() => state.userImageUrl),
		login,
		createAccount,
		getUserImage,
		uploadUserImage,
	}

	async function login(email, password) {
		let user = {
			id: 1,
			first_name: 'peter',
			last_name: 'parker',
			email: 'pparker@dailybuggle.com',
		}

		// this.user = await HackableService.login({'email': email, 'password': password})
		// state.jwt = 'jwt'

		state.user = user
	}

	async function createAccount(firstName, lastName, email, password, passwordRepeat) {
		let user = {
			id: 1,
			first_name: 'peter',
			last_name: 'parker',
			email: 'pparker@dailybuggle.com',
		}

		// response = await HackableService.createAccount(
		// 		{
		// 			'firstName': firstName, 'lastNmae': lastName, 'email': email,
		// 			'password': password, 'passwordRepeat': passwordRepeat
		// 		}
		// )

		// if (response.status === 201) {
		// 	this.user = response.data
		// }
		// state.jwt = 'jwt'
		// return response

		state.user = user
	}

	// async function refreshToken() {

	// }

	// async function refreshUserData() {

	// }

	async function getUserImage() {
		// state.userImageUrl = HackableService.getUserImageUrl()
		state.userImageUrl = 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50'
	}

	async function uploadUserImage(image) {
		// response = await HackableService.uploadUserImage(image)
		// await getUserImage()
		// return response
	}
})
