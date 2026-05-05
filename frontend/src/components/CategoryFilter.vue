<script>
import { CategoriesList } from '../assets/categories'

export default {
  data() {
    return {
      categories: CategoriesList,
      selectedCategories: []
    }
  },
  methods: {
    updateFilter() {
      this.$emit('filter-change', this.selectedCategories)
    }
  }
}

</script>

<template>
  <div class="category-filter">
    <h2>Filter by Category</h2>
    <div class="category-checkbox-group" v-for="cat in categories" :key="cat">
      <label class="checkbox">
        <input
          type="checkbox"
          :value="cat"
          v-model="selectedCategories"
          @change="updateFilter"
        />
        {{ cat }}
      </label>
    </div>
  </div>

</template>

<sttyle scoped>

</sttyle>