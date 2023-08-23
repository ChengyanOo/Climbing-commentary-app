const audioFolderPath =
  "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary/audios";
const soundEffectFolderPath =
  "/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/ai-commentary/sound_effects";

const audioMap = new Map([
  ["startAudio", `${audioFolderPath}/audio_0.mp3`],
  ["threeMinAudio", `${audioFolderPath}/audio_1.mp3`],
  ["twoMinAudio", `${audioFolderPath}/audio_2.mp3`],
  ["oneMinAudio", `${audioFolderPath}/audio_3.mp3`],
  ["halfMinAudio", `${audioFolderPath}/audio_4.mp3`],
  ["halfWayAudio", `${audioFolderPath}/audio_5.mp3`],
  ["fallAudio", `${audioFolderPath}/audio_6.mp3`],
  ["finishAudio", `${audioFolderPath}/audio_7.mp3`],
  ["introductionAudio", `${audioFolderPath}/introduction_audio.mp3`],
  ["beepSound", `${soundEffectFolderPath}/beep.mp3`],
  ["timeUpSound", `${soundEffectFolderPath}/timeUp.mp3`]
]);

module.exports = { audioFolderPath, audioMap };
