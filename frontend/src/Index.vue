<script>
  import { createRouter, createWebHistory } from 'vue-router'
  import Home from './components/Home.vue'
  import Login from './components/Login.vue'
  import Profile from './components/Profile.vue'
  import CreateRecipe from './components/CreateRecipe.vue'

  const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/login', name: 'Login', component: Login},
    {path: '/profile', name: 'Profile', component: Profile},
    {path: '/create-recipe', name: 'CreateRecipe', component: CreateRecipe},
  ]

  const router = createRouter({
    history: createWebHistory(),
    routes
  })

  export default router
</script>