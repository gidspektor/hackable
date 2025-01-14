import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'

export const useHackableStore = defineStore('hackable', () => {
	const state = reactive({
		user: null,
		jwt: null,
	})

	return {
		user: computed(() => state.user),
		login,
		createAccount,
		clearUser,
	}

	async function login(email, password) {
		let user = {
			id: 1,
			name: 'user1'
		}

		// this.user = await HackableService.login({'email': email, 'password': password})
		// state.jwt = 'jwt'

		state.user = user
	}

	async function createAccount(name, email, password, passwordRepeat) {
		let user = {
			id: 1,
			name: 'user1'
		}

		// response = await HackableService.createAccount({'name': name, 'email': email, 'password': password, 'passwordRepeat': passwordRepeat})

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

	function clearUser() {
		state.user = null
	}
})
