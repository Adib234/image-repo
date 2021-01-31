<template>
  <div class="parent">
    <h1 class="is-size-2">Search</h1>
    <div class="level">
      <input
        v-model="query"
        class="file input is-medium"
        type="text"
        placeholder="Enter relevant keywords for image and we will show the top 5 images "
      />
      <button v-on:click="searchRequest" class="button is-light is-medium">Search</button>
    </div>
    <div class="control">
      <label class="radio">
        <input type="radio" id="public" value="Public" v-model="permissions" />
        Public
      </label>
      <label class="radio">
        <input type="radio" id="private" value="Private" v-model="permissions" />
        Private
      </label>
    </div>
  </div>
</template>

<script>
import axios from "axios";
//import AWS from "aws-sdk";

export default {
  name: "Search",
  data() {
    return { query: "", permissions: "" };
  },
  methods: {
    searchRequest: function() {
      if (this.query.length > 0) {
        axios
          .post(`http://127.0.0.1:5000/search`, {
            query: this.query
          })
          .then(function(response) {
            console.log(response.data);
          })
          // eslint-disable-next-line no-unused-vars
          .catch(function(error) {
            return this.$buefy.toast.open({
              message: "Sorry, please try again",
              type: "is-danger",
              position: "is-bottom",
              duration: 6000
            });
          });
      } else {
        return this.$buefy.toast.open({
          message: "Hold up, you haven't searched anything",
          type: "is-danger",
          position: "is-bottom",
          duration: 6000
        });
      }
    }
  }
};
</script>
<style scoped>
.level {
  margin-left: 2rem;
  margin-right: 2rem;
}
.button {
  margin-left: 2rem;
}
.parent {
  margin-top: 3rem;
}
</style>