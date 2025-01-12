import { defineStore } from 'pinia'

export const useHackableStore = defineStore('hackable', {
	state: () => {
			return {
					user: null,
			}
	},

	actions: {
		async login(email, password) {
			this.user = {
				id: 1,
				name: 'user1'
			}

			// this.user = await HackableService.login({'email': email, 'password': password})
		}
	},
})