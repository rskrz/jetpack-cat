import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Commands from "./views/Commands.vue"

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "*",
      redirect: "Home"
    },
    {
      path: "/Commands",
      name: "Commands",
      component: Commands
    }
  ]
});
