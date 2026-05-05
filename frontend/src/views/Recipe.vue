<script>
import axios from '../axios/axios'

export default {
  data() {
    return {
      errorMessage: '',
      loading: false,
      recipe: null,
      currentUserId: null,
      showDeleteDialogue: false
    }
  },
  computed: {
    isAuthor() {
      //console.log(this.currentUserId)
      //console.log(this.recipe.user_id)
      return this.currentUserId && this.recipe &&
        this.currentUserId == this.recipe.user_id
    }
  },
  async mounted() {
    const userItem = localStorage.getItem('user')
    if (userItem) {
      try {
        const user = JSON.parse(userItem)
        //console.log(user)
        this.currentUserId = user.id
      } catch (err) {
        console.error('Error parsing user: ', err)
      }
    }

    await this.getRecipe()
  },
  methods: {
    // function to format the date here

    async getRecipe() {
      this.errorMessage = ''
      this.loading = true

      try {
        const recipeId = this.$route.params.id
        const response = await axios.get(`/api/recipe/${recipeId}`)
        this.recipe = response.data

        console.log('Recipe retrieved')

      } catch(error) {
        console.error('Error getting recipe: ', error)

        if (error.response?.status === 404) {
          // recipe does not exist
          this.errorMessage = 'Recipe not found'
          console.error(this.errorMessage)
        } else if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Failed to load recipe'
          console.error(this.errorMessage)
        } else if (error.request) {
          // request but no response
          this.errorMessage = 'Cannot connect to server'
          console.error(this.errorMessage)
        } else {
          // something else
          this.errorMessage = 'Unexpected error'
          console.error(error.response?.data?.msg || 'Unknown error')
        }
      } finally {
        this.loading = false
      }
    },
    editRecipe() {
      this.$router.push(`/recipe/${this.recipe.id}/edit`)
    },
    confirmDelete() {
      this.showDeleteDialogue = true
    },
    async deleteRecipe() {
      try {
        const response = await axios.delete(`/api/recipe/${this.recipe.id}`)

        if (response.status === 200) {
          this.showDeleteDialogue = false
          this.$router.push('/')
          alert('Recipe deleted successfully')
        }
      } catch (error) {
        console.error('Error deleting recipe: ', error)

        alert (error.response?.data?.errorMessage || 'Error deleting recipe')
        this.showDeleteDialogue = false
      }
    },
    routeToHome() {
      this.$router.push('/')
    }
  },
}

</script>

<template>
  <div v-if="errorMessage" class="error-message">
    <h2>{{ errorMessage }}</h2>
    <button type="button" @click="routeToHome">
      Back to Home
    </button>
  </div>

  <!--v-if for image-->

  <div v-else-if="recipe" class="recipe-section">
    <div class="recipe-header">
      <h1>{{ recipe.title }}</h1>

      <div v-if="isAuthor">
        <button type="button" @click="editRecipe">Edit Recipe</button>
        <button type="button" @click="confirmDelete">Delete Recipe</button>
      </div>

      <!--Make it an actual dialogue box later maybe-->
      <div v-if="showDeleteDialogue">
        <h3>Delete Recipe?</h3>
        <p>Are you sure you want to delete "{{ recipe?.title }}"? This cannot be undone.</p>
        <div>
          <button @click="showDeleteDialogue = false">
            <span>Cancel</span>
          </button>
          <button @click="deleteRecipe">
            <span>Delete</span>
          </button>
        </div>
      </div>
    </div>

    <div class="recipe-meta">
      <span class="author">By: {{ recipe.creator }}</span>
      <br/>
      <span class="date-created">Published: {{ recipe.timestamp }}</span> <!--need to format it-->
      <br/>
      <span v-if="recipe.updated" class="date-updated">Last Updated: {{ recipe.updated }}</span> <!--need to format it-->
    </div>

    <div class="recipe-meta-info-section">
      <div v-if="recipe.categories?.length" class="categories-group">
        <strong>Categories: </strong>
        <span v-for="cat in recipe.categories" :key="cat" class="category">
          {{ cat }}, 
        </span>
      </div>

      <div v-if="recipe.tags?.length" class="tags-group">
        <strong>Tags: </strong>
        <span v-for="tag in recipe.tags" :key="tag" class="tag">
          {{ tag }}, 
        </span>
      </div>

      <div class="short-desc">
        <p>{{ recipe.short_desc }}</p>
      </div>
    </div>

    <div v-if="recipe.long_desc" class="recipe-desc-section">
      <h2>About This Recipe</h2>
      <p>{{ recipe.long_desc }}</p>
    </div>

    <div class="recipe-ingredients-section">
      <h2>Ingredients</h2>
      <ul class="ingredients-list">
        <li v-for="ingr in recipe.ingredients" :key="ingr">
          {{ ingr }}
        </li>
      </ul>
    </div>

    <div class="recipe-instructions-section">
      <h2>Instructions</h2>
      <ol class="instructions-list">
        <li v-for="instr in recipe.instructions" :key="instr">
          {{ instr }}
        </li>
      </ol>
    </div>
  </div>

</template>

<style scoped>

</style>