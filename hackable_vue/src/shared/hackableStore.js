import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'
import HackableService from './hackableService.js'
import jwtDecode from 'jwt-decode'

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
		inspectToken,
		getUser,
		refreshToken
	}

	async function login(email, password) {
		let user = {
			id: 1,
			first_name: 'peter',
			last_name: 'parker',
			email: 'pparker@dailybuggle.com',
		}

		// state.user = await HackableService.login({'email': email, 'password': password})
		// state.jwt = 'jwt'

		state.user = user
	}

	async function getUser() {
		state.user = await HackableService.getUserInfo()
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

	async function refreshToken() {
		// response = await HackableService.refreshToken()
		// return response
	}

	function inspectToken () {
		let state = ''
	  
		if (localStorage.getItem('t')) {
		  const decoded = jwtDecode(localStorage.getItem('t'))
	  
		  const exp = parseFloat(decoded.exp)
		  let iat = null
	  
		  if (Object.keys(decoded).includes('orig_at')) {
			iat = parseFloat(decoded.orig_iat)
		  } else {
			iat = parseFloat(decoded.iat)
		  }
	  
		  if (exp - (Date.now() / 1000) < 1800 && (Date.now() / 1000) - iat > 86400) {
			state = 'refresh'
		  } else if (exp - (Date.now() / 1000) < 3600 && exp - (Date.now() / 1000) > 0) {
			state = 'active'
		  } else {
			state = 'expired'
		  }
		}
	  
		return state
	}
},
	{
    	persist: true,
  	}
)
