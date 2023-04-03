import { createRouter, createWebHashHistory } from 'vue-router'

const Router = createRouter({
  history: createWebHashHistory(),
  routes: [{
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home/Home.vue'),
    meta: {
      showInNavBar: true,
      icon: 'mdi-home'
    }
  },
  {
    path: '/submit',
    name: 'Submit',
    component: () => import ('@/views/Submit/Submit.vue'),
    meta: {
      showInNavBar: true,
      requiredLogin: true,
      icon: 'mdi-transfer'
    }
  },
  {
    path: '/search',
    name: 'Search',
    component: () => import ('@/views/Search/Search.vue'),
    meta: {
      showInNavBar: true,
      keepAlive: true,
      icon: 'mdi-magnify'
    }
  },
  {
    path: '/mylearnware',
    name: 'MyLearnware',
    component: () => import ('@/views/MyLearnware/MyLearnware.vue'),
    meta: {
      showInNavBar: true,
      requiredLogin: true,
      keepAlive: true,
      icon: 'mdi-file-eye'
    }
  },
  {
    path: '/learnwaredetail',
    name: 'LearnwareDetail',
    component: () => import ('@/views/LearnwareDetail/LearnwareDetail.vue'),
    meta: {
      showInNavBar: false,
      icon: 'mdi-bullseye-arrow'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import ('@/views/Login/Login.vue'),
    meta: {
      showInNavBar: true,
      hideWhenLoggedIn: true,
      icon: 'mdi-account'
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import ('@/views/Register/Register.vue'),
    meta: {
      showInNavBar: true,
      hideWhenLoggedIn: true,
      icon: 'mdi-account-plus',
      variant: 'outlined',
      class: ['py-2.5 bg-primary rounded-lg border-2']
    },
  },
  {
    path: '/logout',
    name: 'Logout', 
    component: () => import ('@/views/Logout/Logout.vue'),
    meta: {
      showInNavBar: true,
      requiredLogin: true,
      icon: 'mdi-logout',
      variant: 'outlined',
      class: ['py-2.5 rounded border-2']
    },
  },]
})

export default Router