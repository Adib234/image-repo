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
    <div class="search level">
      <div class="img-container level-item" v-for="image in imageUrls" v-bind:key="image">
        <img class="img" :src="image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AWS from "aws-sdk";
let bucketName = process.env.VUE_APP_BUCKET_NAME;
let bucketRegion = process.env.VUE_APP_BUCKET_REGION;
let IdentityPoolId = process.env.VUE_APP_IDENTITY_POOL_ID;

AWS.config.update({
  region: bucketRegion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId
  })
});
var s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: bucketName }
});
export default {
  name: "Search",
  data() {
    return { query: "", permissions: "", imageUrls: [] };
  },
  methods: {
    searchRequest: function() {
      let self = this;

      if (this.query.length > 0) {
        axios
          .post(`http://127.0.0.1:5000/search`, {
            query: this.query
          })
          .then(function(response) {
            let imageArray = [];
            if (response.data.length == 0) {
              throw response;
            }
            for (let key of response.data) {
              imageArray.push(key["_source"]["file_name"]);
            }

            for (let imageFile of imageArray) {
              var params = {
                Bucket: bucketName,
                Key: `${bucketName}/` + imageFile
              };
              let getImage = s3.getObject(params);

              let promise = getImage.promise();

              promise.then(
                function(data) {
                  let imageData = data.Body;
                  let str = imageData.reduce(function(a, b) {
                    return a + String.fromCharCode(b);
                  }, "");
                  let base64encode = btoa(str).replace(/.{76}(?=.)/g, "$&\n");
                  let srcUrl = `data:image/jpeg;base64, ${base64encode}`;
                  self.imageUrls.push(srcUrl);
                },
                function(err) {
                  console.log(err, err.stack);
                }
              );
            }
          })
          // eslint-disable-next-line no-unused-vars
          .catch(function(error) {
            return self.$buefy.toast.open({
              message: "Sorry, please try again or add more words",
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
.search {
  margin-top: 2rem;
}
.img-container {
  height: 15rem;
  width: 15rem;
  margin-left: 1rem;
}
.img {
  height: 15rem;
  width: 15rem;
}
</style>