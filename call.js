const axios = require("axios");

async function getImagePrediction() {
  try {
    const response = await axios.post("http://127.0.0.1:5000/tags", {
      image: "baboon.png",
    });
    console.log(response.data.tags);
  } catch (e) {
    console.log(e);
  }
}

getImagePrediction();
