<template>
  <div>
    <h2 class="is-size-2">Add</h2>
    <div class="level is-3">
      <input
        class="file input is-medium"
        type="text"
        placeholder="Enter relevant keywords for image or click the button to upload images"
      />
      <button v-on:click="s3upload" class="button is-light is-medium">
        Add
      </button>
    </div>
    <div>
      <input class="button is-light is-medium" type="file" id="fileUpload" />
    </div>
    <progress max="”100”" value="”0”"></progress>
  </div>
</template>

<script>
import Vue from "vue";
import AWS from "aws-sdk";
import Buefy from "buefy";
import "buefy/dist/buefy.css";
Vue.use(Buefy);
export default {
  name: "Search",
  data() {
    return {};
  },
  methods: {
    success() {
      this.$buefy.toast.open({
        message: "Yay, your file has been uploaded",
        type: "is-success",
        position: "is-bottom",
        duration: 3000,
      });
    },
    s3upload() {
      let bucketName = process.env.VUE_APP_BUCKET_NAME;
      let bucketRegion = process.env.VUE_APP_BUCKET_REGION;
      let IdentityPoolId = process.env.VUE_APP_IDENTITY_POOL_ID;

      AWS.config.update({
        region: bucketRegion,
        credentials: new AWS.CognitoIdentityCredentials({
          IdentityPoolId: IdentityPoolId,
        }),
      });

      var s3 = new AWS.S3({
        apiVersion: "2006-03-01",
        params: { Bucket: bucketName },
      });

      var files = document.getElementById("fileUpload").files;
      if (files) {
        var file = files[0];
        var fileName = file?.name;
        var filePath = `${bucketName}/` + fileName;

        var upload = s3.upload({
          Bucket: bucketName,
          Key: filePath,
          Body: file,
        });
        var promise = upload.promise();

        promise.then(
          // eslint-disable-next-line no-unused-vars
          function(data) {
            alert("Successfully uploaded photo.");
          },
          function(err) {
            return alert(
              "There was an error uploading your photo: ",
              err.message
            );
          }
        );
      }
    },
  },
};
</script>

<style scoped>
.level {
  padding: 0 2rem 0.5rem 2rem;
}

.input {
  margin-right: 1rem;
}

.is-size-2 {
  margin-top: 1rem;
}
</style>
