import Vue from "vue";
import Router from "vue-router";

const Home = () =>
  import(/* webpackChunkName: "Home" */ "./views/Home.vue");
const Commands = () =>
  import(/* webpackChunkName: "Commands" */ "./views/Commands.vue");

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
