<script>
  //import Home from './components/Home.vue'
  //import Login from './components/Login.vue'
  //import Profile from './components/Profile.vue'
  //import RecipeCreate from './components/RecipeCreate.vue'
  import axios from 'axios'

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
          this.message = response.data.message
        } catch (error) {
          console.error('Error connecting: ', error)
        }
      }
    }
  };
</script>

<template>
  <div>
    <h1>{{  message  }}</h1>
  </div>
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
