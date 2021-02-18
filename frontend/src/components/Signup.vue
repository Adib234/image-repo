<template>
  <div>
    <h1 class="is-size-1">Image Repository 🖼️</h1>
    <div class="login card">
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
            <input
              class="input"
              v-model="password"
              type="password"
              placeholder="Password, please make sure it's greater than 5 characters"
            />
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        <button
          v-on:click="verifyUser"
          class="login-button button is-primary is-light is-rounded"
        >Sign me up!</button>

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
import axios from "axios";
import S3 from "aws-sdk/clients/s3";
import CognitoIdentityCredentials from "aws-sdk/lib/credentials";

let publicBucketName = process.env.VUE_APP_BUCKET_NAME;
let bucketRegion = process.env.VUE_APP_BUCKET_REGION;
let IdentityPoolId = process.env.VUE_APP_IDENTITY_POOL_ID;

var s3 = new S3({
  apiVersion: "2006-03-01",
  params: { Bucket: publicBucketName },
  region: bucketRegion,
  credentials: new CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});
export default {
  name: "Signup",
  data() {
    return { email: "", password: "", validEmail: false };
  },
  methods: {
    verifyUser: function() {
      if (this.email.length == 0 && this.password.length == 0) {
        return this.$buefy.toast.open({
          message: "Missing password and email",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.email.length == 0 && this.password.length > 0) {
        return this.$buefy.toast.open({
          message: "Missing email",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.email.length > 0 && this.password.length == 0) {
        return this.$buefy.toast.open({
          message: "Missing password",
          type: "is-danger",
          position: "is-bottom",
          duration: 10000
        });
      } else if (this.password.length < 5) {
        return this.$buefy.toast.open({
          message: "Password must be greater than 5 characters",
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
            .post(`http://127.0.0.1:5000/signup`, {
              email: this.email,
              password: this.password
            })
            // eslint-disable-next-line no-unused-vars
            .then(function(response) {
              var params = {
                Bucket: publicBucketName,
                Key: `${self.email}/`
              };
              s3.putObject(params, function(err, data) {
                if (err) {
                  console.log("Error creating the folder: ", err);
                } else {
                  console.log(data);
                }
              });
              return self.$buefy.toast.open({
                message: "Signup success, please login now",
                type: "is-success",
                position: "is-bottom",
                duration: 10000
              });
            })
            // eslint-disable-next-line no-unused-vars
            .catch(function(error) {
              return self.$buefy.toast.open({
                message: "You've already signed up, please login",
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
