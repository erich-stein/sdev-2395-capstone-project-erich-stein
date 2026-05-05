<script>
import axios from '../axios/axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      password_confirm: '',
      loading: false,
      message: '',
      errorMessage: '',
    }
  },
  methods: {
    async createAccount() {
      this.errorMessage = ''
      this.message = ''

      if (this.username.length < 3 || this.password.length < 3) {
        this.errorMessage = 'Username and password must be at least 3 characters'
        return
      }

      if (!this.username || !this.password || !this.password_confirm) {
        this.errorMessage = 'All fields are required'
        return
      }

      if (this.password !== this.password_confirm) {
        this.errorMessage = 'Passwords do not match'
        return
      }

      this.loading = true
      
      try {
        const response = await axios.post('/api/create-account', {
          username: this.username,
          password: this.password
        })

        if (response.status === 201) {
          this.message = response?.data?.message
          console.log(this.message)
          setTimeout(() => {
              this.$router.push('/login')
            }, 2000)
        }
        
      } catch (error) {
        if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Registration failed'
          console.error(this.errorMessage)
        } else if (error.request) {
          // request but no response
          this.errorMessage = 'Cannot connect to server'
          console.error(this.errorMessage)
        } else {
          // something else
          this.errorMessage = 'Unexpected error'
          console.error(error.response?.data?.msg || 'Unknown error')
        }
      } finally {
        this.loading = false
      }
    },

    routeToLogin() {
      this.$router.push('/login')
    }
  }
};
</script>

<template>
  <div class="createAccount">
    <h1>Create Account</h1>

    <form @submit.prevent="createAccount">
      <hr/>
      <div>
        <input
          v-model="username"
          class="input"
          type="text"
          placeholder="Username"
          required
          :disabled="loading"
        />
      </div>
      <div>
        <input
          v-model="password"
          class="input"
          type="password"
          placeholder="Password"
          required
          :disabled="loading"
        />
      </div>
      <div>
        <input
          v-model="password_confirm"
          class="input"
          type="password"
          placeholder="Confirm Password"
          required
          :disabled="loading"
        />
      </div>
      <hr/>
      <button type="submit" :disabled="loading">
        <span v-if="loading">Creating account...</span>
        <span v-else>Create account</span>
      </button>
    </form>

    <p v-if="message" class="success-message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <div class="login-link">
      <p>Already have an account?</p>
      <button type="button" @click="routeToLogin" :disabled="loading">
        <span>Login here!</span>
      </button>
    </div>
  </div>

</template>

<style>

</style>