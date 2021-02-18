<template>
  <div>
    <h1 class="is-size-2">Delete</h1>
    <div class="parent">
      <div class="level first">
        <button
          v-show="!deleted"
          v-on:click="imagesForDelete"
          class="button is-light is-medium"
        >Show my images to delete</button>
        <button class="button is-light is-medium" v-on:click="deleteNow" v-show="deleted">Delete</button>
        <button class="button escape is-light is-medium" v-on:click="escape" v-show="deleted">Escape</button>
      </div>
      <div class="level second">
        <div class="img-container level-item" v-for="object in myObjects" v-bind:key="object.key">
          <img class="img" :src="object.image" />
          <label class="checkbox">
            <input type="checkbox" @click="selectedDelete(object.key)" />
            Select this
          </label>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
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
  name: "Delete",
  data() {
    return { deleted: false, myObjects: [], selected: [] };
  },
  props: { email: String },
  methods: {
    imagesForDelete: function() {
      this.deleted = true;
      let getObjects = s3.listObjects({ Prefix: `${this.email}/` });
      let promise = getObjects.promise();
      let self = this;
      promise.then(
        function(data) {
          let final = [];
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
          if (final.length > 0) {
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
                    self1.myObjects.push({ image: srcUrl, key: object });
                  },
                  function(err) {
                    console.log(err, err.stack);
                  }
                );
              })
            );
          } else {
            return self.$buefy.toast.open({
              message: "You have no images to delete",
              type: "is-danger",
              position: "is-bottom",
              duration: 6000
            });
          }
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
    },
    selectedDelete: function(key) {
      this.selected.push(key);
    },
    deleteNow: function() {
      for (let deleteImage of this.selected) {
        console.log(deleteImage);
        let deletedRequest = s3.deleteObject({ Key: deleteImage });
        let promise = deletedRequest.promise();
        let self = this;
        promise.then(
          // eslint-disable-next-line no-unused-vars
          function(data) {
            self.myObjects.filter(image => image.key !== self.deleteImage);
          },
          function(err) {
            console.log(err);
            return self.$buefy.toast.open({
              message: "We couldn't delete your images, please try again later",
              type: "is-danger",
              position: "is-bottom",
              duration: 6000
            });
          }
        );
      }
      this.selected = [];
      this.myObjects = [];
      this.imagesForDelete();
    },
    escape: function() {
      this.deleted = false;
    }
  }
};
</script>


<style scoped>
.first {
  justify-content: center;
  margin-bottom: 2rem;
}
.second {
  flex-wrap: wrap;
}
.img-container {
  height: 15rem;
  width: 15rem;
  margin-left: 1rem;
  margin-bottom: 1rem;
  justify-content: flex-start;
}
.img {
  height: 15rem;
  width: 15rem;
}
.escape {
  margin-left: 0.5rem;
}
</style>