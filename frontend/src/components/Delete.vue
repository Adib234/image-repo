<template>
  <div>
    <h1 class="is-size-2">Delete</h1>
    <div class="parent">
      <div class="level first">
        <button
          v-on:click="imagesForDelete"
          class="button is-light is-medium"
        >Show my images to delete</button>
      </div>

      <div class="level">
        <div class="img-container level-item" v-for="image in myObjects" v-bind:key="image">
          <img class="img" :src="image" />
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import AWS from "aws-sdk";

let publicBucketName = process.env.VUE_APP_BUCKET_NAME;
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
  params: { Bucket: publicBucketName }
});
export default {
  name: "Delete",
  data() {
    return { myObjects: [] };
  },
  props: { email: String },
  methods: {
    imagesForDelete: function() {
      let getObjects = s3.listObjects({ Prefix: `${this.email}/` });
      let promise = getObjects.promise();
      let self = this;
      promise.then(
        function(data) {
          let final = [];
          // should do this with regex in the future, this is just a quick hack
          for (let object of data.Contents) {
            if (
              object.Key.endsWith(".jpg") ||
              object.Key.endsWith(".JPG") ||
              object.Key.endsWith(".png") ||
              object.Key.endsWith(".PNG")
            ) {
              final.push(object.Key);
            }
          }
          Promise.all(
            final.map(object => {
              let getImage = s3.getObject({
                Bucket: publicBucketName,
                Key: object
              });
              let promise = getImage.promise();
              let self1 = self;
              promise.then(
                function(data) {
                  let imageData = data.Body;
                  let str = imageData.reduce(function(a, b) {
                    return a + String.fromCharCode(b);
                  }, "");
                  let base64encode = btoa(str).replace(/.{76}(?=.)/g, "$&\n");
                  let srcUrl = `data:image/jpeg;base64, ${base64encode}`;
                  self1.myObjects.push(srcUrl);
                },
                function(err) {
                  console.log(err, err.stack);
                }
              );
            })
          );
        },
        function(err) {
          console.log(err);
          return self.$buefy.toast.open({
            message: "We couldn't fetch your images, please try again later",
            type: "is-danger",
            position: "is-bottom",
            duration: 6000
          });
        }
      );
    }
  }
};
</script>


<style scoped>
.first {
  justify-content: center;
  margin-bottom: 2rem;
}
.img-container {
  height: 15rem;
  width: 15rem;
  margin-left: 1rem;
  word-wrap: break-word;
  margin-bottom: 1rem;
}
.img {
  height: 15rem;
  width: 15rem;
}
</style>