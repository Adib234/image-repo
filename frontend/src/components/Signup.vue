<template>
  <div>
    <h1 class="is-size-1">Image Repository 🖼️</h1>
    <div class="login card">
      <section class="hero">
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" placeholder="Email" />
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span class="icon is-small is-right">
              <i v-if="validEmail" class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="password" placeholder="Password" />
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
            <span class="icon is-small is-right">
              <i v-if="validPassword" class="fas fa-check"></i>
            </span>
          </p>
        </div>
        <button class="login-button button is-primary is-light is-rounded">Sign me up!</button>

        <router-link to="/" custom v-slot="{ navigate }">
          <button
            @click="navigate"
            @keypress.enter="navigate"
            role="link"
            class="signin-button button is-primary is-light is-rounded"
          >Go back!</button>
        </router-link>
        <p class="creator is-size-3">Made with ❤️ by A.K.M. Adib</p>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Signup",
  data() {
    return { validPassword: false, validEmail: false };
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
  margin-right: 24rem;
  padding: 2rem;
  margin-left: 24rem;
  padding-bottom: 0.5rem;
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
