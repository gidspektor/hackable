import Axios from 'axios'
import { API_URL } from './constants.js'

const baseURL = API_URL

export default {
	async SIGN_IN(authUrl) {
		return Axios.get(authUrl)
	},
	async SIGN_OUT(authUrl) {
		return Axios.get(authUrl, {
			headers: getHeaders(),
		})
	},

	async GET(route, params, anonymous = false) {
		const _params = params && Object.keys(params)?.length ? cleanParams(params) : ''
		const url = `${baseURL}/${route}${_params}`

		const headers = {
			...(anonymous
				? {
						'Content-Type': 'application/json',
					}
				: getHeaders()),
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
				: getHeaders()),
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
				: getHeaders(isFormData)),
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
				: getHeaders(isFormData)),
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
				: getHeaders()),
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

function getHeaders(isFormData = false) {
	const sessionVars = session.getSession()
	if (!sessionVars.jwt || !sessionVars.sessionid) {
		// Prevent requests if there isn't even session data
		const signInError = new Error('Need to sign in first')
		signInError.sessionError = true
		signInError.skipUserMessage = true
		useRouter().push({ name: 'sign-in' })
		throw signInError
	}

	const headers = {
		...sessionVars,
	}

	if (!isFormData) {
		headers['Content-Type'] = 'application/json'
	}

	return headers
}
