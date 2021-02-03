<template>
  <div>
    <button v-on:click="$emit('session')" class="logout button is-medium">Logout</button>
    <h2 class="is-size-2">Add</h2>
    <section class="hero">
      <div class="level">
        <input
          v-model="imageDescription"
          class="input is-medium"
          type="text"
          placeholder="Enter some description of the image if you'd like, otherwise we will classify the image on our own!"
        />

        <button v-on:click="s3upload" class="button is-light is-medium">Add</button>
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
      <div v-if="permissions=='Private'" class="private">
        <div v-bind:class="dropdown">
          <div class="dropdown-trigger">
            <button
              v-on:click="makeActive"
              class="button"
              aria-haspopup="true"
              aria-controls="dropdown-menu3"
            >
              <span>Private albums</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu3" role="menu">
            <div class="dropdown-content">
              <a href="#" class="dropdown-item">Overview</a>
              <a href="#" class="dropdown-item">Modifiers</a>
              <a href="#" class="dropdown-item">Grid</a>
            </div>
          </div>
        </div>
        <button v-on:click="addBucket" class="add-album button">Add new album</button>
        <input
          v-model="bucketUserName"
          v-if="adding"
          class="bucket input"
          type="text"
          placeholder="Album name"
        />
      </div>
      <div class="control1">
        <label class="radio">
          <input type="radio" value="Single" v-model="fileUpload" />
          Single
        </label>
        <label class="radio">
          <input type="radio" value="Bulk" v-model="fileUpload" />
          Bulk
        </label>
      </div>
      <div class="container has-text-centered">
        <div class="level">
          <input class="button is-light is-medium" type="file" id="fileUpload" />
        </div>
      </div>
    </section>

    <div class="container">
      <p v-if="uploaded" class="is-size-3">The image you just uploaded</p>
      <img class="img" v-if="uploaded" :src="imageUrl" />

      <!-- <img
        class="img"
        src="https://homepages.cae.wisc.edu/~ece533/images/baboon.png"
      />-->
    </div>
  </div>
</template>

<script>
import AWS from "aws-sdk";
import axios from "axios";

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
  name: "Add",
  props: { email: String },

  data() {
    return {
      uploaded: false,
      fileNameGlobal: "",
      imageUrl: "",
      imageDescription: "",
      permissions: "",
      fileUpload: "",
      dropdown: "dropdown",
      adding: false,
      bucketUserName: "",
      userBuckets: []
    };
  },

  methods: {
    showImage: function() {
      var params = {
        Bucket: bucketName,
        Key: `${bucketName}/` + this.fileNameGlobal
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
          let base64encode = btoa(str).replace(/.{76}(?=.)/g, "$&\n");
          let srcUrl = `data:image/jpeg;base64, ${base64encode}`;
          self.imageUrl = srcUrl;

          // tags == 0 test passes
          // tags > 1 works
          // * why does client give me bad request when server says 200
          if (self.permissions === "Public") {
            axios
              .post(`http://127.0.0.1:5000/tags`, {
                fileName: self.fileNameGlobal,
                image: base64encode,
                tags: self.imageDescription
              })
              .then(function(response) {
                console.log(response);
              })
              .catch(function(error) {
                console.log(error);
              });
          }
          // else {} private permissions
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
            Body: file
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
                duration: 6000
              });
            },
            // eslint-disable-next-line no-unused-vars
            function(err) {
              return self.$buefy.toast.open({
                message:
                  "Your file failed to be uploaded, please try again or later",
                type: "is-danger",
                position: "is-bottom",
                duration: 6000
              });
            }
          );
        }
      } catch (err) {
        return self.$buefy.toast.open({
          message: "Please upload something",
          type: "is-danger",
          position: "is-bottom",
          duration: 3000
        });
      }
    },
    makeActive: function() {
      //request works
      if (this.dropdown == "dropdown") {
        this.dropdown = "dropdown is-active";
        let self = this;
        axios
          .post(`http://127.0.0.1:5000/get_all_buckets`, {
            email: this.email
          })
          .then(function(response) {
            console.log(response);
            self.userBuckets = response.data;
          })
          .catch(function(error) {
            console.log(error);
          });
      } else {
        this.dropdown = "dropdown";
      }
    },
    addBucket: function() {
      this.adding = true;
      let self = this;

      if (this.bucketUserName.length == 0) {
        return this.$buefy.toast.open({
          message: "Please enter something for your album name",
          type: "is-danger",
          position: "is-bottom",
          duration: 3000
        });
      } else {
        // request works
        axios
          .post(`http://127.0.0.1:5000/add_bucket_name`, {
            email: this.email,
            bucketName: this.bucketUserName
          })
          .then(function(response) {
            console.log(response);
            return self.$buefy.toast.open({
              message: "Yay your bucket was added",
              type: "is-success",
              position: "is-bottom",
              duration: 3000
            });
          })
          .catch(function(error) {
            console.log(error);
          });
      }
    }
  }
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
.button-parent {
  margin-bottom: 2rem;
}

.control {
  margin-bottom: 1rem;
}
.control1 {
  margin-bottom: 1rem;
  margin-right: 1.2rem;
}

.logout {
  padding: 0 5rem 0 5rem;
}
.private {
  margin-bottom: 1rem;
}
.add-album {
  padding: 1rem 3rem 1rem 3rem;
  margin-left: 1rem;
}

.bucket {
  width: 25%;
  margin-left: 1rem;
}
</style>
