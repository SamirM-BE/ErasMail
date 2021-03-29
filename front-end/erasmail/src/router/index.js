import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Loading from '../views/Loading.vue'
import Threads from '../views/Threads.vue'
import Emails from '../views/Emails.vue'
import LandingPage from '../views/LandingPage.vue'
import Stats from '../views/Stats.vue'
import Newsletters from '../views/Newsletters.vue'

const routes = [
  {
    path: '/',
    name: 'landingpage',
    component: LandingPage,
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresUnAuth: true }
  },
  {
    path: '/loading',
    name: 'loading',
    component: Loading,
    beforeEnter: (to, from, next) => {
      if (from.name === 'login' && store.getters['auth/loggedIn']) next()
      else next({ name: 'landingpage' })
    }
  },
  {
    path: '/threads',
    name: 'threads',
    component: Threads,
    meta: { requiresAuth: true }
  },
  {
    path: '/emails',
    name: 'emails',
    component: Emails,
    meta: { requiresAuth: true }
  },
  {
    path: '/stats',
    name: 'stats',
    component: Stats,
    meta: { requiresAuth: true }
  },
  {
    path: '/newsletters',
    name: 'newsletters',
    component: Newsletters,
    meta: { requiresAuth: true }
  },

  {
    // will match everything
    path: "/:catchAll(.*)",
    redirect: { name: 'landingpage' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (!store.getters['auth/loggedIn']) {
      next({
        name: 'login'
      })
    } else {
      next()
    }
  } else if (to.matched.some(record => record.meta.requiresUnAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    if (store.getters['auth/loggedIn']) {
      next({
        name: 'landingpage'
      })
    } else {
      next()
    }
  } else {
    next() // make sure to always call next()!
  }
})

export default router
