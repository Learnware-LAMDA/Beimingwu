import { createRouter, createWebHashHistory } from "vue-router";
import store from "@main/store";
import { Component } from "vue";
import NProgress from "@main/plugins/nprogress";

const Router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      name: "Summary",
      component: (): Promise<Component> => import("@admin/views/Summary.vue"),
      meta: {
        showInNavBar: true,
        icon: "mdi-eye",
      },
    },
    {
      path: "/alllearnware",
      name: "Search",
      component: (): Promise<Component> => import("@main/views/Search.vue"),
      props: {
        isAdmin: true,
      },
      meta: {
        showInNavBar: true,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-file-eye",
      },
    },
    {
      path: "/submit",
      name: "Submit",
      component: (): Promise<Component> => import("@main/views/Submit.vue"),
      meta: {
        showInNavBar: false,
        requiredLogin: true,
        keepAlive: true,
        icon: "mdi-upload",
      },
    },
    {
      path: "/alluser",
      name: "Users",
      component: (): Promise<Component> => import("@admin/views/Users.vue"),
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
      component: (): Promise<Component> => import("@main/views/LearnwareDetail.vue"),
      meta: {
        showInNavBar: false,
        icon: "mdi-bullseye-arrow",
      },
    },
    {
      path: "/userlearnware",
      name: "UserLearnware",
      component: (): Promise<Component> => import("@main/views/MyLearnware.vue"),
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
          component: (): Promise<Component> => import("@main/views/Login.vue"),
          meta: {
            showInNavBar: true,
            hideWhenLoggedIn: true,
            icon: "mdi-login",
          },
        },
        {
          path: "/logout",
          name: "Logout",
          component: (): Promise<Component> => import("@main/views/Logout.vue"),
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
        icon: "mdi-translate",
      },
      children: [
        {
          path: "/language/zh-cn",
          name: "Chinese",
          component: (): Promise<Component> => import("@main/views/ChangeLanguage.vue"),
          meta: {
            showInNavBar: true,
            icon: "🇨🇳",
            variant: "outlined",
          },
        },
        {
          path: "/language/en",
          name: "English",
          component: (): Promise<Component> => import("@main/views/ChangeLanguage.vue"),
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

Router.beforeEach((to, _from, next) => {
  NProgress.start();

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

Router.afterEach(() => {
  NProgress.done();
});

export default Router;
