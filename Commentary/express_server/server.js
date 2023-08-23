const express = require("express");
const http = require("http");
const socketIO = require("socket.io");
const fs = require("fs");
const path = require("path");
const player = require("play-sound")((opts = {}));
// const cors = require("cors");
const { spawn } = require("child_process");
const AudioManager = require("./audioManager");

const audiosFolderPath =
  "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary/audios";
const folderPath =
  "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/FinishImg";

const audioManager = new AudioManager("exampleName");
const app = express();
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

const framesFolder = path.join(__dirname, "frames");
if (!fs.existsSync(framesFolder)) {
  fs.mkdirSync(framesFolder);
}
fs.writeFile("boundingBox.txt", "", (err) => {
  if (err) {
    console.error("An error occurred while clearing the file:", err);
    return;
  }
  console.log("File content cleared successfully!");
});
fs.writeFile("userInfo.txt", "", (err) => {
  if (err) {
    console.error("An error occurred while clearing the file:", err);
    return;
  }
  console.log("File content cleared successfully!");
});

let isPlayed = false;
io.on("connection", (socket) => {
  console.log("Server got lil bro");

  socket.on("start-climbing", () => {
    audioManager.playStartAudio();
  });
  socket.on("three-min-left", () => {
    audioManager.playThreeMinAudio();
  });
  socket.on("two-min-left", () => {
    audioManager.playTwoMinAudio();
  });
  socket.on("one-min-left", () => {
    audioManager.playOneMinAudio();
  });
  socket.on("half-min-left", () => {
    audioManager.playHalfMinAudio();
  });
  socket.on("frame", (data) => {
    // console.log("Frame received:", data.image);
    const base64Data = data.image.split(",")[1];
    const buffer = Buffer.from(base64Data, "base64");
    const filename = `frame_${id++}.jpg`;

    fs.writeFile(path.join(framesFolder, filename), buffer, (err) => {
      if (err) {
        console.error("Error writing file:", err);
      } else {
        console.log("File saved:", filename);
      }
    });
  });

  socket.on("bounding-box", (data) => {
    const dataString = JSON.stringify(data);
    console.log(dataString);
    fs.appendFile("boundingBox.txt", dataString + "\n", (err) => {
      if (err) {
        console.error("An error occurred while writing to the file:", err);
        return;
      }
      console.log("Data successfully appended to boundingBox.txt");
    });
  });

  let childProcess = null;
  socket.on("form-value-collected", (data) => {
    const dataString =
      "The contestant's name is " +
      data.name +
      ", age is " +
      data.age +
      ", height is " +
      data.height +
      ", nationality is " +
      data.nationality +
      ", experience is " +
      data.experience +
      ", level is " +
      data.level +
      ", and current level is " +
      data.currLevel +
      ".";

    fs.appendFile("userInfo.txt", dataString + "\n", (err) => {
      if (err) {
        console.error("An error occurred while writing to the file:", err);
        return;
      }
      console.log("Data successfully appended to userInfo.txt" + dataString);
      const cv_python_script_path =
        "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary/ai-commentary.py";
      const activate_and_run_python_script_command = `source /Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary/ai-commentary-system-env/bin/activate && python3 ${cv_python_script_path}`;

      const workingDirectory =
        "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary";
      childProcess = spawn(activate_and_run_python_script_command, {
        shell: true,
        executable: "/bin/bash",
        cwd: workingDirectory,
      });

      childProcess.stderr.on("data", (data) => {
        console.error(`Python script error: ${data}`);
      });

      childProcess.on("exit", (code) => {
        if (code !== 0) {
          console.error(`Python script exited with code ${code}`);
        } else {
          console.log("Python script completed successfully");
        }
      });
    });
  });

  socket.on("play-beep-sound", () => {
    audioManager.playBeepSound()
  });
  socket.on("play-time-up-sound", () => {
    audioManager.playTimeUpSound()
  });
});
fs.watch(folderPath, { recursive: true }, (eventType, filename) => {
  if (filename && !isPlayed) {
    console.log(`File ${filename} has been changed with event ${eventType}`);
    io.emit("finish-detected");
    audioManager.playFinishAudio();
    isPlayed = true;
  }
});

fs.watch(audiosFolderPath, { recursive: true }, (eventType, filename) => {
  fs.readdir(audiosFolderPath, (err, files) => {
    if (err) {
      console.error("Error reading the directory:", err);
      return;
    }
    if (files.length === 9) {
      io.emit("form-values-processed");
      audioManager.playIntroAudio();
      console.log("File num reached!!");
    }
  });
});

server.listen(3000, () =>
  console.log("Server running on http://localhost:3000")
);
