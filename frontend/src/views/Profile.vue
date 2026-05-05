<script>
import axios from '../axios/axios'
import RecipeCard from '../components/RecipeCard.vue'

export default {
  components: { RecipeCard },
  data() {
    return {
      recipes: [],
      loading: false,
      username: '',
      errorMessage: ''
    };
  },
  async mounted() {
    await this.getUserData()
  },
  methods: {
    async getUserData() {
      this.loading = true
      this.errorMessage = ''
      this.message = ''

      try {
        const response = await axios.get('/api/profile')
        this.recipes = response.data.recipes
        this.username = response.data.username

        console.log(`Retrieved ${this.recipes.length} recipes by ${this.username}`)

      } catch (error) {
        console.error('Error retrieving recipes: ', error)

        if (error.response?.status === 401) {
          // missing authorization
          this.errorMessage = 'Please login'
          console.error(this.errorMessage)
        } else if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Failed to load recipes'
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
        this.$router.push('/login')
      } finally {
        this.loading = false
      }
    },
    routeToCreateRecipe() {
      this.$router.push('/create-recipe')
    }
  }
};
</script>

<template>
  <div class="profile-header">
    <h1 v-if="username">Hi, {{ username }}!</h1>
  </div>

  <div v-if="errorMessage" class="error-message">
    <h2>{{ errorMessage }}</h2>
    <button type="button" @click="$forceUpdate()">
      Reload Page
    </button>
    <button type="button" @click="$router.push('/')">
      Back to Home
    </button>
  </div>

  <div v-else-if="recipes.length < 1" class="empty-recipes">
    <p>No recipes found. Create one!</p>
    <button type="button" @click="routeToCreateRecipe">Create A Recipe</button>
  </div>

  <div v-else class="has-recipes">
    <h3>Here are your recipes!</h3>
    <div class="recipes-grid">
      <RecipeCard
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </div>

</template>

<style scoped>
.recipes-grid {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  grid-template-columns: repeat(3, 1fr);
  gap: 8px
}

</style>