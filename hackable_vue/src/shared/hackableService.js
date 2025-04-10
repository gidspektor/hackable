import api from '@/shared/api.js'
import { BASE_ROUTE } from '@/shared/constants.js'

class HackableService {
	async login(params) {
		return await api.POST(`${BASE_ROUTE}/login/`, params, true)
	}

	async createAccount(params) {
		return await api.POST(`${BASE_ROUTE}/user/`, params, true)
	}

	async getUserImageUrl() {
		return await api.GET(`${BASE_ROUTE}/user/image/`)
	}

	async uploadUserImage(params) {
		return await api.PATCH(`${BASE_ROUTE}/upload/image/`, params)
	}

	async getUserInfo() {
		return await api.GET(`${BASE_ROUTE}/user/`)
	}

	async refreshToken() {
		return await api.POST(`${BASE_ROUTE}/refresh/`, null, true)
	}

	async changePassword(params) {
		return await api.PATCH(`${BASE_ROUTE}/user/password/`, params)
	}

	async logout() {
		return await api.POST(`${BASE_ROUTE}/logout/`)
	}
}

export default new HackableService()
