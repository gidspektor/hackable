import Axios from 'axios'
import { API_URL } from './constants.js'
import router from '@/router/index.js'

const baseURL = API_URL

export default {
	async GET(route, params, anonymous = false) {
		const _params = params && Object.keys(params)?.length ? cleanParams(params) : ''
		const url = `${baseURL}/${route}${_params}`

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getAuthHeaders()),
		}

		return Axios.get(url, { headers }).catch(handleUnauthorized)
	},

	async POST(route, params, anonymous = false) {
		const url = `${baseURL}/${route}`

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getAuthHeaders(false, true)),
		}
		return Axios.post(url, params, { headers }).catch(handleUnauthorized)
	},

	async PUT(route, params, anonymous = false) {
		const url = `${baseURL}/${route}`

		const [formData, isFormData] = prepareFormData(params)

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getAuthHeaders(isFormData)),
		}

		return Axios.put(url, isFormData ? formData : JSON.stringify(params), { headers }).catch(
			handleUnauthorized,
		)
	},

	async PATCH(route, params, anonymous = false) {
		const url = `${baseURL}/${route}`

		const [formData, isFormData] = prepareFormData(params)

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getAuthHeaders(isFormData)),
		}
		return Axios.patch(url, isFormData ? formData : JSON.stringify(params), { headers }).catch(
			handleUnauthorized,
		)
	},

	async DELETE(route, params, anonymous = false) {
		const _params = params && Object.keys(params)?.length ? cleanParams(params) : ''
		const url = `${baseURL}/${route}${_params}`

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getAuthHeaders()),
		}

		return Axios.delete(url, { headers }).catch(handleUnauthorized)
	},
}

/**
 * Remove any `null` and `undefined` params for the query
 */
function cleanParams(params) {
	const cleanedParams = Object.keys(params).reduce((agg, key) => {
		if (params[key] !== null && params[key] !== undefined) agg[key] = params[key]
		return agg
	}, {})

	return `?${new URLSearchParams(cleanedParams).toString()}`
}

function getAuthHeaders(isFormData = false) {
	const jwt = localStorage.getItem('t')

	if (!jwt) {
		// Prevent requests if there isn't even session data
		const signInError = new Error('Need to sign in first')
		signInError.sessionError = true
		signInError.skipUserMessage = true
		router.push({ name: 'login' })
		throw signInError
	}

	const headers = {
		Authorization: `Bearer ${jwt}`,
	}

	if (!isFormData) {
		headers['Content-Type'] = 'application/json'
	}

	return headers
}

async function handleUnauthorized(error) {
	if (localStorage.getItem('t') && error.response?.status === 401) {
        localStorage.removeItem('t')

        try {
            const response = await hackableStore.refreshToken()
            if (!response) throw new Error("Token refresh failed")

            const config = error.config
            config.headers['Authorization'] = `Bearer ${localStorage.getItem('t')}`

            return Axios.request(config)
        } catch (error) {
            console.log(error);
            router.push({ name: 'login' })
        }
    }

	return Promise.reject(error)
}
