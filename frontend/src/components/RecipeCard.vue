<script>
/**
 * Recipe card component to display minimal
 * information from recipes and make browsing
 * easier and nicer.
 */
export default {
  props: {
    recipe: {
      type: Object,
      required: true
    }
  },
  // need something to format date
  methods: {
    goToRecipe() {
      this.$router.push(`/recipe/${this.recipe.id}`)
    }
  }
}

</script>

<template>
  <div class="recipe-card" @click="goToRecipe">
    <!--if image add here-->
    <h3 class="recipe-title">{{ recipe.title }}</h3>
    <p class="recipe-description">{{ recipe.short_desc }}</p>

    <div class="recipe-extra">
      <span class="recipe-date">{{ recipe.timestamp }}</span>
      <div v-if="recipe.updated" class="recipe-updated"> Last updated: {{recipe.updated}} </div>
      <div v-if="recipe.categories?.length" class="recipe-categories">
        <span v-for="cat in recipe.categories" :key="cat" class="category">
          {{ cat }}, 
        </span>
      </div>
    </div>
  </div>

</template>

<style scoped>
.recipe-card {
  border-radius: 0.75rem;
  /*background-image: linear-gradient(144deg, #af40ff, #f342d6 50%, #e7eb00);*/
  background-image: linear-gradient(144deg, #3bbec7, #f5eabc 80%);
  padding: 4px;
  color:#ffffff;
  box-shadow: rgba(0, 0, 0, 0.438) 4px 5px 15px -5px;
  cursor: pointer;
}

</style>