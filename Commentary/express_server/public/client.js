const socket = io.connect("http://localhost:3000");
const video = document.querySelector("#video");
const canvas = document.querySelector("#canvas");
const startBtn = document.querySelector("#start");
const stopBtn = document.querySelector("#stop");
const context = canvas.getContext("2d");
const testButton = document.querySelector("#test");
const label = document.querySelector("#label");
let interval = null;
const fileInput = document.querySelector("#fileInput");
const saveBtn = document.querySelector("#save");
const saveFinishBtn = document.querySelector("#save-finish");


let startX,
  startY,
  dragging = false;

let tempStartX,
  tempStartY,
  tempX,
  tempY = 0;
function captureFrameSendToServer() {
  if (video.paused || video.ended) {
    console.error("Video is not playing");
    return;
  }
  const desiredWidth = 640;
  const aspectRatio = video.videoWidth / video.videoHeight;

  canvas.width = desiredWidth;
  canvas.height = desiredWidth / aspectRatio;

  console.log(canvas.width);
  console.log(canvas.height);
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const frame = canvas.toDataURL("image/jpeg");

  if (frame.startsWith("data:image/jpeg;base64,")) {
    socket.emit("frame", { image: frame });
    console.log({ image: frame });
  } else {
    console.error("Frame data is incorrect:", frame);
  }
}

canvas.addEventListener("mousedown", (e) => {
  const scaleX = canvas.width / canvas.offsetWidth;
  const scaleY = canvas.height / canvas.offsetHeight;

  startX = e.offsetX * scaleX;
  startY = e.offsetY * scaleY;
  dragging = true;
});

canvas.addEventListener("mousemove", (e) => {
  if (dragging) {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const x = e.offsetX;
    const y = e.offsetY;
    context.strokeStyle = "#FF0000"; // red color
    context.lineWidth = 2;
    context.strokeRect(startX, startY, x - startX, y - startY);
    tempStartX = startX;
    tempStartY = startY;
    tempX = x;
    tempY = y;
  }
});

canvas.addEventListener("mouseup", (e) => {
  dragging = false;
  const x = e.offsetX;
  const y = e.offsetY;
  console.log(
    `Selected area from x: ${startX}, y: ${startY} to x: ${x}, y: ${y}`
  );
});

saveBtn.addEventListener("click", (e) => {
  console.log({
    startX: tempStartX,
    startY: tempStartY,
    x: tempX,
    y: tempY,
    finish: false
  });
  socket.emit("bounding-box", {
    startX: tempStartX,
    startY: tempStartY,
    x: tempX,
    y: tempY,
    finish: false
  });
  tempStartX = 0;
  tempStartY = 0;
  tempX = 0;
  tempY = 0;
});

saveFinishBtn.addEventListener("click", (e) => {
  console.log({
    startX: tempStartX,
    startY: tempStartY,
    x: tempX,
    y: tempY,
    finish: true
  });
  socket.emit("bounding-box", {
    startX: tempStartX,
    startY: tempStartY,
    x: tempX,
    y: tempY,
    finish: true
  });
  tempStartX = 0;
  tempStartY = 0;
  tempX = 0;
  tempY = 0;
});

// //using web cam
// navigator.mediaDevices
//   .getUserMedia({ video: true })
//   .then((=stream) => {
//     video.srcObject = stream;
//     video.play();
//   })
//   .catch((error) => {
//     console.error("Error accessing the camera:", error);
//   });

//using file
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const objectURL = URL.createObjectURL(file);
    video.src = objectURL;
    video.play();
  } else {
    console.error("No file selected");
  }
});

startBtn.addEventListener("click", () => {
  label.innerHTML = "Capturing img each 0.5...";
  interval = setInterval(() => {
    captureFrameSendToServer();
  }, 500);
});

stopBtn.addEventListener("click", () => {
  label.innerHTML = "Capturing Stopped.";
  clearInterval(interval);
});

testButton.addEventListener("click", () => {
  label.innerHTML = "Capturing the current frame...";
  captureFrameSendToServer();
});

const input = document.querySelector("#input");
const submitBtn = document.querySelector("#submit");

submitBtn.addEventListener("click", (e) => {
  label.innerHTML = "Sending message to the server...";
  console.log(input.value);
  socket.emit("message", { text: input.value });
  input.value = "";
});

socket.on("connect", () => {
  console.log("Connected to server");
});
