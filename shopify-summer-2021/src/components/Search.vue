<template>
  <div>
    <h2 class="is-size-2">Search and Add</h2>
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
    <div class="container">
      <p v-if="uploaded" class="is-size-3">The image you just uploaded</p>
      <img class="img" v-if="uploaded" :src="imageUrl" />

      <!-- <img
        class="img"
        src="https://homepages.cae.wisc.edu/~ece533/images/baboon.png"
      /> -->
    </div>
  </div>
</template>

<script>
import AWS from "aws-sdk";
import Vue from "vue";
import { Toast } from "buefy";
import "buefy/dist/buefy.css";
Vue.use(Toast);

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
export default {
  name: "Search",
  data() {
    return {
      uploaded: false,
      fileNameGlobal: "",
      imageUrl: "",
    };
  },
  methods: {
    showImage: function() {
      var params = {
        Bucket: bucketName,
        Key: `${bucketName}/` + this.fileNameGlobal,
      };
      let getImage = s3.getObject(params);

      let promise = getImage.promise();
      let self = this;

      promise.then(
        function(data) {
          let imageData = data.Body;
          let str = imageData.reduce(function(a, b) {
            return a + String.fromCharCode(b);
          }, "");
          let srcUrl =
            "data:image/jpeg;base64, " +
            btoa(str).replace(/.{76}(?=.)/g, "$&\n");
          self.imageUrl = srcUrl;
        },
        function(err) {
          console.log(err, err.stack);
        }
      );
    },
    s3upload: function() {
      let self = this;

      var files = document.getElementById("fileUpload").files;
      try {
        if (files) {
          var file = files[0];
          var fileName = file?.name;
          this.fileNameGlobal = fileName;
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
              self.uploaded = true;
              self.showImage();
              return self.$buefy.toast.open({
                message: "Yay, your file has been uploaded!",
                type: "is-success",
                position: "is-bottom",
                duration: 3000,
              });
            },
            // eslint-disable-next-line no-unused-vars
            function(err) {
              return self.$buefy.toast.open({
                message:
                  "Your file failed to be uploaded, please try again or later",
                type: "is-danger",
                position: "is-bottom",
                duration: 3000,
              });
            }
          );
        }
      } catch (err) {
        return self.$buefy.toast.open({
          message: "Please upload something",
          type: "is-danger",
          position: "is-bottom",
          duration: 3000,
        });
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

.img {
  height: 15rem;
}
</style>
