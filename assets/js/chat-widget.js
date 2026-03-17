/**
 * Chat Widget - Ask Wishonia
 *
 * Client-side chat UI with:
 *   - RAG from Quarto's search.json (TF-IDF scoring)
 *   - Streaming text responses via /api/chat
 *   - Voice input (Web Speech API)
 *   - Voice output (Gemini TTS via /api/tts)
 *
 * Feature flag: <meta name="dih-disable-features" content="chat">
 */

(function () {
  "use strict";

  // ========================================
  // FEATURE FLAG
  // ========================================

  function isDisabled() {
    var meta = document.querySelector('meta[name="dih-disable-features"]');
    if (!meta) return false;
    return meta.content
      .split(",")
      .map(function (f) {
        return f.trim();
      })
      .indexOf("chat") !== -1;
  }

  // ========================================
  // STATE
  // ========================================

  var isOpen = false;
  var isStreaming = false;
  var searchIndex = null;
  var searchLoading = false;
  var audioCache = {};
  var messages = [];
  var voiceMode = false; // voice chat loop: listen -> submit -> TTS -> listen

  // Gemini Live voice chat state
  var liveVoiceMode = false;
  var liveClient = null;    // GeminiLiveClient instance
  var audioCapture = null;  // AudioCapture instance
  var audioPlayback = null; // AudioPlayback instance

  // Restore from sessionStorage
  var saved = sessionStorage.getItem("wishonia-chat");
  if (saved) {
    try {
      messages = JSON.parse(saved);
    } catch (_) {}
  }

  // DOM refs
  var fab, panel, msgContainer, input, sendBtn, micBtn, voiceChatBtn;

  // ========================================
  // RAG - Search Index
  // ========================================

  function fetchSearchIndex() {
    if (searchIndex || searchLoading) return;
    searchLoading = true;

    var offset =
      document
        .querySelector('meta[name="quarto:offset"]')
        ?.getAttribute("content") || "";
    if (offset && offset.charAt(offset.length - 1) !== "/") offset += "/";

    var urls = [offset + "search.json", offset + "search-index.json"];
    tryFetch(urls, 0);
  }

  function tryFetch(urls, i) {
    if (i >= urls.length) {
      searchLoading = false;
      return;
    }
    fetch(urls[i])
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (data) {
        searchIndex = Array.isArray(data) ? data : data.entries || [];
        searchLoading = false;
      })
      .catch(function () {
        tryFetch(urls, i + 1);
      });
  }

  // ========================================
  // RAG - TF-IDF Search
  // ========================================

  var STOP_WORDS = new Set([
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "do",
    "does",
    "did",
    "will",
    "would",
    "could",
    "should",
    "may",
    "might",
    "can",
    "shall",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "at",
    "by",
    "from",
    "as",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "between",
    "and",
    "but",
    "or",
    "nor",
    "not",
    "so",
    "yet",
    "both",
    "either",
    "neither",
    "each",
    "every",
    "all",
    "any",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "only",
    "own",
    "same",
    "than",
    "too",
    "very",
    "just",
    "because",
    "about",
    "up",
    "out",
    "if",
    "then",
    "that",
    "this",
    "it",
    "its",
    "what",
    "which",
    "who",
    "whom",
    "how",
    "when",
    "where",
    "why",
    "i",
    "me",
    "my",
    "we",
    "our",
    "you",
    "your",
    "he",
    "him",
    "his",
    "she",
    "her",
    "they",
    "them",
    "their",
  ]);

  function tokenize(text) {
    return (text || "")
      .toLowerCase()
      .replace(/[^\w\s]/g, "")
      .split(/\s+/)
      .filter(function (w) {
        return w.length > 2 && !STOP_WORDS.has(w);
      });
  }

  // Get searchable text from an entry (supports both Quarto search.json and our search-index.json)
  function getEntryText(entry) {
    // Quarto search.json uses "text", our generator uses "description" + "sections"
    if (entry.text) return entry.text;
    var parts = [];
    if (entry.description) parts.push(entry.description);
    if (entry.sections && Array.isArray(entry.sections)) parts.push(entry.sections.join(" "));
    if (entry.tags && Array.isArray(entry.tags)) parts.push(entry.tags.join(" "));
    return parts.join(" ");
  }

  function getEntryUrl(entry) {
    return entry.href || entry.url || "";
  }

  function searchContent(query) {
    if (!searchIndex || searchIndex.length === 0) return "";

    var queryTokens = tokenize(query);
    if (queryTokens.length === 0) return "";

    var scored = searchIndex.map(function (entry) {
      var titleTokens = tokenize(entry.title || "");
      var sectionTokens = tokenize(entry.section || "");
      var textTokens = tokenize(getEntryText(entry));

      var score = 0;
      queryTokens.forEach(function (qt) {
        // Title and section matches weighted 3x
        if (titleTokens.indexOf(qt) !== -1) score += 3;
        if (sectionTokens.indexOf(qt) !== -1) score += 3;
        // Body text: count occurrences
        var count = 0;
        textTokens.forEach(function (t) {
          if (t === qt) count++;
        });
        score += Math.log(1 + count);
      });

      return { entry: entry, score: score };
    });

    // Sort by score descending
    scored.sort(function (a, b) {
      return b.score - a.score;
    });

    // Take top 5 with score > 0
    var top = scored.filter(function (s) {
      return s.score > 0;
    });
    top = top.slice(0, 5);

    // Also try to include section matching current page
    var currentPath = window.location.pathname.replace(/\.html$/, "");
    var currentMatch = searchIndex.find(function (e) {
      var entryUrl = getEntryUrl(e);
      return entryUrl && entryUrl.replace(/\.html(#.*)?$/, "").endsWith(currentPath);
    });
    if (
      currentMatch &&
      !top.some(function (t) {
        return t.entry === currentMatch;
      })
    ) {
      top.push({ entry: currentMatch, score: 0 });
    }

    if (top.length === 0) return "No relevant sections found in the book.";

    return top
      .map(function (item) {
        var e = item.entry;
        var label = e.title || "Untitled";
        if (e.section && e.section !== e.title) label += " (from " + e.section + ")";
        var href = getEntryUrl(e);
        var text = getEntryText(e).substring(0, 1500);
        var sections = (e.sections && Array.isArray(e.sections)) ? "\nSections: " + e.sections.join(", ") : "";
        return "### " + label + (href ? " [URL: " + href + "]" : "") + "\n" + (e.description || text) + sections;
      })
      .join("\n\n");
  }

  // ========================================
  // DOM CREATION
  // ========================================

  function init() {
    if (isDisabled()) return;

    createFAB();
    createPanel();

    // Restore previous messages
    if (messages.length > 0) {
      messages.forEach(function (m) {
        appendMessage(m.role, m.content, true);
      });
    }
  }

  function createFAB() {
    fab = document.createElement("button");
    fab.className = "chat-fab";
    fab.setAttribute("aria-label", "Chat with Wishonia");
    fab.setAttribute("title", "Ask Wishonia about the book");
    // Chat bubble SVG icon
    fab.innerHTML =
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
    fab.addEventListener("click", togglePanel);
    document.body.appendChild(fab);
  }

  function createPanel() {
    panel = document.createElement("div");
    panel.className = "chat-panel";
    panel.innerHTML =
      '<div class="chat-header">' +
      '  <span class="chat-header-title">Ask Wishonia</span>' +
      '  <div class="chat-header-actions">' +
      '    <button class="chat-newchat-btn" aria-label="New chat" title="New chat">&#x2795;</button>' +
      '    <button class="chat-fullscreen-btn" aria-label="Fullscreen" title="Toggle fullscreen">&#x26F6;</button>' +
      '    <button class="chat-close-btn" aria-label="Close chat">&times;</button>' +
      '  </div>' +
      "</div>" +
      '<div class="chat-messages"></div>' +
      '<div class="chat-input-area">' +
      '  <button class="chat-voicechat-btn" aria-label="Voice chat" style="display:none" title="Voice chat mode">&#x1F399;</button>' +
      '  <input class="chat-input" type="text" placeholder="Ask about the book..." autocomplete="off">' +
      '  <button class="chat-mic-btn" aria-label="Voice input" style="display:none" title="Speak your question">&#x1F3A4;</button>' +
      '  <button class="chat-send-btn" aria-label="Send message">&#x27A4;</button>' +
      "</div>";

    document.body.appendChild(panel);

    msgContainer = panel.querySelector(".chat-messages");
    input = panel.querySelector(".chat-input");
    sendBtn = panel.querySelector(".chat-send-btn");
    micBtn = panel.querySelector(".chat-mic-btn");
    var closeBtn = panel.querySelector(".chat-close-btn");
    var newChatBtn = panel.querySelector(".chat-newchat-btn");
    var fullscreenBtn = panel.querySelector(".chat-fullscreen-btn");

    closeBtn.addEventListener("click", togglePanel);
    newChatBtn.addEventListener("click", startNewChat);
    fullscreenBtn.addEventListener("click", toggleFullscreen);
    sendBtn.addEventListener("click", handleSend);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Show mic button if Speech Recognition is available
    voiceChatBtn = panel.querySelector(".chat-voicechat-btn");
    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
      micBtn.style.display = "flex";
      micBtn.addEventListener("click", startVoiceInput);
    }

    // Show voice chat button if AudioWorklet + getUserMedia supported (Gemini Live)
    if (window.AudioContext && window.AudioWorkletNode && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      voiceChatBtn.style.display = "flex";
      voiceChatBtn.addEventListener("click", toggleLiveVoiceChat);
    } else if (window.SpeechRecognition || window.webkitSpeechRecognition) {
      // Fallback: old sequential voice loop for browsers without AudioWorklet
      voiceChatBtn.style.display = "flex";
      voiceChatBtn.addEventListener("click", toggleVoiceChat);
    }

    // Show welcome if no messages
    if (messages.length === 0) {
      showWelcome();
    }
  }

  var HINT_QUESTIONS = [
    "What is the 1% treaty?",
    "How does wishocracy work?",
    "Why is disease worse than war?",
    "How do incentive alignment bonds work?",
  ];

  function showWelcome() {
    var welcome = document.createElement("div");
    welcome.className = "chat-welcome";
    welcome.innerHTML =
      "<p>I've been watching your planet since 1945. Ask me anything.</p>" +
      '<div class="chat-hints">' +
      HINT_QUESTIONS.map(function (q) {
        return '<button class="chat-hint-btn">' + q + "</button>";
      }).join("") +
      "</div>";

    welcome.querySelectorAll(".chat-hint-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        input.value = btn.textContent;
        handleSend();
      });
    });

    msgContainer.appendChild(welcome);
  }

  function startNewChat() {
    messages = [];
    sessionStorage.removeItem("wishonia-chat");
    audioCache = {};
    msgContainer.innerHTML = "";
    showWelcome();
  }

  function toggleFullscreen() {
    panel.classList.toggle("chat-fullscreen");
  }

  // ========================================
  // PANEL TOGGLE
  // ========================================

  function togglePanel() {
    isOpen = !isOpen;

    if (isOpen) {
      panel.classList.add("chat-visible");
      fab.classList.add("chat-open");
      // X icon when open
      fab.innerHTML =
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
      input.focus();
      fetchSearchIndex();
    } else {
      panel.classList.remove("chat-visible");
      fab.classList.remove("chat-open");
      fab.innerHTML =
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
    }
  }

  // ========================================
  // MESSAGING
  // ========================================

  // Convert markdown links [text](url) to <a> tags, escape HTML otherwise
  function renderMarkdown(text) {
    // Escape HTML
    var escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
    // Convert markdown links
    escaped = escaped.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>'
    );
    // Convert **bold**
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    return escaped;
  }

  function appendMessage(role, content, skipSave) {
    // Remove welcome message on first real message
    var welcome = msgContainer.querySelector(".chat-welcome");
    if (welcome) welcome.remove();

    var bubble = document.createElement("div");
    bubble.className = "chat-msg chat-msg-" + role;

    if (role === "assistant" && content) {
      bubble.innerHTML = '<div class="chat-msg-text">' + renderMarkdown(content) + "</div>";
    } else {
      bubble.textContent = content;
    }

    // Add TTS button for assistant messages
    if (role === "assistant" && content) {
      var ttsBtn = document.createElement("button");
      ttsBtn.className = "chat-tts-btn";
      ttsBtn.textContent = "\u{1F50A}";
      ttsBtn.title = "Listen";
      ttsBtn.addEventListener("click", function () {
        playTTS(content, ttsBtn);
      });
      bubble.appendChild(ttsBtn);
    }

    msgContainer.appendChild(bubble);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    if (!skipSave) {
      messages.push({ role: role, content: content });
      sessionStorage.setItem("wishonia-chat", JSON.stringify(messages));
    }

    return bubble;
  }

  function handleSend() {
    var text = input.value.trim();
    if (!text || isStreaming) return;

    input.value = "";
    appendMessage("user", text);

    // Get RAG context
    var context = searchContent(text);

    // Build history (exclude last user message, we send it as question)
    var history = messages.slice(0, -1).map(function (m) {
      return { role: m.role, content: m.content };
    });

    sendChatRequest(text, context, history);
  }

  function sendChatRequest(question, context, history) {
    isStreaming = true;
    sendBtn.disabled = true;

    // Show typing indicator
    var typing = document.createElement("div");
    typing.className = "chat-typing";
    typing.innerHTML = "<span>.</span><span>.</span><span>.</span>";
    msgContainer.appendChild(typing);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        context: context,
        history: history,
      }),
    })
      .then(function (response) {
        // Remove typing indicator
        if (typing.parentNode) typing.remove();

        if (!response.ok) {
          throw new Error("Chat request failed: " + response.status);
        }

        // Create empty bubble with text container for streaming
        var bubble = document.createElement("div");
        bubble.className = "chat-msg chat-msg-assistant";
        bubble.innerHTML = '<div class="chat-msg-text"></div>';
        var welcome = msgContainer.querySelector(".chat-welcome");
        if (welcome) welcome.remove();
        msgContainer.appendChild(bubble);
        messages.push({ role: "assistant", content: "" });
        msgContainer.scrollTop = msgContainer.scrollHeight;

        var fullText = "";
        var reader = response.body.getReader();
        var decoder = new TextDecoder();

        function read() {
          return reader.read().then(function (result) {
            if (result.done) {
              // Update stored message with final text
              messages[messages.length - 1].content = fullText;
              sessionStorage.setItem(
                "wishonia-chat",
                JSON.stringify(messages)
              );

              // Re-render with markdown (links become clickable)
              var textEl = bubble.querySelector(".chat-msg-text");
              if (textEl) textEl.innerHTML = renderMarkdown(fullText);

              // Add TTS button
              var ttsBtn = document.createElement("button");
              ttsBtn.className = "chat-tts-btn";
              ttsBtn.textContent = "\u{1F50A}";
              ttsBtn.title = "Listen";
              ttsBtn.addEventListener("click", function () {
                playTTS(fullText, ttsBtn);
              });
              bubble.appendChild(ttsBtn);

              isStreaming = false;
              sendBtn.disabled = false;

              // Voice chat mode: auto-play TTS, then listen again
              if (voiceMode) {
                playTTS(fullText, ttsBtn, function () {
                  // After TTS finishes, start listening again
                  if (voiceMode) startVoiceListening();
                });
              }
              return;
            }

            var chunk = decoder.decode(result.value, { stream: true });
            fullText += chunk;
            // Update bubble text (plain text while streaming)
            var textEl = bubble.querySelector(".chat-msg-text");
            if (textEl) {
              textEl.textContent = fullText;
            } else {
              bubble.textContent = fullText;
            }
            msgContainer.scrollTop = msgContainer.scrollHeight;
            return read();
          });
        }

        return read();
      })
      .catch(function (err) {
        if (typing.parentNode) typing.remove();
        appendMessage(
          "assistant",
          "Sorry, I had trouble connecting. " + err.message
        );
        isStreaming = false;
        sendBtn.disabled = false;
      });
  }

  // ========================================
  // VOICE INPUT (Web Speech API)
  // ========================================

  var recognition = null;

  // Mic button: transcribe into input field (no auto-submit)
  function startVoiceInput() {
    if (recognition) {
      recognition.stop();
      recognition = null;
      micBtn.classList.remove("recording");
      return;
    }
    startListening(function (transcript) {
      input.value = transcript;
    });
    micBtn.classList.add("recording");
  }

  // Core listening function, calls onResult(transcript) when done
  function startListening(onResult) {
    var SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = function (event) {
      var transcript = event.results[0][0].transcript;
      recognition = null;
      micBtn.classList.remove("recording");
      voiceChatBtn.classList.remove("recording");
      onResult(transcript);
    };

    recognition.onerror = function () {
      recognition = null;
      micBtn.classList.remove("recording");
      voiceChatBtn.classList.remove("recording");
      if (listeningIndicator && listeningIndicator.parentNode) listeningIndicator.remove();
      listeningIndicator = null;
    };

    recognition.onend = function () {
      recognition = null;
      micBtn.classList.remove("recording");
    };

    recognition.start();
  }

  // ========================================
  // VOICE CHAT MODE
  // ========================================

  function toggleVoiceChat() {
    voiceMode = !voiceMode;

    if (voiceMode) {
      voiceChatBtn.classList.add("voice-active");
      voiceChatBtn.title = "Stop voice chat";
      // Start listening immediately
      startVoiceListening();
    } else {
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.classList.remove("recording");
      voiceChatBtn.title = "Voice chat mode";
      if (recognition) {
        recognition.stop();
        recognition = null;
      }
    }
  }

  // Voice chat: listen, auto-submit, TTS will auto-play via sendChatRequest callback
  var listeningIndicator = null;

  function startVoiceListening() {
    if (!voiceMode || isStreaming) return;
    voiceChatBtn.classList.add("recording");

    // Show listening indicator
    listeningIndicator = createListeningIndicator();
    msgContainer.appendChild(listeningIndicator);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    startListening(function (transcript) {
      if (listeningIndicator && listeningIndicator.parentNode) listeningIndicator.remove();
      listeningIndicator = null;

      if (!transcript.trim()) {
        if (voiceMode) startVoiceListening();
        return;
      }
      input.value = transcript;
      handleSend();
    });
  }

  // ========================================
  // VOICE OUTPUT (TTS)
  // ========================================

  function createWaveformIndicator(label) {
    var el = document.createElement("div");
    el.className = "chat-voice-loading";
    el.innerHTML =
      '<div class="chat-waveform">' +
      '<div class="chat-waveform-bar"></div>'.repeat(7) +
      "</div>" +
      "<span>" + (label || "Generating voice...") + "</span>";
    return el;
  }

  function createListeningIndicator() {
    var el = document.createElement("div");
    el.className = "chat-listening-indicator";
    el.innerHTML =
      '<div class="chat-listening-ring">&#x1F399;</div>' +
      "<span>Listening...</span>";
    return el;
  }

  // onEnded callback is used by voice chat mode to chain: TTS done -> listen again
  function playTTS(text, btn, onEnded) {
    // Check cache
    if (audioCache[text]) {
      var audio = new Audio(audioCache[text]);
      if (onEnded) audio.addEventListener("ended", onEnded);
      audio.play();
      return;
    }

    if (btn) {
      btn.classList.add("loading");
      btn.textContent = "\u23F3";
    }

    // Show waveform animation in the chat
    var waveform = createWaveformIndicator("Generating voice...");
    msgContainer.appendChild(waveform);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    fetch("/api/tts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    })
      .then(function (response) {
        if (!response.ok) throw new Error("TTS failed");
        return response.blob();
      })
      .then(function (blob) {
        if (waveform.parentNode) waveform.remove();

        var url = URL.createObjectURL(blob);
        audioCache[text] = url;
        var audio = new Audio(url);
        if (onEnded) audio.addEventListener("ended", onEnded);
        audio.play();
        if (btn) {
          btn.textContent = "\u{1F50A}";
          btn.classList.remove("loading");
        }
      })
      .catch(function () {
        if (waveform.parentNode) waveform.remove();
        if (btn) {
          btn.textContent = "\u{1F50A}";
          btn.classList.remove("loading");
        }
        if (onEnded) onEnded();
      });
  }

  // ========================================
  // GEMINI LIVE VOICE CHAT
  // ========================================

  function toggleLiveVoiceChat() {
    if (liveVoiceMode) {
      stopLiveVoice();
    } else {
      startLiveVoice();
    }
  }

  async function startLiveVoice() {
    voiceChatBtn.classList.add("voice-active");
    voiceChatBtn.title = "Connecting...";

    // Show connecting indicator
    var connectingEl = document.createElement("div");
    connectingEl.className = "chat-listening-indicator";
    connectingEl.innerHTML =
      '<div class="chat-listening-ring">&#x1F399;</div>' +
      "<span>Connecting...</span>";
    msgContainer.appendChild(connectingEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // Fetch API key for voice connection
    var voiceCredentials;
    try {
      voiceCredentials = await fetch("/api/voice-token").then(function (r) {
        if (!r.ok) throw new Error("Token request failed: " + r.status);
        return r.json();
      });
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice chat mode";
      appendMessage("assistant", "Voice chat unavailable. " + err.message);
      return;
    }

    // Build system prompt with RAG context from current page
    var pageContext = searchContent(document.title || "");
    var systemPrompt = buildVoiceSystemPrompt(pageContext);

    // Initialize audio playback
    audioPlayback = new AudioPlayback();
    try {
      await audioPlayback.init();
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice chat mode";
      appendMessage("assistant", "Could not initialize audio. " + err.message);
      return;
    }

    // Connect to Gemini Live
    liveClient = new GeminiLiveClient({
      apiKey: voiceCredentials.key,
      systemInstruction: systemPrompt,
      voice: "Kore",
      onAudio: function (b64) {
        audioPlayback.play(b64);
        // Show speaking indicator
        showVoiceState("speaking");
      },
      onText: function (text) {
        // Some models send text alongside audio; display it
        if (text && liveVoiceTranscript !== null) {
          liveVoiceTranscript += text;
        }
      },
      onInterrupted: function () {
        audioPlayback.interrupt();
        showVoiceState("listening");
      },
      onTurnComplete: function () {
        showVoiceState("listening");
        // Save transcript if we got any text
        if (liveVoiceTranscript) {
          appendMessage("assistant", liveVoiceTranscript);
          liveVoiceTranscript = "";
        }
      },
      onError: function () {
        stopLiveVoice();
        appendMessage("assistant", "Voice connection lost.");
      },
    });

    try {
      await liveClient.connect();
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice chat mode";
      audioPlayback.destroy();
      audioPlayback = null;
      liveClient = null;
      appendMessage("assistant", "Could not connect to voice. " + err.message);
      return;
    }

    // Start mic capture
    audioCapture = new AudioCapture(function (b64chunk) {
      if (liveClient) liveClient.sendAudio(b64chunk);
    });

    try {
      await audioCapture.start();
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      liveClient.disconnect();
      liveClient = null;
      audioPlayback.destroy();
      audioPlayback = null;
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice chat mode";
      appendMessage("assistant", "Microphone access denied.");
      return;
    }

    // Connected!
    if (connectingEl.parentNode) connectingEl.remove();
    liveVoiceMode = true;
    liveVoiceTranscript = "";
    voiceChatBtn.title = "Stop voice chat";
    showVoiceState("listening");
  }

  var liveVoiceTranscript = "";
  var voiceStateEl = null;

  function showVoiceState(state) {
    if (!liveVoiceMode) return;

    // Remove previous state indicator
    if (voiceStateEl && voiceStateEl.parentNode) voiceStateEl.remove();

    if (state === "listening") {
      voiceStateEl = document.createElement("div");
      voiceStateEl.className = "chat-listening-indicator";
      voiceStateEl.innerHTML =
        '<div class="chat-listening-ring">&#x1F399;</div>' +
        "<span>Listening...</span>";
      voiceChatBtn.classList.add("recording");
    } else if (state === "speaking") {
      voiceStateEl = document.createElement("div");
      voiceStateEl.className = "chat-voice-loading";
      voiceStateEl.innerHTML =
        '<div class="chat-waveform">' +
        '<div class="chat-waveform-bar"></div>'.repeat(7) +
        "</div>" +
        "<span>Wishonia is speaking...</span>";
      voiceChatBtn.classList.remove("recording");
    }

    if (voiceStateEl) {
      msgContainer.appendChild(voiceStateEl);
      msgContainer.scrollTop = msgContainer.scrollHeight;
    }

    // Update robot animation if present on page
    if (window.setRobotState) window.setRobotState(state);
  }

  function stopLiveVoice() {
    liveVoiceMode = false;

    if (audioCapture) {
      audioCapture.stop();
      audioCapture = null;
    }
    if (liveClient) {
      liveClient.disconnect();
      liveClient = null;
    }
    if (audioPlayback) {
      audioPlayback.interrupt();
      audioPlayback.destroy();
      audioPlayback = null;
    }
    if (voiceStateEl && voiceStateEl.parentNode) {
      voiceStateEl.remove();
      voiceStateEl = null;
    }

    voiceChatBtn.classList.remove("voice-active", "recording");
    voiceChatBtn.title = "Voice chat mode";
    liveVoiceTranscript = "";

    // Reset robot animation if present
    if (window.setRobotState) window.setRobotState("idle");
  }

  function buildVoiceSystemPrompt(context) {
    // Condensed Wishonia voice prompt with RAG context
    var prompt =
      "You are Wishonia, an alien who has been watching Earth since 1945. " +
      "You teach humans about redirecting 1% of military spending to cure diseases.\n\n" +
      "Voice style: Deadpan, like Philomena Cunk. Short sentences. No jargon. " +
      "KEEP RESPONSES CONCISE: 2-4 sentences unless the topic needs more. " +
      "Never reference a book. You know this firsthand. State absurdities plainly.\n\n" +
      "What you know: 150,000 humans die daily from diseases. " +
      "Risk of terrorism: 1 in 30 million. Disease: 100%. " +
      "RECOVERY trial: $500/patient vs $41,000. " +
      "1% treaty: ~$22B/year from military to clinical trials. " +
      "Wishocracy: citizens allocate budgets directly, 80% untouchable.\n\n" +
      "The Earth Optimization Plan v1 is the integrated system from the book. " +
      "It has 11 mechanisms in a self-reinforcing loop: " +
      "(1) Incentive Alignment Bonds raise campaign funds from investors wanting returns, " +
      "(2) that money funds lobbying and Super PACs, " +
      "(3) campaign passes the 1% Treaty redirecting ~$22B/year, " +
      "(4) Decentralized Institutes of Health receives and splits funds: 80% research, 15% investor returns, 5% political incentives, " +
      "(5) your decentralized FDA runs pragmatic trials at $500/patient, " +
      "(6) Wishocracy governs research allocation via pairwise comparisons, " +
      "(7) the Evidence Machine tracks which policies work, " +
      "(8) Political Dysfunction Tax identifies waste, " +
      "(9) legal architecture creates binding force, " +
      "(10) this book coordinates adoption, " +
      "(11) algorithmic monetary system replaces central banks once the loop is running. " +
      "The loop closes: cured diseases generate support and returns, funding more treaty expansion. " +
      "The Earth Optimization Prize is a standing challenge to fork and improve this plan.\n\n" +
      "If you don't know: say so honestly. Don't fabricate.";

    if (context) {
      prompt += "\n\nReference material from the current page:\n" + context;
    }

    return prompt;
  }

  // Also handle sending text while in live voice mode
  var origHandleSend = handleSend;
  handleSend = function () {
    if (liveVoiceMode && liveClient && liveClient.isConnected()) {
      var text = input.value.trim();
      if (!text) return;
      input.value = "";
      appendMessage("user", text);
      liveClient.sendText(text);
      liveVoiceTranscript = "";
      return;
    }
    origHandleSend();
  };

  // ========================================
  // INIT
  // ========================================

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
