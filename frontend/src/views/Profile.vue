<script>
import axios from 'axios'

export default {
  data() {
    return {
      message:'',
      username: '',
      userId: '',
      errorMessage: ''
    };
  },
  async mounted() {
    await this.profile()
  },
  methods: {
    async profile() {
      this.errorMessage = ''
      try {
        const response = await axios.get('/api/profile')

        this.message = response.data.message
        this.username = response.data.username
        this.userId = response.data.user_id
      } catch (error) {
        console.error('Error connecting: ', error)
        if (error.response?.status === 401) {
          this.errorMessage = 'Please login'
        } else if (error.response?.status === 422) {
          this.errorMessage = 'Validation error'
        } else {
          this.errorMessage = error.response?.data?.message || 'Error loading profile'
        }
        //this.$router.push('/login')
      }
    }
  }
};
</script>

<template>
  <div class="profile">
    <h1>Welcome to the Recipe Book!</h1>
    <p>This is the profile page.</p>
  </div>
  <div>
    <h1 v-if="username">Hi, {{ username }}!</h1>
    <h2 v-if="message">{{ message }}</h2>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>

</template>

<style>

</style>