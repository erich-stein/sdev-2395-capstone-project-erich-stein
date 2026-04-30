<script>
import axios from '../axios/axios'
import RecipeForm from '../components/RecipeForm.vue'

export default {
  components: { RecipeForm },
  data() {
    return {
      recipe: null,
      loading: true,
      errorMessage: '',
      message: ''
    }
  },
  async mounted() {
    await this.loadRecipeData()
  },
  methods: {
    async loadRecipeData() {
      this.loading = true
      this.errorMessage = ''

      try {
        const recipeId = this.$route.params.id
        const response = await axios.get(`/api/recipe/${recipeId}`)
        this.recipe = response.data

        console.log('Recipe retrieved')

      } catch(error) {
        console.error('Error getting recipe: ', error)
        this.errorMessage = error.response?.data?.errorMessage || 'Failed to load recipe'
      } finally {
        this.loading = false
      }
    },
    async editRecipe(recipeData) {
      this.message = ''
      this.errorMessage = ''

      try {
        const response = await axios.put(`/api/recipe/${this.recipe.id}`, recipeData)

        if (response.status === 200) {
          this.message = 'Recipe updated successfully'
          setTimeout(() => {
            this.$router.push(`/recipe/${this.recipe.id}`)
          }, 2000)
        }
    
      } catch (error) {
        console.error('Error updating recipe: ', error)

        if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Recipe update failed'
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
      }
    },
    cancel() {
      this.$router.push(`/recipe/${this.recipe.id}`)
    }
  }
}

</script>

<template>
  <div>
    <h1>Edit Recipe</h1>

    <div v-if="loading">
      Loading recipe data...
    </div>

    <div v-else-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>
    
    <div v-else-if="recipe">
      <RecipeForm
        :init-data="recipe"
        :submit-label="'Update Recipe'"
        @submit="editRecipe"
        @cancel="cancel"
      />
    </div>

    <div v-if="message" class="message">{{ message }}</div>
  </div>

</template>

<style scoped>

</style>