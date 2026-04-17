<script>
  import axios from 'axios'
  import { RouterLink, RouterView } from 'vue-router';

  export default {
    data() {
      return {message:''};
    },
    async mounted() {
      await this.helloWorld()
    },
    methods: {
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
        <RouterLink to="/profile">Profile</RouterLink>
        <RouterLink to="/explore">Explore Recipes</RouterLink>
        <RouterLink to="/create-recipe">Create Recipe</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/create-account">Create Account</RouterLink>
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
