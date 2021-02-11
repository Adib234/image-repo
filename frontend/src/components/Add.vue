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
        <p v-if="dropdownClicked">
          The album you chose and will upload to is
          <strong>{{privateBucket}}</strong>
        </p>

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
              <div v-for="name in userBuckets" :key="name">
                <a v-on:click="setBucket(name)" class="dropdown-item">{{name}}</a>
              </div>
              <!-- <a href="#" class="dropdown-item">wahy</a> -->
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
          <input type="radio" value="Single" v-model="quantity" />
          Single
        </label>
        <label class="radio">
          <input type="radio" value="Bulk" v-model="quantity" />
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
    </div>
  </div>
</template>

<script>
import AWS from "aws-sdk";
import axios from "axios";

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
  name: "Add",
  props: { email: String },

  data() {
    return {
      uploaded: false,
      fileNameGlobal: "",
      imageUrl: "",
      imageDescription: "",
      permissions: "", // public or private
      dropdown: "dropdown",
      adding: false,
      bucketUserName: "", //name of the bucket that the image will be added to, nothing if it's public
      userBuckets: [],
      privateBucket: "", // the private bucket they select from the dropdown
      dropdownClicked: false,
      quantity: "" // single or bulk
    };
  },

  methods: {
    showImage: function() {
      let params =
        this.permissions === "Public"
          ? {
              Bucket: publicBucketName,
              Key: `${publicBucketName}/` + this.fileNameGlobal
            }
          : {
              Bucket: publicBucketName,
              Key: `${this.email}/${this.privateBucket}/` + this.fileNameGlobal
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
          axios
            .post(`http://127.0.0.1:5000/tags`, {
              fileName: self.fileNameGlobal,
              image: base64encode,
              tags: self.imageDescription,
              private: self.permissions === "Private" ? true : false, // if its private, this gets added to the user info in our database
              // so that when they want to search from their private repos they can do so
              email: self.email
            })
            .then(function(response) {
              console.log(response);
            })
            .catch(function(error) {
              console.log(error);
            });
        },
        function(err) {
          console.log(err, err.stack);
        }
      );
    },
    s3upload: function() {
      let self = this;

      var files = document.getElementById("fileUpload").files;

      if (this.quantity === "Single") {
        // single upload
        try {
          if (files) {
            let file = files[0];
            let fileName = file?.name;
            this.fileNameGlobal = fileName;

            if (self.permissions === "Public") {
              let filePath = `${publicBucketName}/` + fileName;

              let upload = s3.upload({
                Bucket: publicBucketName,
                Key: filePath,
                Body: file
              });
              let promise = upload.promise();

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
            } else {
              let filePath = `${self.email}/${self.privateBucket}/` + fileName;

              let upload = s3.upload({
                Bucket: publicBucketName,
                Key: filePath,
                Body: file
              });
              let promise = upload.promise();

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
          }
        } catch (err) {
          return self.$buefy.toast.open({
            message: "Please upload something",
            type: "is-danger",
            position: "is-bottom",
            duration: 3000
          });
        }
      } else if (this.quantity === "Bulk") {
        return 0;
      } else {
        return this.$buefy.toast.open({
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
            var params = {
              Bucket: publicBucketName,
              Key: `${self.email}/${self.bucketUserName}/`
            };
            // when user creates a new account a folder in the bucket is create for them,
            // so they can put there private images if they want to in the future
            // *this works
            s3.putObject(params, function(err, data) {
              if (err) {
                console.log("Error creating the folder: ", err);
              } else {
                console.log(data);
              }
            });
            return self.$buefy.toast.open({
              message: "Yay your bucket was added",
              type: "is-success",
              position: "is-bottom",
              duration: 3000
            });
          })
          .catch(function(error) {
            console.log(error);
            return self.$buefy.toast.open({
              message: "Please do not enter the same bucket name",
              type: "is-danger",
              position: "is-bottom",
              duration: 3000
            });
          });
      }
    },
    setBucket: function(val) {
      this.privateBucket = val;
      this.dropdownClicked = true;
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
