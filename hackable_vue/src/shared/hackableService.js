import api from '@/shared/api.js'
import { BASE_ROUTE } from './constants.js'

export default class HackableService {
	async login(params) {
		return await api.POST(`${BASE_ROUTE}/login/`, params, true)
	}

	async createAccount(params) {
		return await api.POST(`${BASE_ROUTE}/user/`, params)
	}

	async getUserImageUrl() {
		return await api.GET(`${BASE_ROUTE}/getUserImageUrl/`)
	}

	async uploadUserImage(params) {
		return await api.POST(`${BASE_ROUTE}/uploadUserImage/`, params)
	}

	async getUserInfo() {
		return await api.GET(`${BASE_ROUTE}/user/`)
	}

	async refreshToken() {
		return await api.POST(`${BASE_ROUTE}/refresh/`)
	}
}
