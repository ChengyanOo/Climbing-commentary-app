const express = require("express");
const http = require("http");
const socketIO = require("socket.io");
const fs = require("fs");
const path = require("path");
const player = require("play-sound")((opts = {}));
// const cors = require("cors");
const { spawn } = require("child_process");
const readline = require("readline");
const AudioManager = require("./audioManager");

const app = express();
const audioManager = new AudioManager("exampleName");
const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: true,
  },
});
let id = 1;

app.use(express.static("public"));

let isPlayed = false;
io.on("connection", (socket) => {
  console.log("Mock up server got lil bro");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.on("line", (input) => {
    if (input.trim() === "s") {
      io.emit("form-values-processed");
      console.log('Emitted "form-values-processed" event');
    }
  });
  socket.on("play-beep-sound", () => {
    audioManager.playBeepSound()
  });
  socket.on("play-time-up-sound", () => {
    audioManager.playTimeUpSound()
  });
});


server.listen(3000, () =>
  console.log("Server running on http://localhost:3000")
);
