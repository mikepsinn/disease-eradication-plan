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

  // Restore from sessionStorage
  var saved = sessionStorage.getItem("wishonia-chat");
  if (saved) {
    try {
      messages = JSON.parse(saved);
    } catch (_) {}
  }

  // DOM refs
  var fab, panel, msgContainer, input, sendBtn, micBtn;

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

  function searchContent(query) {
    if (!searchIndex || searchIndex.length === 0) return "";

    var queryTokens = tokenize(query);
    if (queryTokens.length === 0) return "";

    var scored = searchIndex.map(function (entry) {
      var titleTokens = tokenize(entry.title || "");
      var sectionTokens = tokenize(entry.section || "");
      var textTokens = tokenize(entry.text || "");

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
      return e.href && e.href.replace(/\.html(#.*)?$/, "").endsWith(currentPath);
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
        var text = (e.text || "").substring(0, 1500);
        if ((e.text || "").length > 1500) text += "...";
        return "### " + label + "\n" + text;
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
      '  <button class="chat-close-btn" aria-label="Close chat">&times;</button>' +
      "</div>" +
      '<div class="chat-messages"></div>' +
      '<div class="chat-input-area">' +
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

    closeBtn.addEventListener("click", togglePanel);
    sendBtn.addEventListener("click", handleSend);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Show mic button if Speech Recognition is available
    if (window.SpeechRecognition || window.webkitSpeechRecognition) {
      micBtn.style.display = "flex";
      micBtn.addEventListener("click", startVoiceInput);
    }

    // Show welcome if no messages
    if (messages.length === 0) {
      showWelcome();
    }
  }

  function showWelcome() {
    var welcome = document.createElement("div");
    welcome.className = "chat-welcome";
    welcome.textContent =
      "I've been watching your planet since 1945. Ask me anything about the book, the 1% treaty, or why you spend more on missiles than medicine.";
    msgContainer.appendChild(welcome);
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

  function appendMessage(role, content, skipSave) {
    // Remove welcome message on first real message
    var welcome = msgContainer.querySelector(".chat-welcome");
    if (welcome) welcome.remove();

    var bubble = document.createElement("div");
    bubble.className = "chat-msg chat-msg-" + role;
    bubble.textContent = content;

    // Add TTS button for assistant messages
    if (role === "assistant" && content) {
      var ttsBtn = document.createElement("button");
      ttsBtn.className = "chat-tts-btn";
      ttsBtn.textContent = "\u{1F50A}";
      ttsBtn.title = "Listen";
      ttsBtn.addEventListener("click", function () {
        playTTS(content, ttsBtn);
      });
      bubble.appendChild(document.createElement("br"));
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

        // Create empty assistant bubble and stream into it
        var bubble = appendMessage("assistant", "");
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

              // Add TTS button now that we have the full text
              var ttsBtn = document.createElement("button");
              ttsBtn.className = "chat-tts-btn";
              ttsBtn.textContent = "\u{1F50A}";
              ttsBtn.title = "Listen";
              ttsBtn.addEventListener("click", function () {
                playTTS(fullText, ttsBtn);
              });
              bubble.appendChild(document.createElement("br"));
              bubble.appendChild(ttsBtn);

              isStreaming = false;
              sendBtn.disabled = false;
              return;
            }

            var chunk = decoder.decode(result.value, { stream: true });
            fullText += chunk;
            // Update bubble text (before the TTS button)
            bubble.firstChild
              ? (bubble.firstChild.textContent = fullText)
              : (bubble.textContent = fullText);
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

  function startVoiceInput() {
    if (recognition) {
      recognition.stop();
      recognition = null;
      micBtn.classList.remove("recording");
      return;
    }

    var SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.classList.add("recording");

    recognition.onresult = function (event) {
      var transcript = event.results[0][0].transcript;
      input.value = transcript;
      micBtn.classList.remove("recording");
      recognition = null;
    };

    recognition.onerror = function () {
      micBtn.classList.remove("recording");
      recognition = null;
    };

    recognition.onend = function () {
      micBtn.classList.remove("recording");
      recognition = null;
    };

    recognition.start();
  }

  // ========================================
  // VOICE OUTPUT (TTS)
  // ========================================

  function playTTS(text, btn) {
    // Check cache
    if (audioCache[text]) {
      var audio = new Audio(audioCache[text]);
      audio.play();
      return;
    }

    btn.classList.add("loading");
    btn.textContent = "\u23F3"; // hourglass

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
        var url = URL.createObjectURL(blob);
        audioCache[text] = url;
        var audio = new Audio(url);
        audio.play();
        btn.textContent = "\u{1F50A}";
        btn.classList.remove("loading");
      })
      .catch(function () {
        btn.textContent = "\u{1F50A}";
        btn.classList.remove("loading");
      });
  }

  // ========================================
  // INIT
  // ========================================

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
