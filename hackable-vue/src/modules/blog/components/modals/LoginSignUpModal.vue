<template>
    <div class="modal-overlay">
      <div class="modal-container">
        <div v-if="isLoading" class="modal-body">
          <div class="loading-text">Loading...</div>
        </div>
        <div v-else>
          <div class="modal-header">
            <div @click="closeModal" class="close-button">&times;</div>
            <h5 class="modal-title">Log in or Sign up</h5>
          </div>
          <div class="modal-content">
            <template v-if="!signUpUser">
              <div>
                <div class="form-group">
                  <input
                    v-model="email"
                    type="email"
                    class="input-field"
                    placeholder="Email Address"
                  />
                  <div v-if="emailError" class="error-message">{{ emailError }}</div>
                  <input
                    v-model="password"
                    type="password"
                    class="input-field"
                    placeholder="Password"
                  />
                  <div class="links">
                    <a href="#" class="link" @click.prevent="resetPassword">Forgot password?</a>
                    <span>|</span>
                    <a href="#" class="link" @click="signUp">Sign up?</a>
                  </div>
                  <div v-if="error" class="error-message">{{ error }}</div>
                </div>
                <button @click="login" class="action-button">Continue</button>
              </div>
            </template>
            <template v-else>
              <div class="form-group">
                <input v-model="name" class="input-field" placeholder="Full Name" type="text" />
                <div v-if="nameError" class="error-message">{{ nameError }}</div>
                <input v-model="email" class="input-field" placeholder="Email Address" type="email" />
                <div v-if="emailError" class="error-message">{{ emailError }}</div>
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
                <button @click="createAccount" class="action-button">Create Account</button>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useHackableStore } from '@/shared/hackableStore';

const hackableStore = useHackableStore();

const signUpUser = ref(false);
const isLoading = ref(false);
const email = ref('');
const password = ref('');
const name = ref('');
const passwordRepeat = ref('');
const error = ref('');
const emailError = ref('');
const nameError = ref('');
const passwordLengthError = ref('');
const passwordNotMatchError = ref('');

const emit = defineEmits(['close']);

const closeModal = () => {
  emit('close');
};
const goBack = () => {
  // Implement goBack logic
};
const login = () => {
  hackableStore.login(email.value, password.value);
};
const signUp = () => {
  signUpUser.value = true;
};
const createAccount = () => {
  // Implement createAccount logic
};
const resetPassword = () => {
  // Implement resetPassword logic
};
const loginWithEmail = () => {
  // Implement loginWithEmail logic
};
</script>
  
<style scoped>
.modal-container {
    background: white;
    border-radius: 10px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}
  
.modal-header {
    padding: 1rem;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
  
.close-button {
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
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

.email-button {
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

.email-button:hover {
    background-color: #f7f7f7;
}
  
.button-icon {
    height: 20px;
    margin-right: 1rem;
}
</style>
  