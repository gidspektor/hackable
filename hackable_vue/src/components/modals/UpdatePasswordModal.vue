<template>
    <div class="modal-overlay">
		<div class="modal-container">
            <div class="modal-header">
                <div @click="closeModal" class="close-button">&times;</div>
            </div>
            <div class="modal-content">
                <div class="form-group">
                    <input
                        v-model="oldPassword"
                        class="input-field"
                        placeholder="Current password"
                        type="password"
                    />
                    <div v-if="passwordLengthError" class="error-message">{{ passwordLengthError }}</div>
                    <input
                        v-model="newPassword"
                        class="input-field"
                        placeholder="New password"
                        type="password"
                    />
                    <input
                        v-model="passwordRepeat"
                        class="input-field"
                        placeholder="Repeat new password"
                        type="password"
                    />
                    <div v-if="passwordNotMatchError" class="error-message">
                        {{ passwordNotMatchError }}
                    </div>
                    <div v-if="error" class="error-message">{{ error }}</div>
                    <button @click="update" class="action-button">Update</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref } from 'vue'
    import { useHackableStore } from '@/shared/hackableStore'

    const hackableStore = useHackableStore()
    const emit = defineEmits(['close'])

    const passwordLengthError = ref<string>('')
    const passwordNotMatchError = ref<string>('')
    const newPassword = ref<string>('')
    const passwordRepeat = ref<string>('')
    const oldPassword = ref<string>('')
    const error = ref<string>('')

    const closeModal = () => {
		emit('close')
	}

    const update = async () => {
        if (newPassword.value.length < 8) {
            passwordLengthError.value = 'Password must be at least 8 characters long'
        } else if (newPassword.value !== passwordRepeat.value) {
            passwordNotMatchError.value = 'Passwords do not match'
        } else {
            try {
                await hackableStore.changePassword(oldPassword.value, newPassword.value, passwordRepeat.value)
				emit('close')
			} catch (err) {
                error.value = 'Error updating password'
                console.error(err)
            }
        }
    }
</script>

<style scoped>
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

.modal-header {
	padding: 1rem;
	border-bottom: 1px solid #ddd;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.error-message {
	color: red;
	font-size: 0.9rem;
	margin-bottom: 0.5rem;
}

.modal-container {
	background: white;
	border-radius: 10px;
	width: 90%;
	max-width: 500px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.close-button {
	cursor: pointer;
	font-size: 1.5rem;
	font-weight: bold;
	color: #333;
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
</style>
