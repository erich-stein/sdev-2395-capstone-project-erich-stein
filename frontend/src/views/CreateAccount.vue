<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      password_confirm: '',
      errorMessage: '',
    }
  },
  methods: {
    async createAccount() {
      this.errorMessage = ''
      
      try {
        const response = await axios.post('/api/create-account', {
          username: this.username,
          password: this.password,
          password_confirm: this.password_confirm,
        })
        localStorage.setItem('token', response.data.token)
        this.$router.push('/')
      } catch (error) {
        this.errorMessage = error.response?.data?.message || 'Registration failed'
      }
    }
  }
};
</script>

<template>
  <div class="createAccount">
    <h1>Welcome to the Recipe Book!</h1>
    <p>This is the account creation page.</p>

    <br/>

    <form @submit.prevent="createAccount">
      <h1>Create Account</h1>
      <hr/>
      <input v-model="username" type="text" placeholder="Username" />
      <br/>
      <input v-model="password" type="password" placeholder="Password" />
      <br/>
      <input v-model="password_confirm" type="password" placeholder="Confirm Password" />
      <hr/>
      <button type="submit">Create Account</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
  </div>

</template>

<style>

</style>