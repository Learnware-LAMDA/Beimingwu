import { createRouter, createWebHashHistory } from "vue-router";
import store from "@main/store";

const Router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "Home",
      component: () => import("@/views/Home.vue"),
      meta: {
        showInNavBar: true,
        icon: "mdi-home",
      },
    },
    {
      path: "/summary",
      name: "Summary",
      component: () => import("@/views/Summary.vue"),
      meta: {
        showInNavBar: true,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: "/alllearnware",
      name: "Learnwares",
      component: () => import("@/views/Learnwares.vue"),
      meta: {
        showInNavBar: true,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: '/submit',
      name: 'Submit',
      component: () => import("@main/views/Submit.vue"),
      meta: {
        showInNavBar: false,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: "/alluser",
      name: "Users",
      component: () => import("@/views/Users.vue"),
      meta: {
        showInNavBar: true,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: "/learnwaredetail",
      name: "LearnwareDetail",
      component: () => import("@main/views/LearnwareDetail.vue"),
      meta: {
        showInNavBar: false,
        icon: "mdi-bullseye-arrow",
      },
    },
    {
      path: "/userlearnware",
      name: "UserLearnware",
      component: () => import("@main/views/MyLearnware.vue"),
      meta: {
        name: "My Learnware",
        showInNavBar: false,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: "/user",
      name: "User",
      meta: {
        showInNavBar: true,
        icon: "mdi-account",
      },
      children: [
        {
          path: "/login",
          name: "Login",
          component: () => import("@/views/Login.vue"),
          meta: {
            showInNavBar: true,
            hideWhenLoggedIn: true,
            icon: "mdi-login",
          },
        },
        {
          path: "/logout",
          name: "Logout",
          component: () => import("@main/views/Logout.vue"),
          meta: {
            showInNavBar: true,
            requiredLogin: true,
            icon: "mdi-logout",
            variant: "outlined",
            class: ["rounded border-2"],
          },
        },
      ],
    },
    {
      path: "/language",
      name: "Language",
      meta: {
        showInNavBar: true,
        icon: "mdi-earth",
      },
      children: [
        {
          path: "/language/zh",
          name: "Chinese",
          component: () => import("@main/views/ChangeLanguage.vue"),
          meta: {
            showInNavBar: true,
            icon: "🇨🇳",
            variant: "outlined",
          },
        },
        {
          path: "/language/en",
          name: "English",
          component: () => import("@main/views/ChangeLanguage.vue"),
          meta: {
            showInNavBar: true,
            icon: "🇺🇸",
            variant: "outlined",
          },
        },
      ],
    },
  ],
});

Router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiredLogin)) {
    if (store && !store.getters.getLoggedIn) {
      store.commit("setShowGlobalError", true);
      store.commit("setGlobalErrorMsg", "Please login first.");
      next({
        path: "/login",
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default Router;
