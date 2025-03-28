<template>
	<div class="modal-overlay">
		<div class="">
			<div v-if="isLoading" class="modal-body">
				<div class="loading-text">Loading...</div>
			</div>
			<div v-else>
				<div class="modal-header">
					<h5 class="modal-title">Login or Sign up</h5>
				</div>
				<div class="modal-content">
					<template v-if="!signUpUser">
						<div>
							<div class="form-group">
								<input
									v-model="username"
									type="username"
									class="input-field"
									placeholder="username"
								/>
								<div v-if="usernameError" class="error-message">{{ usernameError }}</div>
								<input
									v-model="password"
									type="password"
									class="input-field"
									placeholder="Password"
								/>
								<div class="links">
									<a href="#" class="link" @click="signUp">Sign up</a>
								</div>
								<div v-if="error" class="error-message">{{ error }}</div>
							</div>
							<button @click="login" class="action-button">Login</button>
						</div>
					</template>
					<template v-else>
						<div class="form-group">
							<input v-model="username" class="input-field" placeholder="username" type="username" />
							<div v-if="usernameError" class="error-message">{{ usernameError }}</div>
							<input
								v-model="password"
								class="input-field"
								placeholder="Create Password"
								type="password"
							/>
							<div v-if="passwordLengthError" class="error-message">{{ passwordLengthError }}</div>
							<input
								v-model="passwordRepeat"
								class="input-field"
								placeholder="Repeat Password"
								type="password"
							/>
							<div v-if="passwordNotMatchError" class="error-message">
								{{ passwordNotMatchError }}
							</div>
							<div class="links">
								<a href="#" class="link" @click="signIn">Sign in</a>
							</div>
							<button @click="createAccount" class="action-button">Create Account</button>
						</div>
					</template>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useHackableStore } from '@/shared/hackableStore'

const hackableStore = useHackableStore()

const formValid = ref<boolean>(false)
const signUpUser = ref<boolean>(false)
const isLoading = ref<boolean>(false)
const username = ref<string>('')
const password = ref<string>('')
const passwordRepeat = ref<string>('')
const error = ref<string>('')
const usernameError = ref<string>('')
const nameError = ref<string>('')
const passwordLengthError = ref<string>('')
const passwordNotMatchError = ref<string>('')

const emit = defineEmits(['close'])

const closeModal = () => {
	emit('close')
}
const login = async () => {
	let response = await hackableStore.login(username.value, password.value)
	console.log(response)
	if (response.status !== 200) {
		error.value = response.error
	} else {
		emit('close')
	}
}
const signUp = () => {
	signUpUser.value = true
}
const signIn = () => {
	signUpUser.value = false
}
const createAccount = async () => {
	validateForm()

	if (formValid.value) {
		let response = await hackableStore.createAccount(
			username.value,
			password.value,
			passwordRepeat.value,
		)

		if (response.error) {
			error.value = response.error
		} else {
			emit('close')
		}
	}
}

const validateForm = () => {
	formValid.value = false

	passwordLengthError.value = ''
	passwordNotMatchError.value = ''

	if (password.value.length < 8) {
		passwordLengthError.value = 'Password must be a minimum of 8 characters'
	}

	if (password.value !== passwordRepeat.value) {
		passwordNotMatchError.value = "Passwords don't match"
	}

	if (!passwordNotMatchError.value && !passwordLengthError.value && !nameError.value) {
		formValid.value = true
	}
}

const handleKeyPress = (event: KeyboardEvent) => {
	if (event.key === 'Enter') {
		if (signUpUser.value) {
			createAccount()
		} else {
			login()
		}
	}
}

document.addEventListener('keydown', handleKeyPress)

</script>

<style scoped>
.modal-header {
	padding: 1rem;
	border-bottom: 1px solid #ddd;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.modal-title {
	font-size: 1.2rem;
	font-weight: bold;
	text-align: center;
	margin: 0 auto;
	color: green;
}

.back-arrow {
	cursor: pointer;
	height: 20px;
	margin-right: auto;
}

.modal-content {
	padding: 1rem;
}

.form-group {
	margin-bottom: 1rem;
}

.input-field {
	width: 100%;
	padding: 0.5rem;
	margin-bottom: 0.5rem;
	border: 1px solid #ddd;
	border-radius: 5px;
	font-size: 1rem;
}

.error-message {
	color: red;
	font-size: 0.9rem;
	margin-bottom: 0.5rem;
}

.links {
	display: flex;
	justify-content: space-between;
	margin-bottom: 1rem;
}

.link {
	font-size: 0.9rem;
	color: #007bff;
	cursor: pointer;
}

.link:hover {
	text-decoration: underline;
}

.action-button {
	width: 100%;
	padding: 0.75rem;
	font-size: 1rem;
	color: white;
	background-color: #28a745;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	text-align: center;
}

.action-button:hover {
	background-color: #218838;
}

.username-button {
	width: 100%;
	padding: 0.75rem;
	margin-top: 0.5rem;
	border: 1px solid #ddd;
	border-radius: 5px;
	display: flex;
	align-items: center;
	cursor: pointer;
	background-color: white;
}

.username-button:hover {
	background-color: #f7f7f7;
}

.button-icon {
	height: 20px;
	margin-right: 1rem;
}
</style>
