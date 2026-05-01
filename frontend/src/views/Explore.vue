<script>
import axios from '../axios/axios'
import RecipeCard from '../components/RecipeCard.vue'

export default {
  components: { RecipeCard },
  data() {
    return {
      recipes: [],
      loading: false,
      errorMessage: ''
    }
  },
  async mounted() {
    this.getRecipes()
  },
  methods: {
    async getRecipes() {
      this.loading = true
      this.errorMessage = ''

      try {
        const response = await axios.get('/api/explore')
        this.recipes = response.data
        console.log(`Retrieved ${this.recipes.length} recipes`)

      } catch (error) {
        console.error('Error retrieving recipes: ', error)

        if (error.response) {
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
      } finally {
        this.loading = false
      }
    },
    routeToCreateRecipe() {
      this.$router.push('/create-recipe')
    }
  },
}

</script>

<template>
  <div v-if="errorMessage" class="error-message">
    <h2>{{ errorMessage }}</h2>
    <button type="button" @click="$forceUpdate()">
      Reload Page
    </button>
    <button type="button" @click="$router.push('/')">
      Back to Home
    </button>
  </div>

  <!--check if empty, maybe modiffy after adding search and filtering-->
  <div v-else-if="recipes.length < 1" class="empty-recipes">
    <p>No recipes found. Create one!</p>
    <button type="button" @click="routeToCreateRecipe">Create A Recipe</button>
  </div>

  <div v-else class="recipes-grid">
    <RecipeCard
      v-for="recipe in recipes"
      :key="recipe.id"
      :recipe="recipe"
    />
  </div>

</template>

<style scoped>

</style>