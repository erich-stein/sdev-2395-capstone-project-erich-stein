<script>
  import { createRouter, createWebHistory } from 'vue-router'
  import Home from './views/Home.vue'
  import Login from './views/Login.vue'
  import Profile from './views/Profile.vue'
  import CreateRecipe from './views/CreateRecipe.vue'
  import CreateAccount from './views/CreateAccount.vue'
  import Explore from './views/Explore.vue'

  const routes = [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile,
      meta: {requiresAuth: true}
    },
    {
      path: '/create-recipe',
      name: 'CreateRecipe',
      component: CreateRecipe,
      meta: {requiresAuth: true}
    },
    {
      path: '/create-account',
      name: 'CreateAccount',
      component: CreateAccount
    },
    {
      path: '/explore',
      name: 'Explore',
      component: Explore
    },
  ]

  const router = createRouter({
    history: createWebHistory(),
    routes
  })

  // maybe add something to check if token is valid
  // and remove it if invalid as a backup
  // also, a way to hide routes if logged in might go here
  router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!localStorage.getItem('token')) {
        console.log('Redirecting to login')
        next({ name: 'Login' })
      } else {
        console.log('Authorized')
        next()
      }
    } else {
      console.log('Authorization not required')
      next()
    }
  })

  export default router
</script>