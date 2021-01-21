const axios = require("axios");

async function getImagePrediction() {
  try {
    const response = await axios.get("/image-classifier/main.py");
    return response;
  } catch (e) {}
}

getImagePrediction();
