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
        <RouterLink class="router-link" to="/">
          <span>Home</span>
        </RouterLink>
        <RouterLink class="router-link" v-if="isLoggedIn" to="/profile">
          <span>Profile</span>
        </RouterLink>
        <RouterLink class="router-link" to="/explore">
          <span>Explore Recipes</span>
        </RouterLink>
        <RouterLink class="router-link" v-if="isLoggedIn" to="/create-recipe">
          <span>Create Recipe</span>
        </RouterLink>
        <RouterLink class="router-link" v-if="!isLoggedIn" to="/login">
          <span>Login</span>
        </RouterLink>
        <RouterLink class="router-link" v-if="!isLoggedIn" to="/create-account">
          <span>Create Account</span>
        </RouterLink>
        <button v-if="isLoggedIn" @click="logout">
          <span>Logout</span>
        </button>
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
