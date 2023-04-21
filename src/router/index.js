import { createRouter, createWebHashHistory } from 'vue-router'
import store from '@/store'

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
    path: '/submit',
    name: 'Submit',
    component: () => import ('@/views/Submit/Submit.vue'),
    meta: {
      showInNavBar: true,
      requiredLogin: true,
      keepAlive: true,
      icon: 'mdi-transfer'
    }
  },
  {
    path: '/instruction',
    name: 'Instruction',
    component: () => import ('@/views/Instruction/Instruction.vue'),
    meta: {
      showInNavBar: false,
      requiredLogin: false,
      icon: 'mdi-help'
    }
  },
  {
    path: '/mylearnware',
    name: 'MyLearnware',
    component: () => import ('@/views/MyLearnware/MyLearnware.vue'),
    meta: {
      name: 'My Learnware',
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
      class: ['py-2.5 rounded-lg border-2']
    },
  },
  {
    path: '/changepassword',
    name: 'ChangePassword',
    component: () => import ('@/views/ChangePassword/ChangePassword.vue'),
    meta: {
      showInNavBar: true,
      requiredLogin: true,
      name: 'Change Password',
      icon: 'mdi-account-edit',
      class: ['py-2.5 rounded-lg']
    }
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
  }],
  scrollBehavior (to, from, savedPosition) {
    return { top: 0 }
  }
})

Router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiredLogin)) {
    if (store && !store.getters.getLoggedIn) {
      store.commit('setShowGlobalError', true)
      store.commit('setGlobalErrorMsg', 'Please login first.')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default Router