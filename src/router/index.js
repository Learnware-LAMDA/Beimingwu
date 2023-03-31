import { createRouter, createWebHashHistory } from 'vue-router'

const Router = createRouter({
  history: createWebHashHistory(),
  routes: [{
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home/Home.vue'),
    meta: {
      icon: 'mdi-home'
    }
  },
  {
    path: '/submit',
    name: 'Submit',
    component: () => import ('@/views/Submit/Submit.vue'),
    meta: {
      icon: 'mdi-transfer'
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import ('@/views/Search/Search.vue'),
    meta: {
      icon: 'mdi-magnify'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import ('@/views/Login/Login.vue'),
    meta: {
      icon: 'mdi-account'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import ('@/views/Register/Register.vue'),
    meta: {
      icon: 'mdi-account-plus',
      variant: 'outlined',
      class: ['py-2.5 rounded border-2']
    },
  },]
})

export default Router