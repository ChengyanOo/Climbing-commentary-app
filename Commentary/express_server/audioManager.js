const { audioMap } = require("./pathVariables");
const playSound = require("play-sound");

class AudioManager {
  constructor(name) {
    this.name = name;
    this.player = playSound();
    this.currentProcess = null;
    this.isplaying = false;
  }

  _playAudio(audioKey) {
    if (this.currentProcess) {
      this.currentProcess.kill();
      this.currentProcess = null;
      this.isplaying = false;
    }

    if (!this.isplaying) {
      this.currentProcess = this.player.play(audioMap.get(audioKey), (err) => {
        if (err) throw err;
      });
      this.isplaying = true;
    }
  }

  playStartAudio() {
    this._playAudio("startAudio");
  }
  playThreeMinAudio() {
    this._playAudio("threeMinAudio");
  }
  playTwoMinAudio() {
    this._playAudio("twoMinAudio");
  }
  playOneMinAudio() {
    this._playAudio("oneMinAudio");
  }
  playHalfMinAudio() {
    this._playAudio("halfMinAudio");
  }
  playHalfWayAudio() {
    this._playAudio("halfWayAudio");
  }
  playFallAudio() {
    this._playAudio("fallAudio");
  }
  playFinishAudio() {
    this._playAudio("finishAudio");
  }
  enableSound() {
    this.isplaying = false;
  }

  disableSound() {
    this.isplaying = true;
  }
}

module.exports = AudioManager;
