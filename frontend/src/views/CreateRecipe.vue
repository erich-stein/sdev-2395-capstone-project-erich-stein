<script>
import axios from '../axios/axios'
import RecipeForm from '../components/RecipeForm.vue'

export default {
  components: { RecipeForm },
  data() {
    return {
      message: '',
      errorMessage: ''
    }
  },
  methods: {
    async createRecipe(recipeData) {
      this.message = ''
      this.errorMessage = ''

      try {
        const response = await axios.post('/api/create-recipe', recipeData)

        if (response.status === 201) {
          this.message = 'Recipe created successfully'
          // maybe route to created recipe instead
          setTimeout(() => {
            this.$router.push('/')
          }, 2000)
        }

      } catch (error) {
        console.error('Error creating recipe: ', error)

        if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Recipe creation failed'
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
      this.$router.push('/')
    }
  }
}

</script>

<template>
  <div>
    <h1>Create Recipe</h1>
    <RecipeForm
      @submit="createRecipe"
      @cancel="cancel"
    />
  </div>

  <div v-if="message" class="message">{{ message }}</div>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

</template>

<style scoped>

</style>