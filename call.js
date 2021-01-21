const axios = require("axios");

async function getImagePrediction() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/tags");
    console.log(response.data.tags);
  } catch (e) {
    console.log(e);
  }
}

getImagePrediction();
