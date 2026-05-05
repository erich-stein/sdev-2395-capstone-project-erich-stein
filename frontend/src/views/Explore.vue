<script>
import axios from '../axios/axios'
import RecipeCard from '../components/RecipeCard.vue'
import SearchBar from '../components/SearchBar.vue'
import CategoryFilter from '../components/CategoryFilter.vue'

export default {
  components: { RecipeCard, SearchBar, CategoryFilter },
  data() {
    return {
      recipes: [],
      loading: false,
      errorMessage: '',
      searchTerm: '',
      searchType: 'title',
      selectedCategories: []
    }
  },
  async mounted() {
    this.getRecipes()
  },
  methods: {
    async getRecipes() {
      this.loading = true
      this.errorMessage = ''

      let url = '/api/explore'
      const params = []

      if (this.searchTerm) {
        params.push(`term=${encodeURIComponent(this.searchTerm)}`)
        params.push(`type=${this.searchType}`)
      }
      
      if (this.selectedCategories.length > 0) {
        this.selectedCategories.forEach(cat => {
          params.push(`categories=${cat}`)
        })
      }

      if (params.length > 0) {
        url = `/api/explore/search?${params.join('&')}`
      } else {
        url = '/api/explore'
      }

      try {
        const response = await axios.get(url)
        this.recipes = response.data
        //console.log(`Retrieved ${this.recipes.length} recipes`)

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
    async handleSearch(term, type) {
      //console.log('searchTerm: ', term, 'Type: ', typeof term)
      //console.log('searchType: ', type, 'Type: ', typeof type)
      if (!term || term.trim() === '') {
        this.searchTerm = ''
        await this.getRecipes()
        return
      }

      this.searchTerm = term.trim()
      this.searchType = type
      await this.getRecipes()
    },
    async handleCatFilter(categories) {
      this.selectedCategories = categories
      await this.getRecipes()
    },
    routeToCreateRecipe() {
      this.$router.push('/create-recipe')
    }
  },
}

</script>

<template>
  <div class="filter-group">
    <CategoryFilter @filter-change="handleCatFilter" />
  </div>

  <div class="search-bar">
    <SearchBar @search="handleSearch" />
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
.recipes-grid {
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  grid-template-columns: repeat(3, 1fr);
  gap: 8px
}


</style>