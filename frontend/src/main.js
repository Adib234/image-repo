import Vue from "vue";
import App from "./App.vue";
import "buefy/dist/buefy.css";
import { Toast } from "buefy";
import "buefy/dist/buefy.css";

Vue.use(Toast);
Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
}).$mount("#app");
