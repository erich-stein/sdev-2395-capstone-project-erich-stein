<script>
import axios from '../axios/axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      message: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      this.errorMessage = ''
      this.message = ''

      if (!this.username || !this.password) {
        this.errorMessage = 'Please enter both username and password'
        return
      }

      this.loading = true

      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password,
        })
        if (response.data.token) {
          localStorage.setItem('token', response.data.token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
          if (response.data.user) {
            console.log(response.data.user)
            localStorage.setItem('user', JSON.stringify(response.data.user))
          }
          if (response.status === 200) {
            this.message = response?.data?.message
            console.log(this.message)
            setTimeout(() => {
              this.$router.push('/')
            }, 2000)
          }
          
        } else {
          this.errorMessage = 'Login failed - no token'
        }
      } catch (error) {
        if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Login failed'
          console.error(this.errorMessage)
        } else if (error.request) {
          // request but no response
          this.errorMessage = 'Cannot connect to server'
          console.error(this.errorMessage)
        } else {
          // something else
          this.errorMessage = 'Unexpected error'
          console.error(error.response.data.msg)
        }
      } finally {
        this.loading = false
      }
    },

    routeToRegister() {
      this.$router.push('/create-account')
    }
  }
};
</script>

<template>
  <div class="login">
    <h1>Welcome to the Recipe Book!</h1>
    <p>This is the login page.</p>

    <br/>

    <form @submit.prevent="login">
      <hr/>
      <div>
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          required
          :disabled="loading"
        />
      </div>
      <div>
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          :disabled="loading"
        />
      </div>
      <hr/>
      <button type="submit" :disabled="loading">
        <span v-if="loading">Logging in...</span>
        <span v-else>Login</span>
      </button>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <div class="register-link">
      <button type="button" @click="routeToRegister" :disabled="loading">
        Create account here!
      </button>
    </div>
  </div>

</template>

<style>

</style>