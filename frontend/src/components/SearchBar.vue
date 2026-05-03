<script>
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
      v-model="searchTerm"
      placeholder="Search..."
      @keyup.enter="search"
    />
    <select v-model="searchType" class="search-type">
      <option value="title">Name</option>
      <option value="tags">Tags</option>
    </select>
    <button type="button" @click="search">Search</button>
  </div>

</template>

<style scoped>

</style>