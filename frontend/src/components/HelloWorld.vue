<template>
  <div class="hello">
    <h1 class="is-size-1">Image Repository 🖼️</h1>
    <div class="login card" v-if="!authenticated">
      <section class="hero">
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" v-model="email" type="email" placeholder="Email" />
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i v-if="validEmail" class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left">
            <input class="input" v-model="password" type="password" placeholder="Password" />
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        <button
          v-on:click="authenticate"
          class="login-button button is-primary is-light is-rounded"
        >Log me in!</button>
        <p>Or if you've never signed up before!</p>
        <router-link to="/signup" custom v-slot="{ navigate }">
          <button
            @click="navigate"
            @keypress.enter="navigate"
            role="link"
            class="signin-button button is-primary is-light is-rounded"
          >Sign me up!</button>
        </router-link>
        <p class="creator is-size-3">Made with ❤️ by A.K.M. Adib</p>
      </section>
    </div>
    <p
      v-if="!authenticated"
      class="description is-size-2"
    >My goal is to help you securely upload images and be able to retrieve from a public repository and your own through text and other images 🙂</p>
    <Add v-bind:email="email" v-on:session="authenticated=false" v-if="authenticated" />
    <Search v-bind:email="email" v-if="authenticated" />
    <Delete v-bind:email="email" v-if="authenticated" />
  </div>
</template>

<script>
import Add from "./Add";
import Search from "./Search";
import Delete from "./Delete";
import axios from "axios";

export default {
  name: "HelloWorld",
  data() {
    return { email: "", password: "", authenticated: false, validEmail: false };
  },

  components: {
    Add,
    Search,
    Delete
  },
  methods: {
    authenticate: function() {
      if (this.email.length == 0 && this.password.length == 0) {
        return this.$buefy.toast.open({
          message: "Missing credential(s)",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.email.length == 0 && this.password.length > 0) {
        return this.$buefy.toast.open({
          message: "Missing credential(s)",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.email.length > 0 && this.password.length == 0) {
        return this.$buefy.toast.open({
          message: "Missing credential(s)",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.password.length < 5) {
        return this.$buefy.toast.open({
          message: "Missing credential(s)",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else {
        if (
          /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(
            this.email
          )
        ) {
          let self = this;
          axios
            .post(`http://127.0.0.1:5000/login`, {
              email: this.email,
              password: this.password
            })
            // eslint-disable-next-line no-unused-vars
            .then(function(response) {
              self.authenticated = true;
              self.password = "";
              return self.$buefy.toast.open({
                message: "Login success!",
                type: "is-success",
                position: "is-bottom",
                duration: 10000
              });
            })
            // eslint-disable-next-line no-unused-vars
            .catch(function(error) {
              return self.$buefy.toast.open({
                message: "Incorrect email or password",
                type: "is-danger",
                position: "is-bottom",
                duration: 10000
              });
            });
        } else {
          return this.$buefy.toast.open({
            message: "Please enter a valid email",
            type: "is-danger",
            position: "is-bottom",
            duration: 10000
          });
        }
      }
    }
  }
};
</script>
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.login {
  min-width: 15rem;
  padding: 2rem;
  padding-bottom: 0.5rem;
  margin: auto;
  width: 45%;
}
.login-button {
  margin-bottom: 0.5rem;
}
.signin-button {
  margin-top: 0.5rem;
}
.creator {
  margin-top: 2rem;
}
.description {
  margin-top: 2rem;
}
</style>
