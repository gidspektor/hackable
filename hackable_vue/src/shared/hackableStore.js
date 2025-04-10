import { defineStore } from 'pinia'
import { ref } from 'vue'
import HackableService from './hackableService.js'
import { API_URL } from '@/shared/constants.js'
import hackableService from './hackableService.js'

export const useHackableStore = defineStore('hackable', () => {
	const user = ref({})
	const userImageUrl = ref(null)
	const jwt = ref('')

	return {
		jwt,
		user,
		userImageUrl,
		login,
		createAccount,
		getUserImage,
		uploadUserImage,
		getUser,
		refreshToken,
		getJwtToken,
		removeJwtToken,
		changePassword,
		logout,
	}

	async function login(username, password) {
		const response = await HackableService.login({'username': username, 'password': password})

		if (response.status === 200) {
			user.value = response.data
			jwt.value = user.value.jwt

			// Broken access control
			document.cookie = `is_admin=${user.value.is_admin}; path=/;`
		}

		return response
	}

	async function getUser() {
		const response = await HackableService.getUserInfo()
		user.value = response?.data
	}

	async function createAccount(username, password, passwordRepeat) {
		const response = await HackableService.createAccount(
				{
					'username': username,
					'password': password, 'passwordRepeat': passwordRepeat
				}
		)

		if (response.status === 200) {
			user.value = response?.data
			jwt.value = user.value.jwt
		}

		return response
	}

	async function getUserImage() {
		const response = await HackableService.getUserImageUrl()
		userImageUrl.value = response?.data?.image_path ? API_URL + '/' + response?.data?.image_path : null

		return response
	}

	async function uploadUserImage(image) {
		const response = await HackableService.uploadUserImage({image})
		userImageUrl.value = response?.data?.image_path ? API_URL + '/' + response?.data?.image_path : null
		return response
	}

	async function refreshToken() {
		const response = await HackableService.refreshToken()
		jwt.value = response?.data?.jwt
		return response
	}

	function getJwtToken() {
		return jwt.value
	}

	function removeJwtToken() {
		jwt.value = ''
	}

	async function logout() {
		user.value = {}
		jwt.value = ''
		document.cookie = 'is_admin=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
		await hackableService.logout()
	}

	async function changePassword(oldPassword, newPassword, passwordMatch) {
		const response = await HackableService.changePassword({
			'old_password': oldPassword,
			'new_password': newPassword,
			'new_password_match': passwordMatch,
		})

		return response
	}
},
	{
    	persist: true,
  	}
)
