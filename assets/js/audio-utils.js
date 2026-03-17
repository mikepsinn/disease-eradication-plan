/**
 * AudioCapture + AudioPlayback utilities for Gemini Live voice chat.
 *
 * AudioCapture: getUserMedia -> AudioWorklet at native rate -> resample to 16kHz -> base64 PCM chunks -> callback
 * AudioPlayback: base64 PCM 24kHz -> AudioWorklet -> speakers. Has interrupt() to clear queue.
 */

// eslint-disable-next-line no-unused-vars
var AudioCapture = (function () {
  "use strict";

  function AudioCapture(onChunk, onVolume) {
    this.onChunk = onChunk;
    this.onVolume = onVolume || null; // callback(0-1) for volume level
    this.audioCtx = null;
    this.stream = null;
    this.sourceNode = null;
    this.workletNode = null;
    this._analyser = null;
    this._analyserData = null;
    this._volumeRaf = null;
  }

  /**
   * Downsample from source sample rate to 16kHz
   */
  function downsample(inputBuffer, inputRate, outputRate) {
    if (inputRate === outputRate) return inputBuffer;
    var ratio = inputRate / outputRate;
    var outputLength = Math.round(inputBuffer.length / ratio);
    var output = new Int16Array(outputLength);
    for (var i = 0; i < outputLength; i++) {
      var srcIndex = i * ratio;
      var low = Math.floor(srcIndex);
      var high = Math.min(low + 1, inputBuffer.length - 1);
      var frac = srcIndex - low;
      output[i] = Math.round(inputBuffer[low] * (1 - frac) + inputBuffer[high] * frac);
    }
    return output;
  }

  /**
   * Convert Int16Array to base64
   */
  function int16ToBase64(int16arr) {
    var bytes = new Uint8Array(int16arr.buffer);
    var binary = "";
    for (var i = 0; i < bytes.length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }

  AudioCapture.prototype.start = async function () {
    var self = this;

    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        sampleRate: { ideal: 16000 },
        channelCount: 1,
        echoCancellation: true,
        noiseSuppression: true,
      },
    });

    this.audioCtx = new AudioContext({ sampleRate: this.stream.getAudioTracks()[0].getSettings().sampleRate || 48000 });
    var actualRate = this.audioCtx.sampleRate;

    // Determine worklet script path using quarto offset
    var offset = document.querySelector('meta[name="quarto:offset"]')?.getAttribute("content") || "";
    if (offset && offset.charAt(offset.length - 1) !== "/") offset += "/";
    var workletUrl = offset + "assets/js/audio-worklet-processor.js";

    await this.audioCtx.audioWorklet.addModule(workletUrl);

    this.sourceNode = this.audioCtx.createMediaStreamSource(this.stream);
    this.workletNode = new AudioWorkletNode(this.audioCtx, "mic-processor");

    this.workletNode.port.onmessage = function (e) {
      if (!e.data.pcm16) return;
      var pcm16 = new Int16Array(e.data.pcm16);
      // Downsample to 16kHz if needed
      var resampled = downsample(pcm16, actualRate, 16000);
      var b64 = int16ToBase64(resampled);
      if (self.onChunk) self.onChunk(b64);
    };

    this.sourceNode.connect(this.workletNode);
    // Don't connect worklet to destination (we don't want to hear ourselves)
    this.workletNode.connect(this.audioCtx.destination);

    // Set up AnalyserNode for volume metering
    if (this.onVolume) {
      this._analyser = this.audioCtx.createAnalyser();
      this._analyser.fftSize = 256;
      this._analyserData = new Uint8Array(this._analyser.frequencyBinCount);
      this.sourceNode.connect(this._analyser);
      var analyser = this._analyser;
      var analyserData = this._analyserData;
      var onVol = this.onVolume;
      var rafSelf = this;
      function pollVolume() {
        analyser.getByteFrequencyData(analyserData);
        var sum = 0;
        for (var k = 0; k < analyserData.length; k++) sum += analyserData[k];
        var avg = sum / analyserData.length / 255; // 0-1
        onVol(avg);
        rafSelf._volumeRaf = requestAnimationFrame(pollVolume);
      }
      pollVolume();
    }
  };

  AudioCapture.prototype.stop = function () {
    if (this._volumeRaf) {
      cancelAnimationFrame(this._volumeRaf);
      this._volumeRaf = null;
    }
    if (this._analyser) {
      this._analyser.disconnect();
      this._analyser = null;
    }
    if (this.workletNode) {
      this.workletNode.disconnect();
      this.workletNode = null;
    }
    if (this.sourceNode) {
      this.sourceNode.disconnect();
      this.sourceNode = null;
    }
    if (this.stream) {
      this.stream.getTracks().forEach(function (t) { t.stop(); });
      this.stream = null;
    }
    if (this.audioCtx) {
      this.audioCtx.close();
      this.audioCtx = null;
    }
  };

  return AudioCapture;
})();

// eslint-disable-next-line no-unused-vars
var AudioPlayback = (function () {
  "use strict";

  var PLAYBACK_RATE = 24000;

  function AudioPlayback() {
    this.audioCtx = null;
    this.workletNode = null;
    this._ready = false;
    this._initPromise = null;
  }

  AudioPlayback.prototype.init = async function () {
    if (this._ready) return;
    if (this._initPromise) return this._initPromise;

    var self = this;
    this._initPromise = (async function () {
      self.audioCtx = new AudioContext({ sampleRate: PLAYBACK_RATE });

      var offset = document.querySelector('meta[name="quarto:offset"]')?.getAttribute("content") || "";
      if (offset && offset.charAt(offset.length - 1) !== "/") offset += "/";
      var workletUrl = offset + "assets/js/audio-worklet-processor.js";

      await self.audioCtx.audioWorklet.addModule(workletUrl);
      self.workletNode = new AudioWorkletNode(self.audioCtx, "playback-processor");
      self.workletNode.connect(self.audioCtx.destination);
      self._ready = true;
    })();

    return this._initPromise;
  };

  /**
   * Decode base64 PCM (24kHz 16-bit mono) and queue for playback
   */
  AudioPlayback.prototype.play = function (base64Pcm) {
    if (!this._ready || !this.workletNode) return;

    // Resume AudioContext if suspended (autoplay policy)
    if (this.audioCtx.state === "suspended") {
      this.audioCtx.resume();
    }

    // Decode base64 to Int16
    var binary = atob(base64Pcm);
    var bytes = new Uint8Array(binary.length);
    for (var i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
    var int16 = new Int16Array(bytes.buffer);

    // Convert Int16 to Float32 for AudioWorklet
    var float32 = new Float32Array(int16.length);
    for (var j = 0; j < int16.length; j++) {
      float32[j] = int16[j] / 32768;
    }

    this.workletNode.port.postMessage(
      { samples: float32.buffer },
      [float32.buffer]
    );
  };

  /**
   * Immediately clear all queued audio (for interruptions)
   */
  AudioPlayback.prototype.interrupt = function () {
    if (this.workletNode) {
      this.workletNode.port.postMessage({ cmd: "clear" });
    }
  };

  AudioPlayback.prototype.destroy = function () {
    if (this.workletNode) {
      this.workletNode.disconnect();
      this.workletNode = null;
    }
    if (this.audioCtx) {
      this.audioCtx.close();
      this.audioCtx = null;
    }
    this._ready = false;
    this._initPromise = null;
  };

  return AudioPlayback;
})();
