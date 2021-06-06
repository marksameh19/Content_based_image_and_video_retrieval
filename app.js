const express = require("express");
const app = express();
const fs = require("fs");
const bodyparser = require("body-parser");
const path = require("path");
const { spawn } = require("child_process");
const multer = require("multer");
const { type } = require("os");
let dataFromPython;

let port = 3000;
app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(express.static("images"));
app.use(express.static("uploads"));
app.use(bodyparser.urlencoded({ extended: true }));

const upload = multer({
  dest: path.join(__dirname, "uploads"),
  // you might also want to set some limits: https://github.com/expressjs/multer#limits
});

app.post("/upload", upload.single("img"), (req, res) => {
  const tempPath = req.file.path;
  const targetPath = path.join(__dirname, "./uploads/image.jpg");
  fs.rename(tempPath, targetPath, (err) => {
    const python = spawn("python", [
      "main_cbir.py",
      req.body.algorithm,
      req.body.image_limit,
    ]);
    python.stdout.on("data", (data) => {
      dataFromPython = data.toString();
      console.log(dataFromPython);
      let final_data = dataFromPython
        .split("'")
        .join("")
        .slice(1, -3)
        .split(",");
      res.render("home2.ejs", { images: final_data });
    });
    // if (req.body.algorithm == 3) {
    //   const python = spawn("python", ["hist.py"]);
    //   python.stdout.on("data", (data) => {
    //     dataFromPython = data.toString();
    //     dataFromPython = String(dataFromPython);
    //     let final_data = dataFromPython
    //       .split("'")
    //       .join("")
    //       .slice(1, -3)
    //       .split(",");
    //     res.render("images", { images: final_data });
    //     //res.send(final_data[0]);
    //   });
    // } else res.send("hhhhhhhh");
  });
});

app.post("/upload_video", upload.single("video"), (req, res) => {
  const tempPath = req.file.path;
  const targetPath = path.join(__dirname, "./uploads/video.mp4");
  fs.rename(tempPath, targetPath, (err) => {
    const python = spawn("python", ["main_cbvr.py", req.body.video_limit]);
    python.stdout.on("data", (data) => {
      dataFromPython = data.toString();
      console.log(dataFromPython);
      let final_data = dataFromPython
        .split("'")
        .join("")
        .slice(1, -3)
        .split(",");
      res.render("videos.ejs", { videos: final_data });
    });
  });
});

app.get("/", (req, res) => {
  res.render("index");
});

// fs.readFile("imgav.json", "utf-8", (err, data) => {
//   if (err) {
//     throw err;
//   }
//   // parse JSON object
//   const img_avg = JSON.parse(data.toString());
//   const python = spawn("python", ["color_distance.py", img_avg["imgavg"]]);
//   python.stdout.on("data", (data) => {
//     console.log("test");
//     dataFromPython = data.toString();
//     console.log(dataFromPython);
//   });
// });

app.listen(port, () => {
  console.log("listening on http://localhost:3000");
});

// const python = spawn("python", [
//   "main_cbir.py",
//   req.body.algorithm,
//   req.body.image_limit,
// ]);
// python.stdout.on("data", (data) => {
//   dataFromPython = data.toString();
//   console.log(dataFromPython);
// });
