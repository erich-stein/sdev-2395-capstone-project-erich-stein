<script>
  import { createRouter, createWebHistory } from 'vue-router'
  import Home from './views/Home.vue'
  import Login from './views/Login.vue'
  import Profile from './views/Profile.vue'
  import CreateRecipe from './views/CreateRecipe.vue'
  import CreateAccount from './views/CreateAccount.vue'
  import Explore from './views/Explore.vue'

  const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/login', name: 'Login', component: Login},
    {path: '/profile', name: 'Profile', component: Profile},
    {path: '/create-recipe', name: 'CreateRecipe', component: CreateRecipe},
    {path: '/create-account', name: 'CreateAccount', component: CreateAccount},
    {path: '/explore', name: 'Explore', component: Explore},
  ]

  const router = createRouter({
    history: createWebHistory(),
    routes
  })

  export default router
</script>