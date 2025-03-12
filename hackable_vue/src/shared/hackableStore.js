import { defineStore } from 'pinia'
import { reactive, computed } from 'vue'
import HackableService from './hackableService.js'
import { jwtDecode } from 'jwt-decode'
import { API_URL } from '@/shared/constants.js'

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

	async function login(username, password) {
		const response = await HackableService.login({'username': username, 'password': password})

		if (response.status === 200) {
			state.user = response.data
			localStorage.setItem('t', state.user.jwt)

			// Broken access control
			document.cookie = `is_admin=${state.user.is_admin}; path=/;`
		}

		return response
	}

	async function getUser() {
		const response = await HackableService.getUserInfo()
		state.user = response.data
	}

	async function createAccount(username, password, passwordRepeat) {
		const response = await HackableService.createAccount(
				{
					'username': username,
					'password': password, 'passwordRepeat': passwordRepeat
				}
		)

		if (response.status === 200) {
			state.user = response.data
			localStorage.setItem('t', state.user.jwt)

			// Broken access control
			document.cookie = `is_admin=${state.user.is_admin}; path=/;`
		}

		return response
	}

	async function getUserImage() {
		const response = HackableService.getUserImageUrl()
		state.userImageUrl = API_URL + response.data
	}

	async function uploadUserImage(image) {
		const response = await HackableService.uploadUserImage(image)
		state.userImageUrl = API_URL + response.data
		return response
	}

	async function refreshToken() {
		const response = await HackableService.refreshToken()
		localStorage.setItem('t', response.data.jwt)
		return response
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
