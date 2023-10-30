import { createRouter, createWebHashHistory } from "vue-router";
import store from "../store";
import { Component } from "vue";

const Router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "Home",
      component: (): Promise<Component> => import("../views/Home.vue"),
      meta: {
        showInNavBar: true,
        icon: "mdi-home",
      },
    },
    {
      path: "/search",
      name: "Search",
      component: (): Promise<Component> => import("../views/Search.vue"),
      meta: {
        showInNavBar: true,
        keepAlive: true,
        icon: "mdi-magnify",
      },
    },
    {
      path: "/submit",
      name: "Submit",
      component: (): Promise<Component> => import("../views/Submit.vue"),
      meta: {
        showInNavBar: true,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-transfer",
      },
    },
    {
      path: "/docs",
      name: "Docs",
      component: (): Promise<Component> => import("../views/Docs.vue"),
      meta: {
        showInNavBar: true,
        name: "Docs",
        icon: "mdi-book-open-page-variant",
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
          component: (): Promise<Component> => import("../views/Login.vue"),
          meta: {
            showInNavBar: true,
            hideWhenLoggedIn: true,
            icon: "mdi-login",
          },
        },
        {
          path: "/register",
          name: "Register",
          component: (): Promise<Component> => import("../views/Register.vue"),
          meta: {
            showInNavBar: true,
            hideWhenLoggedIn: true,
            icon: "mdi-account-plus",
            variant: "outlined",
            class: ["py-2.5 rounded-lg border-2"],
          },
        },
        {
          path: "/changepassword",
          name: "ChangePassword",
          component: (): Promise<Component> => import("../views/ChangePassword.vue"),
          meta: {
            showInNavBar: true,
            requiredLogin: true,
            name: "Change Password",
            icon: "mdi-account-edit",
            class: ["py-2.5 rounded-lg"],
          },
        },
        {
          path: "/mylearnware",
          name: "MyLearnware",
          component: (): Promise<Component> => import("../views/MyLearnware.vue"),
          meta: {
            name: "My Learnware",
            showInNavBar: true,
            requiredLogin: true,
            keepAlive: true,
            icon: "mdi-file-eye",
          },
        },
        {
          path: "/clienttoken",
          name: "ClientToken",
          component: (): Promise<Component> => import("../views/ClientToken.vue"),
          meta: {
            showInNavBar: true,
            requiredLogin: true,
            name: "Client Token",
            icon: "mdi-key",
            keepAlive: true,
          },
        },
        {
          path: "/logout",
          name: "Logout",
          component: (): Promise<Component> => import("../views/Logout.vue"),
          meta: {
            showInNavBar: true,
            requiredLogin: true,
            icon: "mdi-logout",
            variant: "outlined",
            class: ["py-2.5 rounded border-2"],
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
          path: "/language/zh-cn",
          name: "Chinese",
          component: (): Promise<Component> => import("../views/ChangeLanguage.vue"),
          meta: {
            showInNavBar: true,
            icon: "🇨🇳",
            variant: "outlined",
          },
        },
        {
          path: "/language/en",
          name: "English",
          component: (): Promise<Component> => import("../views/ChangeLanguage.vue"),
          meta: {
            showInNavBar: true,
            icon: "🇺🇸",
            variant: "outlined",
          },
        },
      ],
    },
    {
      path: "/learnwaredetail",
      name: "LearnwareDetail",
      component: (): Promise<Component> => import("../views/LearnwareDetail.vue"),
      meta: {
        showInNavBar: false,
        icon: "mdi-bullseye-arrow",
      },
    },
    {
      path: "/verify_email",
      name: "VerifyEmail",
      component: (): Promise<Component> => import("../views/VerifyEmail.vue"),
      meta: {
        showInNavBar: false,
        icon: "mdi-email-check-outline",
      },
    },
    {
      path: "/reset_password",
      name: "ResetPassword",
      component: (): Promise<Component> => import("../views/ResetPassword.vue"),
      meta: {
        showInNavBar: false,
        icon: "mdi-email-check-outline",
      },
    },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

Router.beforeEach((to, from, next) => {
  if (from.name === to.name) {
    return next(false);
  }
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
