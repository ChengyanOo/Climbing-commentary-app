const express = require("express");
const http = require("http");
const socketIO = require("socket.io");
const fs = require("fs");
const path = require("path");
const cors = require("cors");

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

// Create frames folder if it doesn't exist
const framesFolder = path.join(__dirname, "frames");
if (!fs.existsSync(framesFolder)) {
  fs.mkdirSync(framesFolder);
}

// Clear the content of "boundingBox.txt"
fs.writeFile("boundingBox.txt", "", (err) => {
  if (err) {
    console.error("An error occurred while clearing the file:", err);
    return;
  }
  console.log("File content cleared successfully!");
});

io.on("connection", (socket) => {
  console.log("Server got lil bro");
  socket.on("message", (data) => {
    console.log("Message received:", data);
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
    
    const folderPath = "/Users/tonsonwang/Desktop/Commentary/FinishImg";
    fs.watch(folderPath, { recursive: true }, (eventType, filename) => {
      if (filename) {
        console.log(
          `File ${filename} has been changed with event ${eventType}`
        );
        socket.emit("finish-detected");
      }
    });
  });

  socket.on("bounding-box", (data) => {
    // Convert data to a string if necessary
    const dataString = JSON.stringify(data);

    // Append the data to "boundingBox.txt"
    fs.appendFile("boundingBox.txt", dataString + "\n", (err) => {
      if (err) {
        console.error("An error occurred while writing to the file:", err);
        return;
      }
      console.log("Data successfully appended to boundingBox.txt");
    });
  });
});

server.listen(3000, () =>
  console.log("Server running on http://localhost:3000")
);
