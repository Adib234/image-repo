import Vue from "vue";
import App from "./App.vue";
import "buefy/dist/buefy.css";
import { Toast } from "buefy";
import "buefy/dist/buefy.css";
import VueRouter from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import Signup from "./components/Signup.vue";
import NotFound from "./components/NotFound.vue";
Vue.use(VueRouter);
Vue.use(Toast);
const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "main",
      component: HelloWorld,
    },
    { path: "/signup", component: Signup },
    {
      path: "/*",
      component: NotFound,
    },
  ],
});
Vue.config.productionTip = false;

new Vue({ router, render: (h) => h(App) }).$mount("#app");
