<script>
  import axios from './axios/axios'
  import { RouterLink, RouterView } from 'vue-router';

  export default {
    computed: {
      isLoggedIn() {
        return !!localStorage.getItem('token')
      }
    },
    data() {
      return {message:''};
    },
    async mounted() {
      await this.helloWorld()
    },
    methods: {
      // modify login/logout so options show even without refresh
      // use reactivity already in vue or use pinia
      // pinia is probably easier
      logout() {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.reload()
        this.$router.push('/login')
      },
      async helloWorld() {
        try {
          const response = await axios.get('/api')
          this.message = response.data?.message
        } catch (error) {
          console.error('Error connecting: ', error)
        }
      }
    }
  };
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/profile">Profile</RouterLink>
        <RouterLink to="/explore">Explore Recipes</RouterLink>
        <RouterLink v-if="isLoggedIn" to="/create-recipe">Create Recipe</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/login">Login</RouterLink>
        <RouterLink v-if="!isLoggedIn" to="/create-account">Create Account</RouterLink>
        <button v-if="isLoggedIn" @click="logout">Logout</button>
      </nav>
    </div>
  </header>
  <br/>
  <h1>{{ message }}</h1>
  <br/>

  <RouterView />

</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
