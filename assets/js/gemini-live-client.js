/**
 * GeminiLiveClient - WebSocket client for Gemini Live API
 *
 * Manages a bidirectional audio streaming connection to Gemini.
 * Audio goes in (mic PCM), audio comes out (model PCM). No separate STT/TTS.
 */

// eslint-disable-next-line no-unused-vars
var GeminiLiveClient = (function () {
  "use strict";

  var API_BASE = "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent";

  function GeminiLiveClient(opts) {
    this.apiKey = opts.apiKey;
    this.systemInstruction = opts.systemInstruction || "";
    this.voice = opts.voice || "Kore";
    this.onAudio = opts.onAudio || null;
    this.onText = opts.onText || null;
    this.onInterrupted = opts.onInterrupted || null;
    this.onTurnComplete = opts.onTurnComplete || null;
    this.onReady = opts.onReady || null;
    this.onError = opts.onError || null;
    this.ws = null;
    this._setupDone = false;
  }

  GeminiLiveClient.prototype.connect = function () {
    var self = this;
    return new Promise(function (resolve, reject) {
      var url = API_BASE + "?key=" + encodeURIComponent(self.apiKey);
      self.ws = new WebSocket(url);

      self.ws.onopen = function () {
        self._sendSetup();
      };

      self.ws.onmessage = function (event) {
        var data;
        if (typeof event.data === "string") {
          data = JSON.parse(event.data);
        } else if (event.data instanceof Blob) {
          event.data.text().then(function (text) {
            self._handleMessage(JSON.parse(text));
          });
          return;
        } else {
          return;
        }
        self._handleMessage(data);
      };

      self.ws.onerror = function (err) {
        if (self.onError) self.onError(err);
        reject(err);
      };

      self.ws.onclose = function () {
        self._setupDone = false;
      };

      // Resolve when setup is complete
      var origOnReady = self.onReady;
      self.onReady = function () {
        self._setupDone = true;
        if (origOnReady) origOnReady();
        resolve();
      };
    });
  };

  GeminiLiveClient.prototype._sendSetup = function () {
    var setup = {
      setup: {
        model: "models/gemini-2.5-flash-native-audio-latest",
        generationConfig: {
          responseModalities: ["AUDIO"],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: { voiceName: this.voice },
            },
          },
        },
        systemInstruction: {
          parts: [{ text: this.systemInstruction }],
        },
        realtimeInputConfig: {
          automaticActivityDetection: {
            disabled: false,
            startOfSpeechSensitivity: "START_SENSITIVITY_LOW",
            endOfSpeechSensitivity: "END_SENSITIVITY_LOW",
          },
        },
      },
    };
    this.ws.send(JSON.stringify(setup));
  };

  /**
   * Send raw PCM audio chunk (base64 encoded, 16kHz mono 16-bit)
   */
  GeminiLiveClient.prototype.sendAudio = function (base64Pcm) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN || !this._setupDone) return;
    this.ws.send(
      JSON.stringify({
        realtimeInput: {
          mediaChunks: [{ data: base64Pcm, mimeType: "audio/pcm;rate=16000" }],
        },
      })
    );
  };

  /**
   * Send a text message (typed question while in voice mode)
   */
  GeminiLiveClient.prototype.sendText = function (text) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN || !this._setupDone) return;
    this.ws.send(
      JSON.stringify({
        clientContent: {
          turns: [{ role: "user", parts: [{ text: text }] }],
          turnComplete: true,
        },
      })
    );
  };

  GeminiLiveClient.prototype._handleMessage = function (msg) {
    // Setup complete
    if (msg.setupComplete) {
      if (this.onReady) this.onReady();
      return;
    }

    var sc = msg.serverContent;
    if (!sc) return;

    // Interruption
    if (sc.interrupted) {
      if (this.onInterrupted) this.onInterrupted();
      return;
    }

    // Model audio/text output
    if (sc.modelTurn && sc.modelTurn.parts) {
      for (var i = 0; i < sc.modelTurn.parts.length; i++) {
        var part = sc.modelTurn.parts[i];
        if (part.inlineData && part.inlineData.data) {
          if (this.onAudio) this.onAudio(part.inlineData.data);
        }
        if (part.text) {
          if (this.onText) this.onText(part.text);
        }
      }
    }

    // Turn complete
    if (sc.turnComplete) {
      if (this.onTurnComplete) this.onTurnComplete();
    }
  };

  GeminiLiveClient.prototype.disconnect = function () {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this._setupDone = false;
  };

  GeminiLiveClient.prototype.isConnected = function () {
    return this.ws && this.ws.readyState === WebSocket.OPEN && this._setupDone;
  };

  return GeminiLiveClient;
})();
