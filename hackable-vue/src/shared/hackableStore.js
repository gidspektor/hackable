import { defineStore } from 'pinia'

export const useHackableStore = defineStore('hackable', {
	state: () => {
			return {
				user: JSON.parse(localStorage.getItem('user')) || null,
			}
	},

	actions: {
		async login(email, password) {
			let user = {
				id: 1,
				name: 'user1'
			}

			// this.user = await HackableService.login({'email': email, 'password': password})

			localStorage.setItem('user', JSON.stringify(user));
		},

		async createAccount(name, email, password, passwordRepeat) {
			let user = {
				id: 1,
				name: 'user1'
			}

			// response = await HackableService.createAccount({'name': name, 'email': email, 'password': password, 'passwordRepeat': passwordRepeat})

			// if (response.status === 201) {
			// 	this.user = response.data
			// }

			// return response

			localStorage.setItem('user', JSON.stringify(user));
		},

		clearUser() {
      this.user = null;
      localStorage.removeItem('user');
    },
	},
})