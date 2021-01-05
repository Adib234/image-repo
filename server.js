const express = require("express");
const mongoose = require("mongoose");
require("dotenv").config({ path: "./variables.env" });

const app = express();

//Database
mongoose
  .connect(
    `mongodb+srv://${process.env.USERNAME}:${process.env.PASSWORD}@cluster0.fbnpy.mongodb.net/api?retryWrites=true&w=majority`,
    {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    }
  )
  .then(() => console.log("Connected to database"))
  .catch((err) => console.log(err));

//Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.listen(process.env.PORT, () =>
  console.log(`Server started on ${process.env.PORT}`)
);

//Controllers
const ParkControl = require("./controller");

//Routes
app.post("/api/park/create", ParkControl.create);
app.post("/api/park/update", ParkControl.update);
app.get("/api/park/retrieve", ParkControl.retrieve);
app.delete("/api/park/delete", ParkControl.delete);
//Start Server
