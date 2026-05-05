<script>
/**
 * Component for recipe form that works with
 * both creating and editing recipes.
 * 
 * Does not use a 'submit' button so that
 * the enter key may be used to add tags,
 * ingredients, and instructions.
 */
import { CategoriesList } from '../assets/categories'

export default {
  props: {
    initData: {
      type: Object,
      default: () => ({
        title: '',
        short_desc: '',
        long_desc: '',
        categories: [],
        tags: [],
        ingredients: [],
        instructions: []
      })
    },
    submitLabel: {
      type: String,
      default: 'Create Recipe'
    }
  },
  data() {
    return {
      formData: {
        title: '',
        long_desc: '',
        short_desc: '',
        categories: [],
        tags: [],
        ingredients: [],
        instructions: []
      },
      newTag: '',
      newIngr: '',
      newInstr: '',
      loading: false, // helps prevent multiple submits and shows saving state
      message: '',
      errorMessage: '',
      categoriesList: CategoriesList
    }
  },
  mounted() {
    this.formData = JSON.parse(JSON.stringify(this.initData))
  },
  methods: {
    addTag() {
      const cleanedTag = this.newTag.trim().toLowerCase()
      if (cleanedTag && !this.formData.tags.includes(cleanedTag)) {
        this.formData.tags.push(cleanedTag)
        this.newTag = ''
      }
    },
    removeTag() {
      this.formData.tags.pop()
    },
    addIngredient() {
      const cleanedIngr = this.newIngr.trim()
      if (cleanedIngr) {
        this.formData.ingredients.push(cleanedIngr)
        this.newIngr = ''
      }
    },
    removeIngredient() {
      this.formData.ingredients.pop()
    },
    addInstruction() {
      const cleanedInstr = this.newInstr.trim()
      if (cleanedInstr) {
        this.formData.instructions.push(cleanedInstr)
        this.newInstr = ''
      }
    },
    removeInstruction() {
      this.formData.instructions.pop()
    },
    validateData() {
      if (!this.formData.title) {
        this.errorMessage = 'Recipe name is required'
        return false
      }
      if (!this.formData.short_desc) {
        this.errorMessage = 'At least a short description is required'
        return false
      }
      if (this.formData.ingredients.length < 1) {
        this.errorMessage = 'Add at least one ingredient'
        return false
      }
      if (this.formData.instructions.length < 1) {
        this.errorMessage = 'Add at least one instruction'
        return false
      }
      return true
    },
    async handleFormSubmit() {
      if (!this.validateData())
        return

      this.errorMessage = ''
      this.message = ''

      this.loading = true

      const cleanedData = {
        title: this.formData.title.trim(),
        long_desc: this.formData.long_desc.trim(),
        short_desc: this.formData.short_desc.trim(),
        categories: this.formData.categories,
        tags: this.formData.tags,
        ingredients: this.formData.ingredients,
        instructions: this.formData.instructions
      }

      try {
        await this.$emit('submit', cleanedData)

      } catch (error) {
        console.error('Error saving recipe: ', error)
        
        /*
        if (error.response) {
          // server responded with error
          this.errorMessage = error.response?.data?.errorMessage || 'Recipe submission failed'
          console.error(this.errorMessage)
        } else if (error.request) {
          // request but no response
          this.errorMessage = 'Cannot connect to server'
          console.error(this.errorMessage)
        } else {
          // something else
          this.errorMessage = 'Unexpected error'
          console.error(error.response?.data?.msg || 'Unknown error')
        } */
      } finally {
        this.loading = false
      }
    },
    cancel() {
      this.$emit('cancel')
    }
  }
}

</script>

<template>
  <div class="recipe-form">

    <form @submit.prevent="handleFormSubmit">

      <div class="form-section">
        <h2>Basic Information</h2>
        <hr/>

        <div class="form-group">
          <!--label for="formData.title">Recipe Name</label-->
          <input
            v-model="formData.title"
            class="input"
            type="text"
            placeholder="Name of recipe"
            required
            :disabled="loading"
          />
        </div>
        <div class="form-group">
          <!--label for="formData.short_desc">Short Description</label-->
          <textarea
            v-model="formData.short_desc"
            class="input"
            type="text"
            rows="2"
            placeholder="Brief description of recipe"
            required
            :disabled="loading"
          ></textarea>
          <small>{{ formData.short_desc.length }}</small>
        </div>
        <div class="form-group">
          <!--label for="formData.long_desc">Full Description</label-->
          <textarea
            v-model="formData.long_desc"
            class="input"
            type="text"
            rows="4"
            placeholder="Detailed description of recipe with history, notes, etc..."
            :disabled="loading"
          ></textarea>
        </div>
        <hr/>
      </div>

      <div class="form-section">
        <h2>Categories</h2>
        <p>Select some categories:</p>
        <hr/>
        <div class="checkbox-group" v-for="cat in categoriesList" :key="cat">
          <label class="checkbox">
            <input
              type="checkbox"
              :value="cat"
              v-model="formData.categories"
              :disabled="loading"
            />
            {{ cat }}
          </label>
        </div>
        <hr/>
      </div>

      <div class="form-section">
        <h2>Tags</h2>
        <p>Enter some tags to help search for your recipe:</p>
        <hr/>
        <div class="form-group">
          <label for="newTag">Add tags</label>
          <div class="form-input-button">
            <input
              v-model="newTag"
              class="input"
              type="text"
              placeholder="e.g., vegetarian, meat, quick, spicy..."
              @keyup.enter="addTag"
              :disabled="loading"
            />
            <button type="button" @click="addTag" :disabled="loading">
              <span>Add Tag</span>
            </button>
            <button type="button" @click="removeTag">
              <span>Remove Last Tag</span>
            </button>
          </div>
          <!--Display added tags-->
          <div v-if="formData.tags.length">
            <span v-for="tag in formData.tags" :key="tag">
              {{ tag }}, 
            </span>
          </div>
        </div>
        <hr/>
      </div>

      <div class="form-section">
        <h2>Ingredients</h2>
        <p>Enter the required ingredients:</p>
        <hr/>
        <div class="form-group">
          <label for="newIngr">Add ingredients</label>
          <div class="form-input-button">
            <input
              v-model="newIngr"
              class="input"
              type="text"
              placeholder="e.g., 1 cup rice, 1/4 tsp black pepper"
              @keyup.enter="addIngredient"
              :disabled="loading"
            />
            <button type="button" @click="addIngredient" :disabled="loading">
              <span>Add Ingredient</span>
            </button>
            <button type="button" @click="removeIngredient">
              <span>Remove Last Ingredient</span>
            </button>
          </div>
          <!--Display added ingredients-->
          <div v-if="formData.ingredients.length">
            <div v-for="ingr in formData.ingredients" :key="ingr">
              - {{ ingr }}
            </div>
          </div>
        </div>
        <hr/>
      </div>

      <div class="form-section">
        <h2>Instructions</h2>
        <p>Enter the instructions for the recipe:</p>
        <hr/>
        <div class="form-group">
          <label for="newInstr">Add instructions</label>
          <div class="form-input-button">
            <textarea
              v-model="newInstr"
              class="input"
              type="text"
              rows="3"
              placeholder="e.g., Combine dry ingredients"
              @keyup.enter="addInstruction"
              :disabled="loading"
            ></textarea>
            <button type="button" @click="addInstruction" :disabled="loading">
              <span>Add Instruction</span>
            </button>
            <button type="button" @click="removeInstruction">
              <span>Remove Last Instruction</span>
            </button>
          </div>
          <!--Display added instructions-->
          <div v-if="formData.instructions.length">
            <div v-for="instr in formData.instructions" :key="instr">
              - {{ instr }}
            </div>
          </div>
        </div>
        <hr/>
      </div>

      <div class="form-actions">
        <button type="button" @click="cancel" :disabled="loading">
          <span>Cancel</span>
        </button>
        <button type="button" @click="handleFormSubmit" :disabled="loading">
          <span v-if="loading">Saving...</span>
          <span v-else>{{ submitLabel }}</span>
        </button>
      </div>
    </form>

    <p v-if="message" class="message">{{ message }}</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>

</template>

<style scoped>

</style>