<script>
/**
 * Search bar component that emits a
 * term and a type.
 * 
 * The term is what to search for and
 * the type is what to search in.
 * 
 * Extra types may be added.
 */
export default {
  data() {
    return {
      searchTerm: '',
      searchType: 'title'
    }
  },
  methods: {
    search() {
      this.$emit('search',
        this.searchTerm.trim(),
        this.searchType
      )
    }
  }
}

</script>

<template>
  <div class="search-bar">
    <input
      type="text"
      class="input"
      v-model="searchTerm"
      placeholder="Search..."
      @keyup.enter="search"
    />
    <select v-model="searchType" class="search-type">
      <option value="title">Name</option>
      <option value="tags">Tags</option>
    </select>
    <button type="button" @click="search">
      <span>Search</span>
    </button>
  </div>

</template>

<style scoped>

</style>