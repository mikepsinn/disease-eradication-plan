/**
 * Talk Widget - Ask Wishonia
 *
 * Client-side talk UI with:
 *   - RAG from search-index.json (TF-IDF scoring)
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
  // API BASE (set via <meta name="dih-api-base" content="https://transmit.warondisease.org">)
  // ========================================

  var apiBaseMeta = document.querySelector('meta[name="dih-api-base"]');
  var API_BASE = apiBaseMeta ? apiBaseMeta.content.replace(/\/$/, '') : '';
  var MANUAL_BASE = "https://manual.warondisease.org";

  function isLocalhostDebugUi() {
    var hostname = (window.location && window.location.hostname || "").toLowerCase();
    return hostname === "localhost" || hostname === "127.0.0.1" || hostname === "[::1]" || /(^|\.)localhost$/.test(hostname);
  }

  var SHOW_VOICE_RAG_DEBUG = isLocalhostDebugUi();

  // ========================================
  // STATE
  // ========================================

  var isOpen = false;
  var isStreaming = false;
  var searchIndex = null;
  var searchLoading = false;
  var audioCache = {};
  var messages = [];
  var voiceMode = false; // voice mode loop: listen -> submit -> TTS -> listen

  // Gemini Live voice mode state
  var liveVoiceMode = false;
  var liveClient = null;    // GeminiLiveClient instance
  var audioCapture = null;  // AudioCapture instance
  var audioPlayback = null; // AudioPlayback instance
  var pendingTurnComplete = false; // true while waiting for audio to drain after turnComplete
  var drainSafetyTimer = null;     // safety timeout so mouth never gets stuck
  var mouthRafId = null;           // requestAnimationFrame handle for analyser-driven lipsync
  var localRecognition = null; // Local SpeechRecognition for user speech in voice mode
  var voiceSystemPrompt = "";  // Cached system prompt for RAG debug display
  var voiceIdleTimer = null;   // auto-stop voice mode after 60s of silence
  var VOICE_IDLE_MS = 60000;

  // Rich content state
  var lastSearchResults = [];
  var ragCache = {};
  var imageIndex = null;
  var imageIndexLoading = false;
  var katexLoaded = false;
  var katexLoading = false;
  var chartJsLoaded = false;
  var chartJsLoading = false;
  var mermaidLoaded = false;
  var mermaidLoading = false;
  var abortController = null;
  var userScrolledUp = false;

  // Restore persisted state
  messages = ChatStorage.loadMessages();
  ragCache = ChatStorage.loadRagCache();

  // DOM refs
  var fab, panel, msgContainer, input, sendBtn, voiceChatBtn;

  // ========================================
  // RAG - Search Index
  // ========================================

  function fetchSearchIndex() {
    if (searchIndex || searchLoading) return;
    searchLoading = true;

    fetch("/assets/json/search-index.json")
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        var ct = r.headers.get("content-type") || "";
        if (ct.indexOf("json") === -1) throw new Error("Expected JSON, got " + ct + " (proxy misconfigured?)");
        return r.json();
      })
      .then(function (data) {
        searchIndex = Array.isArray(data) ? data : data.entries || [];
        searchLoading = false;
        console.log("[VOICE-RAG] Search index loaded:", searchIndex.length, "entries");
      })
      .catch(function (err) {
        console.error("[VOICE-RAG] Failed to load search index:", err.message);
        searchLoading = false;
      });
  }

  // ========================================
  // SYSTEM PROMPT (for RAG debug display)
  // ========================================

  function fetchSystemPrompt() {
    var url = API_BASE + "/api/system-prompt";
    fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        if (data.prompt) {
          voiceSystemPrompt = data.prompt;
          console.log("[VOICE-RAG] System prompt loaded:", voiceSystemPrompt.length, "chars");
        } else {
          throw new Error("No prompt field in response");
        }
      })
      .catch(function (err) {
        console.error("[VOICE-RAG] Failed to load system prompt:", err.message);
      });
  }

  // ========================================
  // IMAGE INDEX
  // ========================================

  function fetchImageIndex() {
    if (imageIndex || imageIndexLoading) return;

    // Try cached index first
    var cached = ChatStorage.loadImageIndex();
    if (cached && cached.length > 0) {
      imageIndex = cached;
      imageIndex.forEach(function (img) {
        if (!img._keywords) {
          img._keywords = tokenize(
            (img.keywords || []).join(" ") + " " +
            (img.title || "") + " " + (img.description || "")
          );
        }
      });
      return;
    }

    imageIndexLoading = true;
    fetch("/assets/image-index.json")
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      })
      .then(function (data) {
        var images = data.images || [];
        imageIndex = images.filter(function (img) {
          var type = (img.imageType || "").toLowerCase();
          return type !== "icon" && type !== "og" && (img.width || 0) >= 400;
        });
        imageIndex.forEach(function (img) {
          img._keywords = tokenize(
            (img.keywords || []).join(" ") +
              " " +
              (img.title || "") +
              " " +
              (img.description || "")
          );
        });
        ChatStorage.saveImageIndex(imageIndex);
        imageIndexLoading = false;
      })
      .catch(function () {
        imageIndexLoading = false;
      });
  }

  function findRelevantImage(query, ragResults) {
    if (!imageIndex || imageIndex.length === 0) return null;

    var queryTokens = tokenize(query);
    if (queryTokens.length === 0) return null;

    var ragSlugs = (ragResults || [])
      .map(function (r) {
        return (r.url || "")
          .replace(/\.html.*$/, "")
          .replace(/^.*\//, "");
      })
      .filter(Boolean);

    var best = null;
    var bestScore = 0;

    imageIndex.forEach(function (img) {
      var score = 0;
      var path = (img.path || "").toLowerCase();

      ragSlugs.forEach(function (slug) {
        if (path.indexOf(slug.toLowerCase()) !== -1) score += 5;
      });

      queryTokens.forEach(function (qt) {
        if (img._keywords.indexOf(qt) !== -1) score += 2;
      });

      var type = (img.imageType || "").toLowerCase();
      if (type === "infographic" || type === "chart") score += 1;

      if (score > bestScore) {
        bestScore = score;
        best = img;
      }
    });

    return bestScore >= 4 ? best : null;
  }

  function findTopImageCandidates(query, ragResults, count) {
    if (!imageIndex || imageIndex.length === 0) return [];

    var queryTokens = tokenize(query);
    if (queryTokens.length === 0) return [];

    var ragSlugs = (ragResults || [])
      .map(function (r) {
        return (r.url || "")
          .replace(/\.html.*$/, "")
          .replace(/^.*\//, "");
      })
      .filter(Boolean);

    var scored = [];
    imageIndex.forEach(function (img) {
      var score = 0;
      var path = (img.path || "").toLowerCase();

      ragSlugs.forEach(function (slug) {
        if (path.indexOf(slug.toLowerCase()) !== -1) score += 5;
      });

      queryTokens.forEach(function (qt) {
        if (img._keywords.indexOf(qt) !== -1) score += 2;
      });

      var type = (img.imageType || "").toLowerCase();
      if (type === "infographic" || type === "chart") score += 1;

      if (score >= 2) {
        scored.push({ path: img.path, title: img.title || "", description: img.description || "", score: score });
      }
    });

    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, count || 3);
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

  // Correct common STT misrecognitions of domain-specific terms
  var TRANSCRIPT_CORRECTIONS = [
    [/\b(optometran|optimetron|optimitran|opt a metron|opt i metron|optimatron)\b/gi, "Optimitron"],
    [/\b(op democracy|optimo cracy|opt democracy|opt a mocracy|optim ocracy)\b/gi, "Optimocracy"],
    [/\b(wish own ya|wishon ya|wish on ya|we shown ya|wish own ia|wisha nia)\b/gi, "Wishonia"],
    [/\b(wish ocracy|wish ah cracy|wisho cracy)\b/gi, "Wishocracy"],
    [/\b(d f d a|d\.f\.d\.a\.?)\b/gi, "DFDA"],
    [/\b(i a b|i\.a\.b\.?)\b/gi, "IAB"],
    [/\b(o b g|o\.b\.g\.?)\b/gi, "OBG"],
    [/\b(o p g|o\.p\.g\.?)\b/gi, "OPG"],
    [/\b(dolly|daily)(?=\s+adjusted|\s+life|\s+year)/gi, "DALY"],
    [/\b(collie|quality)(?=[\s-]+adjusted\s+life)/gi, "QALY"],
    [/\bone percent treaty\b/gi, "1% Treaty"],
  ];

  function correctTranscript(text) {
    var corrected = text;
    for (var i = 0; i < TRANSCRIPT_CORRECTIONS.length; i++) {
      corrected = corrected.replace(TRANSCRIPT_CORRECTIONS[i][0], TRANSCRIPT_CORRECTIONS[i][1]);
    }
    return corrected;
  }

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

  // Extract the most relevant snippets from text around query token matches
  function extractSnippets(fullText, queryTokens, maxChars) {
    if (fullText.length <= maxChars) return fullText;

    var WINDOW = 200; // chars around each match
    var lower = fullText.toLowerCase();
    var positions = [];

    // Find all positions where query tokens appear
    queryTokens.forEach(function (qt) {
      var start = 0;
      while (start < lower.length) {
        var idx = lower.indexOf(qt, start);
        if (idx === -1) break;
        positions.push(idx);
        start = idx + qt.length;
      }
    });

    if (positions.length === 0) return fullText.substring(0, maxChars) + "...";

    // Sort and deduplicate positions, create windows
    positions.sort(function (a, b) { return a - b; });
    var windows = [];
    positions.forEach(function (pos) {
      var winStart = Math.max(0, pos - WINDOW);
      var winEnd = Math.min(fullText.length, pos + WINDOW);
      // Merge with previous window if overlapping
      if (windows.length > 0 && winStart <= windows[windows.length - 1].end) {
        windows[windows.length - 1].end = Math.max(windows[windows.length - 1].end, winEnd);
      } else {
        windows.push({ start: winStart, end: winEnd });
      }
    });

    // Always include the first ~300 chars for context (intro/description)
    var intro = fullText.substring(0, 300);
    var snippets = [intro];
    var totalLen = intro.length;

    windows.forEach(function (w) {
      if (totalLen >= maxChars) return;
      // Skip if overlaps with intro
      if (w.start < 300) {
        w.start = 300;
        if (w.start >= w.end) return;
      }
      var snippet = fullText.substring(w.start, w.end);
      // Trim to word boundaries
      var firstSpace = snippet.indexOf(" ");
      if (firstSpace > 0 && firstSpace < 20) snippet = snippet.substring(firstSpace + 1);
      var lastSpace = snippet.lastIndexOf(" ");
      if (lastSpace > snippet.length - 20) snippet = snippet.substring(0, lastSpace);
      snippets.push("..." + snippet);
      totalLen += snippet.length + 3;
    });

    return snippets.join("\n");
  }

  // Expand query with synonyms/related terms for better recall
  var QUERY_EXPANSIONS = {
    get: ["earn", "receive", "reward", "bonus", "referral", "incentive"],
    pay: ["earn", "revenue", "return", "compensation", "bonus"],
    money: ["fund", "investment", "return", "profit", "revenue", "bond"],
    vote: ["voter", "voting", "campaign", "politician", "senator", "election"],
    cure: ["treatment", "therapy", "drug", "medicine", "clinical", "trial"],
    disease: ["illness", "health", "medical", "patient", "daly"],
    cost: ["price", "expense", "budget", "spending", "daly", "effectiveness"],
    work: ["mechanism", "function", "operate", "process", "architecture"],
    corrupt: ["corruption", "waste", "fraud", "transparency"],
    spend: ["spending", "budget", "military", "allocation"],
    invest: ["investor", "investment", "bond", "return", "profit"],
    save: ["prevent", "avert", "death", "daly", "lives"],
    optimitron: ["policy", "generator", "budget", "optimal"],
    optimocracy: ["governance", "optimitron", "policy"],
    wishocracy: ["allocation", "funding", "voting", "rappa"],
    dfda: ["fda", "decentralized", "regulatory", "trial"],
  };

  function expandQueryTokens(tokens) {
    var expanded = [];
    tokens.forEach(function (t) {
      expanded.push({ token: t, weight: 1 });
      if (QUERY_EXPANSIONS[t]) {
        QUERY_EXPANSIONS[t].forEach(function (syn) {
          if (!tokens.some(function (x) { return x === syn; }) &&
              !expanded.some(function (x) { return x.token === syn; })) {
            expanded.push({ token: syn, weight: 0.5 });
          }
        });
      }
    });
    return expanded;
  }

  function searchContent(query, maxResults, maxChars) {
    maxResults = maxResults || 8;
    maxChars = maxChars || 6000;
    if (!searchIndex || searchIndex.length === 0) return "";

    query = correctTranscript(query);
    var queryTokens = tokenize(query);
    if (queryTokens.length === 0) return "";

    var expandedTokens = expandQueryTokens(queryTokens);

    var scored = searchIndex.map(function (entry) {
      var titleTokens = tokenize(entry.title || "");
      var sectionTokens = tokenize(entry.section || "");
      var textTokens = tokenize(getEntryText(entry));

      var score = 0;
      expandedTokens.forEach(function (item) {
        var qt = item.token;
        var w = item.weight;
        // Title and section matches weighted 3x
        if (titleTokens.indexOf(qt) !== -1) score += 3 * w;
        if (sectionTokens.indexOf(qt) !== -1) score += 3 * w;
        // Body text: count occurrences
        var count = 0;
        textTokens.forEach(function (t) {
          if (t === qt) count++;
        });
        score += Math.log(1 + count) * w;
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
    top = top.slice(0, maxResults);

    // Populate lastSearchResults for source links
    lastSearchResults = top.slice(0, 5).map(function (item) {
      var e = item.entry;
      return {
        title: e.title || "Untitled",
        section: e.section || "",
        url: getEntryUrl(e),
        score: item.score,
      };
    });

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
        var fullText = getEntryText(e);
        // Extract relevant snippets around query matches instead of blind first-N-chars
        var text = extractSnippets(fullText, queryTokens, maxChars);
        var sections = (e.sections && Array.isArray(e.sections)) ? "\nSections: " + e.sections.join(", ") : "";
        return "### " + label + "\n" + (e.description || "") + "\n" + text + sections + (href ? "\nSource: " + href : "");
      })
      .join("\n\n");
  }

  // ========================================
  // DOM CREATION
  // ========================================

  function init() {
    if (isDisabled()) return;

    // Pre-load search index and image index. System prompt is only needed for localhost RAG debug UI.
    fetchSearchIndex();
    fetchImageIndex();
    if (SHOW_VOICE_RAG_DEBUG) fetchSystemPrompt();

    createFAB();
    createPanel();

    // Restore previous messages with all enrichments
    if (messages.length > 0) {
      messages.forEach(function (m) {
        var bubble = appendMessage(m.role, m.content, true);
        if (bubble && m.role === "assistant") {
          if (m.sourceLinks) renderSourcePills(bubble, m.sourceLinks);
          if (m.relevantImage) renderRelevantImage(bubble, m.relevantImage.path, m.relevantImage.title);
        }
        if (m.visuals) {
          var card = renderVisualCard(m.visuals);
          if (card) msgContainer.appendChild(card);
        }
      });
    }
  }

  function createFAB() {
    fab = document.createElement("button");
    fab.className = "chat-fab";
    fab.setAttribute("aria-label", "Talk with Wishonia");
    fab.setAttribute("title", "Talk to Wishonia about the book");
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
      '  <span class="chat-header-title">Argue with Wishonia</span>' +
      '  <div class="chat-header-actions">' +
      '    <button class="chat-newchat-btn" aria-label="New talk" title="New talk">&#x2795;</button>' +
      '    <button class="chat-fullscreen-btn" aria-label="Open full talk" title="Open full talk">&#x26F6;</button>' +
      '    <button class="chat-close-btn" aria-label="Close talk">&times;</button>' +
      '  </div>' +
      "</div>" +
      '<div class="chat-messages"></div>' +
      '<div class="chat-input-area">' +
      '  <textarea class="chat-input" rows="1" placeholder="Talk about the book..."></textarea>' +
      '  <button class="chat-stop-btn" aria-label="Stop generating" title="Stop generating">&#x25A0;</button>' +
      '  <button class="chat-voicechat-btn" aria-label="Voice mode" style="display:none" title="Voice mode">&#x1F3A4;</button>' +
      '  <button class="chat-send-btn" aria-label="Send message">&#x27A4;</button>' +
      "</div>";

    document.body.appendChild(panel);

    msgContainer = panel.querySelector(".chat-messages");
    input = panel.querySelector(".chat-input");
    sendBtn = panel.querySelector(".chat-send-btn");
    var closeBtn = panel.querySelector(".chat-close-btn");
    var newChatBtn = panel.querySelector(".chat-newchat-btn");
    var fullscreenBtn = panel.querySelector(".chat-fullscreen-btn");

    var stopBtn = panel.querySelector(".chat-stop-btn");

    closeBtn.addEventListener("click", togglePanel);
    newChatBtn.addEventListener("click", startNewChat);
    fullscreenBtn.addEventListener("click", toggleFullscreen);
    sendBtn.addEventListener("click", handleSend);
    stopBtn.addEventListener("click", abortStreaming);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Auto-grow textarea
    input.addEventListener("input", function () {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 120) + "px";
    });

    // Scroll-to-bottom button
    var scrollBtn = document.createElement("button");
    scrollBtn.className = "chat-scroll-bottom";
    scrollBtn.innerHTML = "&#x2193;";
    scrollBtn.title = "Scroll to bottom";
    scrollBtn.addEventListener("click", function () {
      userScrolledUp = false;
      scrollBtn.style.display = "none";
      msgContainer.scrollTop = msgContainer.scrollHeight;
    });
    panel.appendChild(scrollBtn);

    msgContainer.addEventListener("scroll", function () {
      var atBottom =
        msgContainer.scrollHeight - msgContainer.scrollTop - msgContainer.clientHeight < 50;
      userScrolledUp = !atBottom;
      scrollBtn.style.display = userScrolledUp ? "flex" : "none";
    });

    voiceChatBtn = panel.querySelector(".chat-voicechat-btn");

    // Show voice button if AudioWorklet + getUserMedia supported (Gemini Live)
    if (window.AudioContext && window.AudioWorkletNode && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      voiceChatBtn.style.display = "flex";
      if (API_BASE && !API_BASE.match(/warondisease\.org/)) {
        // External embed: redirect to hosted voice chat
        voiceChatBtn.title = "Open voice chat";
        voiceChatBtn.addEventListener("click", function () {
          window.open("https://transmit.warondisease.org", "_blank");
        });
      } else {
        voiceChatBtn.addEventListener("click", toggleLiveVoiceChat);
      }
    } else if (window.SpeechRecognition || window.webkitSpeechRecognition) {
      // Fallback: sequential voice loop for browsers without AudioWorklet
      voiceChatBtn.style.display = "flex";
      if (API_BASE && !API_BASE.match(/warondisease\.org/)) {
        voiceChatBtn.title = "Open voice chat";
        voiceChatBtn.addEventListener("click", function () {
          window.open("https://transmit.warondisease.org", "_blank");
        });
      } else {
        voiceChatBtn.addEventListener("click", toggleVoiceChat);
      }
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
    ChatStorage.clearAll();
    audioCache = {};
    ragCache = {};
    lastSearchResults = [];
    stopCurrentAudio();
    if (isStreaming) abortStreaming();
    isStreaming = false;
    sendBtn.disabled = false;
    showStreamingUI(false);
    // Stop live voice chat if active
    if (liveVoiceMode) stopLiveVoice();
    // Stop sequential voice mode if active
    if (voiceMode) {
      voiceMode = false;
      voiceChatBtn.classList.remove("voice-active", "recording");
      voiceChatBtn.title = "Voice mode";
      if (recognition) {
        recognition.stop();
        recognition = null;
      }
    }
    msgContainer.innerHTML = "";
    showWelcome();
  }

  function toggleFullscreen() {
    var offset =
      document
        .querySelector('meta[name="quarto:offset"]')
        ?.getAttribute("content") || "";
    if (offset && offset.charAt(offset.length - 1) !== "/") offset += "/";
    window.location.href = offset + "talk.html";
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

  // Render markdown to HTML with code blocks, LaTeX, headers, lists, etc.
  function renderMarkdown(text) {
    var placeholders = [];
    function ph(html) {
      var id = "\x00PH" + placeholders.length + "\x00";
      placeholders.push(html);
      return id;
    }

    // 1. Extract fenced code blocks
    text = text.replace(/```(\w*)\n?([\s\S]*?)```/g, function (_, lang, code) {
      var escaped =
        code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return ph('<pre class="chat-codeblock"><code>' + escaped + "</code></pre>");
    });

    // 2. Extract inline code
    text = text.replace(/`([^`]+)`/g, function (_, code) {
      var escaped =
        code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return ph('<code class="chat-inline-code">' + escaped + "</code>");
    });

    // 3. Extract display LaTeX ($$...$$)
    text = text.replace(/\$\$([\s\S]*?)\$\$/g, function (_, tex) {
      return ph(renderLatex(tex.trim(), true));
    });

    // 4. Extract inline LaTeX ($...$) - require backslash command or multi-letter math identifiers
    // Skip dollar amounts ($500, $83.3T) and short text fragments
    text = text.replace(/\$([^$]+?)\$/g, function (match, tex) {
      // Must contain a backslash command (e.g. \frac, \times) or be a known LaTeX pattern
      if (!/\\[a-zA-Z]/.test(tex)) return match;
      return ph(renderLatex(tex, false));
    });

    // 5. HTML escape
    var escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // 6. Headers
    escaped = escaped.replace(/^#### (.+)$/gm, '<div class="chat-h4">$1</div>');
    escaped = escaped.replace(
      /^###? (.+)$/gm,
      '<div class="chat-h3">$1</div>'
    );

    // 7. Blockquotes
    escaped = escaped.replace(
      /^&gt; (.+)$/gm,
      '<div class="chat-blockquote">$1</div>'
    );

    // 8. Bullet lists: consecutive lines starting with "- " or "* "
    escaped = escaped.replace(/((?:^|\n)[-*] [^\n]+)+/g, function (block) {
      var items = block
        .trim()
        .split("\n")
        .map(function (line) {
          return "<li>" + line.replace(/^[-*] /, "") + "</li>";
        })
        .join("");
      return '<ul class="chat-list">' + items + "</ul>";
    });

    // 9. Numbered lists: consecutive lines starting with "1. " etc.
    escaped = escaped.replace(/((?:^|\n)\d+\. [^\n]+)+/g, function (block) {
      var items = block
        .trim()
        .split("\n")
        .map(function (line) {
          return "<li>" + line.replace(/^\d+\. /, "") + "</li>";
        })
        .join("");
      return '<ol class="chat-list">' + items + "</ol>";
    });

    // 10. Bold
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // 11. Italic (single *)
    escaped = escaped.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // 12. Links
    escaped = escaped.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>'
    );

    // 13. Paragraphs
    escaped = escaped.replace(/\n\n+/g, "</p><p>");
    escaped = escaped.replace(/\n/g, "<br>");

    // 14. Re-insert placeholders
    for (var i = 0; i < placeholders.length; i++) {
      escaped = escaped.replace("\x00PH" + i + "\x00", placeholders[i]);
    }

    return "<p>" + escaped + "</p>";
  }

  // LaTeX rendering (KaTeX lazy-loaded)
  function renderLatex(tex, display) {
    if (typeof katex !== "undefined") {
      try {
        return katex.renderToString(tex, {
          displayMode: display,
          strict: false,
          throwOnError: false,
        });
      } catch (_) {}
    }
    var cls = display
      ? "chat-latex-pending chat-latex-display"
      : "chat-latex-pending";
    return (
      '<span class="' +
      cls +
      '" data-tex="' +
      tex.replace(/"/g, "&quot;") +
      '">' +
      (display ? "$$" + tex + "$$" : "$" + tex + "$") +
      "</span>"
    );
  }

  var katexCallbacks = [];
  function loadKatex(callback) {
    if (katexLoaded) {
      if (callback) callback();
      return;
    }
    if (callback) katexCallbacks.push(callback);
    if (katexLoading) return;
    katexLoading = true;

    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css";
    document.head.appendChild(link);

    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js";
    script.onload = function () {
      katexLoaded = true;
      katexLoading = false;
      renderPendingLatex();
      var cbs = katexCallbacks.splice(0);
      for (var i = 0; i < cbs.length; i++) cbs[i]();
    };
    document.head.appendChild(script);
  }

  function renderPendingLatex() {
    if (typeof katex === "undefined") return;
    var pending = document.querySelectorAll(".chat-latex-pending");
    for (var i = 0; i < pending.length; i++) {
      var el = pending[i];
      var tex = el.getAttribute("data-tex");
      var display = el.classList.contains("chat-latex-display");
      try {
        el.innerHTML = katex.renderToString(tex, {
          displayMode: display,
          throwOnError: false,
          strict: false,
        });
        el.classList.remove("chat-latex-pending");
      } catch (_) {}
    }
  }

  // ========================================
  // CDN lazy-loaders for Chart.js and Mermaid
  // ========================================

  var chartJsCallbacks = [];
  function loadChartJs(callback) {
    if (chartJsLoaded) {
      if (callback) callback();
      return;
    }
    if (callback) chartJsCallbacks.push(callback);
    if (chartJsLoading) return;
    chartJsLoading = true;

    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js";
    script.onload = function () {
      chartJsLoaded = true;
      chartJsLoading = false;
      var cbs = chartJsCallbacks.splice(0);
      for (var i = 0; i < cbs.length; i++) cbs[i]();
    };
    script.onerror = function () {
      chartJsLoading = false;
    };
    document.head.appendChild(script);
  }

  var mermaidCallbacks = [];
  function loadMermaid(callback) {
    if (mermaidLoaded) {
      if (callback) callback();
      return;
    }
    if (callback) mermaidCallbacks.push(callback);
    if (mermaidLoading) return;
    mermaidLoading = true;

    var script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js";
    script.onload = function () {
      mermaidLoaded = true;
      mermaidLoading = false;
      window.mermaid.initialize({
        startOnLoad: false,
        theme: "base",
        themeVariables: {
          primaryColor: "#2a4a2a",
          primaryTextColor: "#33ff33",
          primaryBorderColor: "#33ff33",
          secondaryColor: "#1a1a2e",
          secondaryTextColor: "#00ccff",
          secondaryBorderColor: "#00ccff",
          tertiaryColor: "#3a1a3a",
          tertiaryTextColor: "#ff66ff",
          tertiaryBorderColor: "#ff66ff",
          lineColor: "#33ff33",
          textColor: "#33ff33",
          mainBkg: "#0a0a1a",
          nodeBorder: "#33ff33",
          clusterBkg: "#1a1a2e",
          titleColor: "#00ccff",
          edgeLabelBackground: "#0a0a1a",
          nodeTextColor: "#33ff33",
          fontFamily: "monospace",
          fontSize: "13px",
        },
      });
      var cbs = mermaidCallbacks.splice(0);
      for (var i = 0; i < cbs.length; i++) cbs[i]();
    };
    script.onerror = function () {
      mermaidLoading = false;
    };
    document.head.appendChild(script);
  }

  // ========================================
  // Visual Supplements (parallel request)
  // ========================================

  function fetchVisuals(question, context, imageOptions) {
    console.log("[VISUALS] fetching for:", question.substring(0, 50));
    return fetch(API_BASE + "/api/visuals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        context: context,
        imageOptions: imageOptions || [],
      }),
    })
      .then(function (response) {
        console.log("[VISUALS] response status:", response.status);
        if (!response.ok) return null;
        return response.json();
      })
      .then(function (data) {
        if (data) {
          var fields = Object.keys(data).filter(function (k) { return data[k] !== null; });
          console.log("[VISUALS] populated fields:", fields.join(", ") || "(none)");
        } else {
          console.log("[VISUALS] null response");
        }
        return data;
      })
      .catch(function (err) {
        console.error("[VISUALS] error:", err);
        return null;
      });
  }

  function escapeHtml(text) {
    return (text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderVisualCard(visuals) {
    if (!visuals) return null;

    var hasContent =
      visuals.keyFigure ||
      visuals.latex ||
      visuals.chartConfig ||
      visuals.table ||
      visuals.mermaid ||
      (visuals.sourceLinks && visuals.sourceLinks.length > 0) ||
      visuals.image;

    if (!hasContent) return null;

    var card = document.createElement("div");
    card.className = "chat-visual-card";

    // Key Figure
    if (visuals.keyFigure) {
      var fig = document.createElement("div");
      fig.className = "chat-key-figure";
      fig.innerHTML =
        '<div class="chat-key-figure-value">' + escapeHtml(visuals.keyFigure.value) + "</div>" +
        '<div class="chat-key-figure-label">' + escapeHtml(visuals.keyFigure.label) + "</div>" +
        (visuals.keyFigure.context
          ? '<div class="chat-key-figure-context">' + escapeHtml(visuals.keyFigure.context) + "</div>"
          : "");
      card.appendChild(fig);
    }

    // LaTeX
    if (visuals.latex) {
      var latexEl = document.createElement("div");
      latexEl.className = "chat-visual-latex";
      latexEl.innerHTML = renderLatex(visuals.latex, true);
      card.appendChild(latexEl);
      if (latexEl.querySelector(".chat-latex-pending")) {
        loadKatex();
      }
    }

    // Chart
    if (visuals.chartConfig) {
      var chartContainer = document.createElement("div");
      chartContainer.className = "chat-visual-chart";
      var canvas = document.createElement("canvas");
      chartContainer.appendChild(canvas);
      card.appendChild(chartContainer);

      var chartCfg = visuals.chartConfig;
      loadChartJs(function () {
        if (typeof Chart !== "undefined") {
          new Chart(canvas, {
            type: chartCfg.type,
            data: chartCfg.data,
            options: Object.assign(
              {
                responsive: true,
                maintainAspectRatio: true,
                color: "#ececec",
                plugins: {
                  legend: {
                    labels: { font: { size: 11 }, color: "#C6CBF5" },
                  },
                },
                scales: chartCfg.type === "pie" || chartCfg.type === "doughnut" ? {} : {
                  x: { ticks: { color: "#999" }, grid: { color: "rgba(255,255,255,0.06)" } },
                  y: { ticks: { color: "#999" }, grid: { color: "rgba(255,255,255,0.06)" } },
                },
              },
              chartCfg.options || {}
            ),
          });
        }
      });
    }

    // Table
    if (visuals.table && visuals.table.headers && visuals.table.rows) {
      var table = document.createElement("table");
      table.className = "chat-visual-table";
      var thead = document.createElement("thead");
      var headerRow = document.createElement("tr");
      visuals.table.headers.forEach(function (h) {
        var th = document.createElement("th");
        th.textContent = h;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);

      var tbody = document.createElement("tbody");
      visuals.table.rows.forEach(function (row) {
        var tr = document.createElement("tr");
        row.forEach(function (cell) {
          var td = document.createElement("td");
          td.textContent = cell;
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      card.appendChild(table);
    }

    // Mermaid
    if (visuals.mermaid) {
      var mermaidContainer = document.createElement("div");
      mermaidContainer.className = "chat-visual-mermaid";
      var mermaidSrc = visuals.mermaid;
      mermaidContainer.textContent = mermaidSrc;
      card.appendChild(mermaidContainer);

      var mermaidId = "mermaid-" + Date.now();
      loadMermaid(function () {
        if (window.mermaid) {
          window.mermaid.render(mermaidId, mermaidSrc).then(function (result) {
            mermaidContainer.innerHTML = result.svg;
          }).catch(function () {
            // Leave text source as fallback
          });
        }
      });
    }

    // Source Links
    if (visuals.sourceLinks && visuals.sourceLinks.length > 0) {
      var sourcesDiv = document.createElement("div");
      sourcesDiv.className = "chat-sources";
      visuals.sourceLinks.forEach(function (link) {
        var a = document.createElement("a");
        a.className = "chat-source-pill";
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = link.title;
        sourcesDiv.appendChild(a);
      });
      card.appendChild(sourcesDiv);
    }

    // Image
    if (visuals.image) {
      var imgContainer = document.createElement("div");
      imgContainer.className = "chat-image-container";
      var img = document.createElement("img");
      img.className = "chat-image-thumb";
      img.src = MANUAL_BASE + "/" + visuals.image;
      img.alt = "";
      img.loading = "lazy";
      img.addEventListener("click", function () {
        showLightbox(MANUAL_BASE + "/" + visuals.image, "");
      });
      imgContainer.appendChild(img);
      card.appendChild(imgContainer);
    }

    return card;
  }

  function showVisualLoading(bubble) {
    var shimmer = document.createElement("div");
    shimmer.className = "chat-visual-loading";
    shimmer.setAttribute("data-visual-loading", "true");
    bubble.appendChild(shimmer);
    return shimmer;
  }

  function removeVisualLoading(bubble) {
    var shimmer = bubble.querySelector("[data-visual-loading]");
    if (shimmer && shimmer.parentNode) shimmer.remove();
  }

  // Extract source links from model output + RAG results, return HTML pills
  // Extract source link data (serialisable array of {title, url})
  function extractSourceLinksData(fullText, ragResults) {
    var links = [];
    var seen = {};
    var BASE_URL = "https://manual.warondisease.org/knowledge";

    function normalizeSourceUrl(rawUrl) {
      var u = rawUrl;
      u = u.replace(/\.html$/, "");
      if (u.charAt(0) === "/" || (u.indexOf("http") !== 0 && u.indexOf(".") !== -1)) {
        u = BASE_URL + (u.charAt(0) === "/" ? "" : "/") + u;
      }
      return u;
    }

    var readMoreRegex = /Read more:\s*\[([^\]]+)\]\(([^)]+)\)/g;
    var match;
    while ((match = readMoreRegex.exec(fullText)) !== null) {
      var url = normalizeSourceUrl(match[2]);
      if (!seen[url]) {
        links.push({ title: match[1], url: url });
        seen[url] = true;
      }
    }

    (ragResults || []).forEach(function (r) {
      if (links.length >= 3) return;
      var rUrl = r.url || "";
      if (!rUrl) return;
      rUrl = normalizeSourceUrl(rUrl);
      if (!seen[rUrl]) {
        links.push({ title: r.title || r.section || "Source", url: rUrl });
        seen[rUrl] = true;
      }
    });

    return links;
  }

  // Render source pills into a parent element
  function renderSourcePills(parent, links) {
    if (!links || links.length === 0) return;
    var html = '<div class="chat-sources">';
    links.forEach(function (link) {
      html +=
        '<a class="chat-source-pill" href="' +
        link.url +
        '" target="_blank" rel="noopener">' +
        link.title +
        "</a>";
    });
    html += "</div>";
    var el = document.createElement("div");
    el.innerHTML = html;
    parent.appendChild(el.firstChild);
  }

  // Render a relevant image thumbnail into a parent element
  function renderRelevantImage(parent, path, title) {
    var imgEl = document.createElement("div");
    imgEl.className = "chat-image-container";
    var imgTag = document.createElement("img");
    imgTag.className = "chat-image-thumb";
    imgTag.src = MANUAL_BASE + "/" + path;
    imgTag.alt = title;
    imgTag.loading = "lazy";
    imgTag.addEventListener("click", function () {
      showLightbox(MANUAL_BASE + "/" + path, title);
    });
    imgEl.appendChild(imgTag);
    parent.appendChild(imgEl);
  }

  // Lightbox overlay for images
  function showLightbox(src, alt) {
    var overlay = document.createElement("div");
    overlay.className = "chat-lightbox";
    overlay.innerHTML =
      '<img src="' +
      src +
      '" alt="' +
      (alt || "").replace(/"/g, "&quot;") +
      '">';
    overlay.addEventListener("click", function () {
      overlay.remove();
    });
    document.body.appendChild(overlay);
  }

  // Smart scroll: only auto-scroll if user hasn't scrolled up
  function scrollToBottom(force) {
    if (!force && userScrolledUp) return;
    msgContainer.scrollTop = msgContainer.scrollHeight;
  }

  // Thinking indicator with orbiting rings and rotating quips
  var THINKING_QUIPS = [
    "Consulting my notes on your species...",
    "Translating from Wishonian to English...",
    "Searching for the polite way to say this...",
    "Did you know? You spend 604x more on weapons than testing medicines.",
    "The 1% Treaty: redirect 1% of military budgets to clinical trials.",
    "Your destructive economy is 11.5% of GDP. The Soviet Union collapsed at 15%.",
    "Incentive Alignment Bonds: investors fund cures, get paid when diseases drop.",
    "Wishocracy: citizens pick priorities, 80% untouchable for science.",
    "The Invisible Graveyard: 10 million die yearly from diseases with known solutions.",
    "The plan caps corruption at 20% (transparent) so 80% actually reaches patients.",
    "Comparing to 340 other planets (you rank 312th)...",
  ];

  /**
   * Build a collapsible <details> showing what was sent to Gemini Live:
   * system prompt, user statement, and RAG context -- all markdown-rendered.
   */
  function buildRagDetailsElement(opts) {
    var charCount = (opts.systemPrompt || "").length + (opts.transcript || "").length + (opts.ragContext || "").length;
    var details = document.createElement("details");
    details.className = "chat-thinking";
    details.style.cssText = "font-size:12px;margin:4px 0;";
    var summary = document.createElement("summary");
    summary.textContent = opts.ragContext
      ? "\uD83D\uDCDA Sent " + charCount + " chars to Gemini Live"
      : "\u26A0\uFE0F No RAG context sent" + (opts.indexSize ? " (search index: " + opts.indexSize + " entries)" : "");
    details.appendChild(summary);

    var content = document.createElement("div");
    content.className = "chat-thinking-text";
    content.style.cssText = "max-height:400px;overflow-y:auto;";

    if (opts.systemPrompt) {
      content.innerHTML += '<strong style="display:block;margin:8px 0 4px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:4px;">\uD83E\uDD16 System Prompt</strong>';
      content.innerHTML += '<div class="chat-msg-text">' + renderMarkdown(opts.systemPrompt) + "</div>";
    }
    if (opts.transcript) {
      content.innerHTML += '<strong style="display:block;margin:8px 0 4px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:4px;">\uD83D\uDDE3\uFE0F User</strong>';
      content.innerHTML += '<div class="chat-msg-text">' + renderMarkdown(opts.transcript) + "</div>";
    }
    content.innerHTML += '<strong style="display:block;margin:8px 0 4px;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:4px;">\uD83D\uDCDA RAG Context</strong>';
    content.innerHTML += '<div class="chat-msg-text">' + renderMarkdown(opts.ragContext || "(none)") + "</div>";

    details.appendChild(content);
    return details;
  }

  /**
   * Search RAG, send combined context to Gemini Live, and show collapsible debug bubble.
   * Shared by both the local-transcription debounce path and the native onInputTranscript path.
   */
  function sendRagToGemini(transcript) {
    var ragContext = searchContent(transcript, 5, 2000);
    console.log("[VOICE-RAG] searchContent:", ragContext ? ragContext.length + " chars" : "EMPTY", "index:", searchIndex ? searchIndex.length : "NULL");
    if (!liveClient || !liveClient.isConnected()) return { ragContext: ragContext };

    var combined = "The user just asked: \"" + transcript + "\"\n\n";
    if (ragContext) {
      combined += "Your Earth Optimization Protocol notes:\n" + ragContext + "\n\n";
      combined += "Answer the user's question using your own knowledge above.";
    } else {
      combined += "Answer the user's question.";
    }
    console.log("[VOICE-RAG] sendText:", combined.length, "chars");
    liveClient.sendText(combined);

    if (SHOW_VOICE_RAG_DEBUG) {
      // Show collapsible RAG/prompt details in localhost only.
      var ragBubble = document.createElement("div");
      ragBubble.className = "chat-msg chat-msg-assistant";
      ragBubble.appendChild(buildRagDetailsElement({
        systemPrompt: voiceSystemPrompt,
        transcript: transcript,
        ragContext: ragContext,
        indexSize: searchIndex ? searchIndex.length : null,
      }));
      msgContainer.appendChild(ragBubble);
      scrollToBottom();
    }

    return { ragContext: ragContext };
  }

  function createThinkingIndicator() {
    var el = document.createElement("div");
    el.className = "chat-thinking-indicator";
    el.innerHTML =
      '<div class="chat-thinking-brain">' +
      '<div class="chat-brain-ring"></div>' +
      '<div class="chat-brain-ring"></div>' +
      '<div class="chat-brain-ring"></div>' +
      "</div>" +
      '<div class="chat-thinking-text-area">' +
      '<span class="chat-thinking-label">Thinking...</span>' +
      '<span class="chat-thinking-quip"></span>' +
      "</div>";

    var quips = THINKING_QUIPS.slice();
    for (var i = quips.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = quips[i]; quips[i] = quips[j]; quips[j] = tmp;
    }
    var quipEl = el.querySelector(".chat-thinking-quip");
    var idx = 0;
    quipEl.textContent = quips[0];
    el._quipInterval = setInterval(function () {
      idx = (idx + 1) % quips.length;
      quipEl.style.opacity = "0";
      setTimeout(function () {
        quipEl.textContent = quips[idx];
        quipEl.style.opacity = "1";
      }, 300);
    }, 3200);
    return el;
  }

  function removeThinkingIndicator(el) {
    if (!el) return;
    if (el._quipInterval) clearInterval(el._quipInterval);
    if (el.parentNode) el.remove();
  }

  // Copy button for assistant messages
  function createCopyButton(text) {
    var btn = document.createElement("button");
    btn.className = "chat-copy-btn";
    btn.textContent = "\u{1F4CB}";
    btn.title = "Copy";
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "\u2713";
        btn.classList.add("copied");
        setTimeout(function () {
          btn.textContent = "\u{1F4CB}";
          btn.classList.remove("copied");
        }, 1500);
      });
    });
    return btn;
  }

  // Abort streaming
  function abortStreaming() {
    if (abortController) {
      abortController.abort();
      abortController = null;
    }
  }

  function appendMessage(role, content, skipSave) {
    // Remove welcome message on first real message
    var welcome = msgContainer.querySelector(".chat-welcome");
    if (welcome) welcome.remove();

    var bubble = document.createElement("div");
    bubble.className = "chat-msg chat-msg-" + role;

    if (role === "assistant" && content) {
      var displayContent = content.replace(/\n*Read more:[\s\S]*$/, "").trim();
      bubble.innerHTML = '<div class="chat-msg-text">' + renderMarkdown(displayContent) + "</div>";
      // Check for pending LaTeX in restored messages
      if (bubble.querySelector(".chat-latex-pending")) {
        loadKatex();
      }
    } else {
      bubble.textContent = content;
    }

    // Add action bar (TTS + copy) for assistant messages
    if (role === "assistant" && content) {
      var actions = document.createElement("div");
      actions.className = "chat-msg-actions";
      var ttsBtn = document.createElement("button");
      ttsBtn.className = "chat-tts-btn";
      ttsBtn.textContent = "\u{1F50A}";
      ttsBtn.title = "Listen";
      ttsBtn.addEventListener("click", function () {
        playTTS(content, ttsBtn);
      });
      actions.appendChild(ttsBtn);
      actions.appendChild(createCopyButton(content));
      bubble.appendChild(actions);
    }

    msgContainer.appendChild(bubble);
    scrollToBottom(true);

    if (!skipSave) {
      messages.push({ role: role, content: content });
      ChatStorage.saveMessages(messages);
    }

    return bubble;
  }

  function handleSend() {
    var text = input.value.trim();
    if (!text || isStreaming) return;

    input.value = "";
    input.style.height = "auto";
    appendMessage("user", text);

    // Get RAG context (with caching)
    var cacheKey = text.toLowerCase();
    var context;
    if (ragCache[cacheKey]) {
      context = ragCache[cacheKey].context;
      lastSearchResults = ragCache[cacheKey].results;
    } else {
      context = searchContent(text);
      ragCache[cacheKey] = {
        context: context,
        results: lastSearchResults.slice(),
        ts: Date.now(),
      };
      ChatStorage.saveRagCache(ragCache);
    }

    // Build history (exclude last user message, we send it as question)
    var history = messages.slice(0, -1).map(function (m) {
      return { role: m.role, content: m.content };
    });

    // Fire visuals request in parallel -- renders its own card independently of text stream
    var imageOptions = findTopImageCandidates(text, lastSearchResults, 3);
    fetchVisuals(text, context, imageOptions).then(function (visuals) {
      if (!visuals) return;
      var card = renderVisualCard(visuals);
      if (!card) return;
      console.log("[VISUALS] rendering independent card");
      // Insert before thinking indicator so the loader stays at the bottom
      var thinkingEl = msgContainer.querySelector(".chat-thinking-indicator");
      if (thinkingEl) {
        msgContainer.insertBefore(card, thinkingEl);
      } else {
        msgContainer.appendChild(card);
      }
      scrollToBottom();
      ChatStorage.attachVisuals(messages, visuals);
    });

    sendChatRequest(text, context, history);
  }

  function showStreamingUI(on) {
    var stopBtn = panel.querySelector(".chat-stop-btn");
    if (on) {
      sendBtn.style.display = "none";
      stopBtn.style.display = "flex";
    } else {
      sendBtn.style.display = "flex";
      stopBtn.style.display = "none";
    }
  }

  function finalizeResponse(bubble, fullText, question) {
    // Update stored message with all enrichments
    var lastMsg = messages[messages.length - 1];
    lastMsg.content = fullText;

    // Strip "Read more:" lines for display (source pills replace them)
    var displayText = fullText.replace(/\n*Read more:[\s\S]*$/, "").trim();

    // Re-render with rich markdown
    var textEl = bubble.querySelector(".chat-msg-text");
    if (textEl) textEl.innerHTML = renderMarkdown(displayText);

    // Source pills — extract and persist
    var sourceLinksData = extractSourceLinksData(fullText, lastSearchResults);
    if (sourceLinksData.length > 0) {
      lastMsg.sourceLinks = sourceLinksData;
      renderSourcePills(bubble, sourceLinksData);
    }

    // Relevant image — find and persist
    var relevantImg = findRelevantImage(question, lastSearchResults);
    if (relevantImg) {
      lastMsg.relevantImage = { path: relevantImg.path, title: relevantImg.title || "" };
      renderRelevantImage(bubble, relevantImg.path, relevantImg.title || "");
    }

    ChatStorage.saveMessages(messages);

    // Lazy-load KaTeX if LaTeX was detected
    if (bubble.querySelector(".chat-latex-pending")) {
      loadKatex();
    }

    // Action bar (TTS + copy)
    var actions = document.createElement("div");
    actions.className = "chat-msg-actions";
    var ttsBtn = document.createElement("button");
    ttsBtn.className = "chat-tts-btn";
    ttsBtn.textContent = "\u{1F50A}";
    ttsBtn.title = "Listen";
    ttsBtn.addEventListener("click", function () {
      playTTS(fullText, ttsBtn);
    });
    actions.appendChild(ttsBtn);
    actions.appendChild(createCopyButton(fullText));
    bubble.appendChild(actions);

    isStreaming = false;
    sendBtn.disabled = false;
    showStreamingUI(false);

  // Voice mode: auto-play TTS, then listen again
    if (voiceMode) {
      playTTS(fullText, ttsBtn, function () {
        if (voiceMode) startVoiceListening();
      });
    }
  }

  function sendChatRequest(question, context, history) {
    isStreaming = true;
    sendBtn.disabled = true;
    showStreamingUI(true);

    // Show thinking indicator
    var thinking = createThinkingIndicator();
    msgContainer.appendChild(thinking);
    scrollToBottom(true);

    // Abort controller for stop button
    abortController = new AbortController();

    fetch(API_BASE + "/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        context: context,
        history: history,
      }),
      signal: abortController.signal,
    })
      .then(function (response) {
        removeThinkingIndicator(thinking);

        if (!response.ok) {
          throw new Error("Talk request failed: " + response.status);
        }

        // Create empty bubble for streaming
        var bubble = document.createElement("div");
        bubble.className = "chat-msg chat-msg-assistant";
        bubble.innerHTML = '<div class="chat-msg-text"></div>';
        var welcome = msgContainer.querySelector(".chat-welcome");
        if (welcome) welcome.remove();
        msgContainer.appendChild(bubble);
        messages.push({ role: "assistant", content: "" });
        scrollToBottom(true);

        var fullText = "";
        var reader = response.body.getReader();
        var decoder = new TextDecoder();

        function read() {
          return reader.read().then(function (result) {
            if (result.done) {
              finalizeResponse(bubble, fullText, question);
              return;
            }

            var chunk = decoder.decode(result.value, { stream: true });
            fullText += chunk;
            var textEl = bubble.querySelector(".chat-msg-text");
            if (textEl) {
              textEl.textContent = fullText;
            } else {
              bubble.textContent = fullText;
            }
            scrollToBottom();
            return read();
          });
        }

        return read();
      })
      .catch(function (err) {
        removeThinkingIndicator(thinking);
        if (err.name === "AbortError") {
          // User stopped generation - finalize with whatever we have
          var bubble = msgContainer.querySelector(
            ".chat-msg-assistant:last-child"
          );
          if (bubble) {
            var textEl = bubble.querySelector(".chat-msg-text");
            var partial = textEl ? textEl.textContent : "";
            if (partial) {
              finalizeResponse(bubble, partial, question);
              return;
            }
          }
        } else {
          appendMessage(
            "assistant",
            "Sorry, I had trouble connecting. " + err.message
          );
        }
        isStreaming = false;
        sendBtn.disabled = false;
        showStreamingUI(false);
      });
  }

  // ========================================
  // VOICE INPUT (Web Speech API)
  // ========================================

  var recognition = null;

  // Mic button: transcribe into input field (no auto-submit)
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
      var transcript = correctTranscript(event.results[0][0].transcript);
      recognition = null;
      voiceChatBtn.classList.remove("recording");
      onResult(transcript);
    };

    recognition.onerror = function () {
      recognition = null;
      voiceChatBtn.classList.remove("recording");
      if (listeningIndicator && listeningIndicator.parentNode) listeningIndicator.remove();
      listeningIndicator = null;
    };

    recognition.onend = function () {
      recognition = null;
    };

    recognition.start();
  }

  // ========================================
  // VOICE MODE
  // ========================================

  function toggleVoiceChat() {
    voiceMode = !voiceMode;

    if (voiceMode) {
      voiceChatBtn.classList.add("voice-active");
      voiceChatBtn.title = "Stop voice mode";
      // Start listening immediately
      startVoiceListening();
    } else {
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.classList.remove("recording");
      voiceChatBtn.title = "Voice mode";
      if (recognition) {
        recognition.stop();
        recognition = null;
      }
    }
  }

  // Voice mode: listen, auto-submit, TTS will auto-play via sendChatRequest callback
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
      '<div class="chat-listening-ring">&#x1F3A4;</div>' +
      "<span>Listening...</span>";
    return el;
  }

  // Track currently playing audio so we can stop it
  var currentAudio = null;

  function stopCurrentAudio() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
  }

  // onEnded callback is used by voice chat mode to chain: TTS done -> listen again
  function playTTS(text, btn, onEnded) {
    // If already playing, stop it (toggle behavior)
    if (currentAudio && !currentAudio.paused) {
      stopCurrentAudio();
      if (btn) {
        btn.textContent = "\u{1F50A}";
        btn.classList.remove("loading");
      }
      return;
    }

    function playAudioUrl(audioUrl) {
      stopCurrentAudio();
      var audio = new Audio(audioUrl);
      currentAudio = audio;
      audio.addEventListener("ended", function () {
        currentAudio = null;
        if (btn) btn.textContent = "\u{1F50A}";
        if (onEnded) onEnded();
      });
      if (btn) btn.textContent = "\u23F9";
      audio.play();
    }

    // Check cache
    if (audioCache[text]) {
      playAudioUrl(audioCache[text]);
      return;
    }

    if (btn) {
      btn.classList.add("loading");
      btn.textContent = "\u23F3";
    }

    // Show waveform animation in the chat
    var waveform = createWaveformIndicator("Generating voice...");
    msgContainer.appendChild(waveform);
    scrollToBottom();

    fetch(API_BASE + "/api/tts", {
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
        if (btn) btn.classList.remove("loading");
        playAudioUrl(url);
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
  // GEMINI LIVE VOICE MODE
  // ========================================

  // ========================================
  // LOCAL SPEECH TRANSCRIPTION (user bubbles + RAG in voice mode)
  // ========================================

  function resetVoiceIdleTimer() {
    if (voiceIdleTimer) clearTimeout(voiceIdleTimer);
    voiceIdleTimer = setTimeout(function () {
      if (liveVoiceMode && !aiSpeaking) {
        console.log("[VOICE] idle timeout — stopping voice mode");
        stopLiveVoice();
      }
    }, VOICE_IDLE_MS);
  }

  function clearVoiceIdleTimer() {
    if (voiceIdleTimer) { clearTimeout(voiceIdleTimer); voiceIdleTimer = null; }
  }

  function startLocalTranscription() {
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { console.log("[VOICE-RAG] No SpeechRecognition API"); return; }
    console.log("[VOICE-RAG] startLocalTranscription called");

    localRecognition = new SR();
    localRecognition.lang = "en-US";
    localRecognition.continuous = true;
    localRecognition.interimResults = false;

    localRecognition.onresult = function (event) {
      for (var i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          var chunk = correctTranscript(event.results[i][0].transcript.trim());
          if (!chunk) continue;

          // Accumulate chunks (Chrome can split utterances across recognition restarts)
          resetVoiceIdleTimer();
          liveVoiceAccumulator += (liveVoiceAccumulator ? " " : "") + chunk;
          console.log("[VOICE-RAG] chunk:", chunk, "| accumulated:", liveVoiceAccumulator);

          // Update or create user bubble immediately (shows what we're hearing)
          if (!liveVoiceUserBubble) {
            var welcome = msgContainer.querySelector(".chat-welcome");
            if (welcome) welcome.remove();
            liveVoiceUserBubble = document.createElement("div");
            liveVoiceUserBubble.className = "chat-msg chat-msg-user";
            msgContainer.appendChild(liveVoiceUserBubble);
          }
          liveVoiceUserBubble.textContent = liveVoiceAccumulator;
          scrollToBottom();

          // Debounce: wait 1.5s of silence before sending to Gemini with RAG
          if (liveVoiceDebounceTimer) clearTimeout(liveVoiceDebounceTimer);
          liveVoiceDebounceTimer = setTimeout(function () {
            liveVoiceDebounceTimer = null;
            var transcript = liveVoiceAccumulator;
            liveVoiceAccumulator = "";
            liveVoiceUserBubble = null;

            console.log("[VOICE-RAG] debounce fired, sending:", transcript);
            liveVoiceQuestion = transcript;
            liveVoiceSpoken = "";
            liveVoiceThinking = "";
            liveVoiceBubble = null;
            showVoiceState("thinking");

            // Save to messages array
            messages.push({ role: "user", content: transcript });
            ChatStorage.saveMessages(messages);

            // RAG: search book index, send to Gemini, show debug bubble
            var ragResult = sendRagToGemini(transcript);
            var ragContext = ragResult.ragContext;
            if (liveClient && liveClient.isConnected()) {
              // Fire parallel visuals request -- render immediately when ready
              var voiceImageOptions = findTopImageCandidates(transcript, lastSearchResults, 3);
              fetchVisuals(transcript, ragContext, voiceImageOptions).then(function (visuals) {
                if (!visuals) return;
                var card = renderVisualCard(visuals);
                if (!card) return;
                console.log("[VISUALS] rendering voice visual card immediately");
                // Insert before thinking indicator so the loader stays at the bottom
                var thinkingEl = msgContainer.querySelector(".chat-thinking-indicator");
                if (thinkingEl) {
                  msgContainer.insertBefore(card, thinkingEl);
                } else {
                  msgContainer.appendChild(card);
                }
                scrollToBottom();
                ChatStorage.attachVisuals(messages, visuals);
              });
            }
            scrollToBottom();
          }, 1500);
        }
      }
    };

    localRecognition.onerror = function (e) {
      console.log("[VOICE-RAG] onerror:", e.error, "paused:", localRecognitionPaused);
      if (e.error !== "no-speech" && e.error !== "aborted") {
        console.warn("Local recognition error:", e.error);
      }
    };

    localRecognition.onend = function () {
      console.log("[VOICE-RAG] onend, paused:", localRecognitionPaused, "voiceMode:", liveVoiceMode);
      localRecognition = null;
      // Don't restart if paused (Gemini is speaking) or voice mode ended
      if (localRecognitionPaused || !liveVoiceMode) return;
      setTimeout(startLocalTranscription, 200);
    };

    try {
      localRecognition.start();
      resetVoiceIdleTimer();
    } catch (_) {
      localRecognition = null;
    }
  }

  function stopLocalTranscription() {
    if (localRecognition) {
      var r = localRecognition;
      localRecognition = null;
      r.onend = null;
      r.onerror = null;
      try { r.stop(); } catch (_) {}
    }
  }

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
      '<div class="chat-listening-ring">&#x1F3A4;</div>' +
      "<span>Connecting...</span>";
    msgContainer.appendChild(connectingEl);
    msgContainer.scrollTop = msgContainer.scrollHeight;

    // Fetch ephemeral token for voice connection (real API key stays server-side)
    var voiceCredentials;
    try {
      voiceCredentials = await fetch(API_BASE + "/api/voice-token").then(function (r) {
        if (!r.ok) throw new Error("Token request failed: " + r.status);
        return r.json();
      });
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice mode";
      appendMessage("assistant", "Voice mode unavailable. " + err.message);
      return;
    }

    // Use system prompt from server (single source of truth in wishonia-chat.ts)
    var systemPrompt = voiceCredentials.systemPrompt || "";

    // Initialize audio playback
    audioPlayback = new AudioPlayback();
    try {
      await audioPlayback.init();
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice mode";
      appendMessage("assistant", "Could not initialize audio. " + err.message);
      return;
    }

    // When the AudioWorklet finishes playing all buffered audio, finalize the turn
    audioPlayback.onDrained = function () {
      if (!pendingTurnComplete) return;
      pendingTurnComplete = false;
      if (drainSafetyTimer) { clearTimeout(drainSafetyTimer); drainSafetyTimer = null; }
      finalizeTurnComplete();
    };

    // Connect to Gemini Live
    liveClient = new GeminiLiveClient({
      apiKey: voiceCredentials.token || voiceCredentials.key,
      systemInstruction: systemPrompt,
      voice: "Kore",
      onInputTranscript: function (transcript) {
        if (!transcript || !transcript.trim()) return;
        transcript = correctTranscript(transcript.trim());
        console.log("[VOICE-RAG] onInputTranscript:", transcript, "aiSpeaking:", aiSpeaking, "localRecognition:", !!localRecognition);
        // Ignore echo transcripts while AI is speaking (residual audio leaking past echo cancellation)
        if (aiSpeaking) return;
        // Skip if local SpeechRecognition is handling user speech + RAG
        if (localRecognition) return;
        console.log("[VOICE-RAG] onInputTranscript handling (localSR not active)");
        appendMessage("user", transcript);
        liveVoiceQuestion = transcript;
        liveVoiceSpoken = "";
        liveVoiceThinking = "";
        liveVoiceBubble = null;
        showVoiceState("thinking");

        // Live RAG: send question + context as combined text to interrupt audio-only response
        sendRagToGemini(transcript.trim());
      },
      onModelTurnStarted: function () {
        // Keep showing thinking indicator - switch to "speaking" on first audio chunk
        // Pause local recognition while Gemini speaks to prevent echo transcription
        clearVoiceIdleTimer();
        aiSpeaking = true;
        localRecognitionPaused = true;
        if (localRecognition) {
          try { localRecognition.stop(); } catch (_) {}
        }
      },
      onAudio: function (b64) {
        // Switch to speaking state on first audio chunk (not on model turn start)
        if (voiceStateEl && voiceStateEl.className === "chat-thinking-indicator") {
          showVoiceState("speaking");
        }
        audioPlayback.play(b64);
        // Start analyser-driven lipsync loop on first chunk
        if (!mouthRafId && window.wishoniaAnimator) startMouthLoop();
      },
      onText: function (text) {
        // Chain-of-thought text from native audio model
        if (text) liveVoiceThinking += text;
      },
      onOutputTranscript: function (text) {
        // Transcript of what Gemini actually spoke - stream into bubble
        if (!text) return;
        liveVoiceSpoken += text;
        // Create or update streaming bubble
        if (!liveVoiceBubble) {
          var welcome = msgContainer.querySelector(".chat-welcome");
          if (welcome) welcome.remove();
          liveVoiceBubble = document.createElement("div");
          liveVoiceBubble.className = "chat-msg chat-msg-assistant";
          liveVoiceBubble.innerHTML = '<div class="chat-msg-text"></div>';
          msgContainer.appendChild(liveVoiceBubble);
        }
        var textEl = liveVoiceBubble.querySelector(".chat-msg-text");
        if (textEl) textEl.innerHTML = renderMarkdown(liveVoiceSpoken);
        scrollToBottom();
      },
      onInterrupted: function () {
        // Cancel any pending drain-wait from a prior turnComplete
        pendingTurnComplete = false;
        if (drainSafetyTimer) { clearTimeout(drainSafetyTimer); drainSafetyTimer = null; }
        stopMouthLoop();
        aiSpeaking = false;
        audioPlayback.interrupt();
        if (window.wishoniaAnimator) window.wishoniaAnimator.stopSpeaking();
        if (liveVoiceThinking || liveVoiceSpoken) {
          appendVoiceMessage(liveVoiceThinking, liveVoiceSpoken);
          liveVoiceThinking = "";
          liveVoiceSpoken = "";
        }
        showVoiceState("listening");
        localRecognitionPaused = false;
        if (liveVoiceMode) {
          stopLocalTranscription();
          setTimeout(startLocalTranscription, 300);
        }
      },
      onTurnComplete: function () {
        // Defer mouth/state cleanup until the AudioWorklet drains its buffer,
        // so the mouth keeps moving while buffered audio is still playing.
        pendingTurnComplete = true;
        drainSafetyTimer = setTimeout(function () {
          if (!pendingTurnComplete) return;
          pendingTurnComplete = false;
          drainSafetyTimer = null;
          finalizeTurnComplete();
        }, 2000);
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
      voiceChatBtn.title = "Voice mode";
      audioPlayback.destroy();
      audioPlayback = null;
      liveClient = null;
      appendMessage("assistant", "Could not connect to voice. " + err.message);
      return;
    }

    // Start mic capture with volume metering
    // When localRecognition is available, DON'T send audio to Gemini.
    // Instead, localRecognition transcribes speech -> RAG search -> sendText with context.
    // This prevents: (a) echo (Gemini hearing its own voice), (b) Gemini responding before RAG arrives.
    var hasLocalSR = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
    audioCapture = new AudioCapture(
      function (b64chunk) {
        if (!liveClient) return;
        // Send audio when: (a) no local SR (fallback), or (b) AI is speaking (for interrupt detection via server VAD)
        if (!hasLocalSR || aiSpeaking) liveClient.sendAudio(b64chunk);
      },
      function (volume) {
        updateVolumeVisualizer(volume);
      }
    );

    try {
      await audioCapture.start();
    } catch (err) {
      if (connectingEl.parentNode) connectingEl.remove();
      liveClient.disconnect();
      liveClient = null;
      audioPlayback.destroy();
      audioPlayback = null;
      voiceChatBtn.classList.remove("voice-active");
      voiceChatBtn.title = "Voice mode";
      appendMessage("assistant", "Microphone access denied.");
      return;
    }

    // Connected!
    if (connectingEl.parentNode) connectingEl.remove();
    liveVoiceMode = true;
    liveVoiceTranscript = "";
    voiceChatBtn.title = "Stop voice mode";
    showVoiceState("listening");
    startLocalTranscription();
  }

  var liveVoiceTranscript = "";
  var liveVoiceThinking = "";
  var liveVoiceSpoken = "";
  var liveVoiceQuestion = ""; // last user question for image search
  var liveVoiceBubble = null; // streaming bubble for voice responses
  var liveVoiceVisualsPromise = null; // parallel visuals request for voice mode
  var liveVoiceAccumulator = ""; // accumulates transcript chunks across recognition restarts
  var liveVoiceDebounceTimer = null; // debounce timer before sending accumulated transcript
  var liveVoiceUserBubble = null; // user message bubble updated as chunks arrive
  var localRecognitionPaused = false; // suppress auto-restart while Gemini speaks
  var aiSpeaking = false; // true while AI is responding, enables audio-to-Gemini for interrupt detection
  var voiceStateEl = null;

  // Drive mouth animation from actual speaker output via AnalyserNode
  function startMouthLoop() {
    if (mouthRafId) return;
    function tick() {
      if (!audioPlayback) { mouthRafId = null; return; }
      var amp = audioPlayback.getAmplitude();
      window.wishoniaAnimator.setMouthFromAmplitude(amp);
      mouthRafId = requestAnimationFrame(tick);
    }
    mouthRafId = requestAnimationFrame(tick);
  }

  function stopMouthLoop() {
    if (mouthRafId) { cancelAnimationFrame(mouthRafId); mouthRafId = null; }
  }

  function finalizeTurnComplete() {
    stopMouthLoop();
    aiSpeaking = false;
    if (window.wishoniaAnimator) window.wishoniaAnimator.stopSpeaking();
    if (liveVoiceThinking || liveVoiceSpoken) {
      appendVoiceMessage(liveVoiceThinking, liveVoiceSpoken);
      liveVoiceThinking = "";
      liveVoiceSpoken = "";
    }
    showVoiceState("listening");
    localRecognitionPaused = false;
    if (liveVoiceMode) {
      stopLocalTranscription();
      setTimeout(startLocalTranscription, 300);
    }
  }

  function appendVoiceMessage(thinking, spoken) {
    // Use the streaming bubble if it exists, otherwise create one
    var bubble = liveVoiceBubble;
    if (!bubble) {
      var welcome = msgContainer.querySelector(".chat-welcome");
      if (welcome) welcome.remove();
      bubble = document.createElement("div");
      bubble.className = "chat-msg chat-msg-assistant";
      msgContainer.appendChild(bubble);
    }
    liveVoiceBubble = null;

    // Clear existing content for final rich render
    bubble.innerHTML = "";

    var fullText = (spoken || "").trim();

    // Track enrichments for saving
    var voiceSourceLinks = [];
    var voiceRelevantImg = null;

    if (fullText) {
      // Strip "Read more:" for display
      var displayText = fullText.replace(/\n*Read more:[\s\S]*$/, "").trim();
      var textDiv = document.createElement("div");
      textDiv.className = "chat-msg-text";
      textDiv.innerHTML = renderMarkdown(displayText);
      bubble.appendChild(textDiv);

      // Source pills
      voiceSourceLinks = extractSourceLinksData(fullText, lastSearchResults);
      if (voiceSourceLinks.length > 0) {
        renderSourcePills(bubble, voiceSourceLinks);
      }

      // Relevant image
      var relevantImg = findRelevantImage(liveVoiceQuestion, lastSearchResults);
      if (relevantImg) {
        voiceRelevantImg = { path: relevantImg.path, title: relevantImg.title || "" };
        renderRelevantImage(bubble, relevantImg.path, relevantImg.title || "");
      }

      // LaTeX
      if (bubble.querySelector(".chat-latex-pending")) {
        loadKatex();
      }
    } else {
      var note = document.createElement("div");
      note.className = "chat-voice-note";
      note.textContent = "\uD83D\uDD0A Responded via voice";
      bubble.appendChild(note);
    }

    // Collapsible thinking block
    if (thinking && thinking.trim()) {
      var details = document.createElement("details");
      details.className = "chat-thinking";
      var summary = document.createElement("summary");
      summary.textContent = "\uD83D\uDCA1 Show thinking";
      details.appendChild(summary);
      var pre = document.createElement("pre");
      pre.className = "chat-thinking-text";
      pre.textContent = thinking.trim();
      details.appendChild(pre);
      bubble.appendChild(details);
    }

    // Action bar (TTS + copy) - same as text mode
    if (fullText) {
      var actions = document.createElement("div");
      actions.className = "chat-msg-actions";
      var ttsBtn = document.createElement("button");
      ttsBtn.className = "chat-tts-btn";
      ttsBtn.textContent = "\u{1F50A}";
      ttsBtn.title = "Listen";
      ttsBtn.addEventListener("click", function () {
        playTTS(fullText, ttsBtn);
      });
      actions.appendChild(ttsBtn);
      actions.appendChild(createCopyButton(fullText));
      bubble.appendChild(actions);
    }

    scrollToBottom();

    // Save to session, carrying forward any visuals attached by the async callback
    if (fullText) {
      var newMsg = { role: "assistant", content: fullText };
      var prev = messages[messages.length - 1];
      if (prev && prev.role === "assistant" && prev.visuals) {
        newMsg.visuals = prev.visuals;
      }
      if (voiceSourceLinks.length > 0) newMsg.sourceLinks = voiceSourceLinks;
      if (voiceRelevantImg) newMsg.relevantImage = voiceRelevantImg;
      messages.push(newMsg);
      ChatStorage.saveMessages(messages);
    }
  }

  function showVoiceState(state) {
    if (!liveVoiceMode) return;

    // Remove previous state indicator
    if (voiceStateEl) {
      if (voiceStateEl._quipInterval) clearInterval(voiceStateEl._quipInterval);
      if (voiceStateEl.parentNode) voiceStateEl.remove();
    }
    voiceStateEl = null;

    if (state === "listening") {
      voiceStateEl = document.createElement("div");
      voiceStateEl.className = "chat-listening-indicator";
      voiceStateEl.innerHTML =
        '<div class="chat-volume-bars">' +
        '<div class="chat-vol-bar"></div>'.repeat(5) +
        "</div>" +
        "<span>Listening...</span>";
      voiceChatBtn.classList.add("recording");
    } else if (state === "thinking") {
      voiceStateEl = document.createElement("div");
      voiceStateEl.className = "chat-thinking-indicator";
      voiceStateEl.innerHTML =
        '<div class="chat-thinking-brain">' +
        '<div class="chat-brain-ring"></div>' +
        '<div class="chat-brain-ring"></div>' +
        '<div class="chat-brain-ring"></div>' +
        "</div>" +
        '<div class="chat-thinking-text-area">' +
        '<span class="chat-thinking-label">While I\'m crafting the optimal response to your incredibly insightful statement, please consider these fun facts:</span>' +
        '<span class="chat-thinking-quip"></span>' +
        "</div>";
      // Rotate quips: mix of jokes and key book concepts as loading-screen education
      var quips = [
        // Personality
        "Consulting my notes on your species...",
        "Translating from Wishonian to English...",
        "Searching for the polite way to say this...",
        // Core concept: the spending ratio
        "Did you know? You spend 604x more on weapons than testing medicines.",
        // Core concept: the 1% treaty
        "The 1% Treaty: redirect 1% of military budgets to clinical trials.",
        // Core concept: the destructive economy clock
        "Your destructive economy is 11.5% of GDP. The Soviet Union collapsed at 15%.",
        // Core concept: incentive alignment bonds
        "Incentive Alignment Bonds: investors fund cures, get paid when diseases drop.",
        // Core concept: wishocracy
        "Wishocracy: citizens pick priorities, 80% untouchable for science, 20% for politicians to behave.",
        // Core concept: the invisible graveyard
        "The Invisible Graveyard: 10 million die yearly from diseases that already have solutions.",
        // Core concept: corruption cap
        "The plan caps corruption at 20% (transparent) so the other 80% actually reaches patients.",
        // Core concept: why it self-reinforces
        "The loop: treaty funds trials, trials generate returns, returns pay investors who funded the campaign.",
        // Core concept: decentralized FDA
        "Your decentralized FDA: anyone can fund a trial, data is open, results belong to everyone.",
        // Scale
        "Comparing to 340 other planets (you rank 312th)...",
      ];
      var quipEl = voiceStateEl.querySelector(".chat-thinking-quip");
      // Shuffle so it's different each time
      for (var qi = quips.length - 1; qi > 0; qi--) {
        var qj = Math.floor(Math.random() * (qi + 1));
        var tmp = quips[qi]; quips[qi] = quips[qj]; quips[qj] = tmp;
      }
      var quipIdx = 0;
      quipEl.textContent = quips[0];
      voiceStateEl._quipInterval = setInterval(function () {
        quipIdx = (quipIdx + 1) % quips.length;
        quipEl.style.opacity = "0";
        setTimeout(function () {
          quipEl.textContent = quips[quipIdx];
          quipEl.style.opacity = "1";
        }, 300);
      }, 3200);
      voiceChatBtn.classList.remove("recording");
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

  function updateVolumeVisualizer(volume) {
    if (!voiceStateEl) return;
    var bars = voiceStateEl.querySelectorAll(".chat-vol-bar");
    if (!bars.length) return;
    // Scale volume (0-1) to bar heights. Boost it so normal speech is visible.
    var boosted = Math.min(volume * 4, 1);
    for (var i = 0; i < bars.length; i++) {
      // Each bar gets a slightly different height for visual variety
      var offset = (Math.sin(Date.now() / 100 + i * 1.3) + 1) / 2 * 0.3;
      var h = Math.max(4, (boosted + offset * boosted) * 32);
      bars[i].style.height = h + "px";
    }
  }

  function stopLiveVoice() {
    clearVoiceIdleTimer();
    liveVoiceMode = false;
    aiSpeaking = false;
    pendingTurnComplete = false;
    if (drainSafetyTimer) { clearTimeout(drainSafetyTimer); drainSafetyTimer = null; }
    stopMouthLoop();
    stopLocalTranscription();

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
    voiceChatBtn.title = "Voice mode";
    liveVoiceTranscript = "";
    liveVoiceThinking = "";
    liveVoiceSpoken = "";
    liveVoiceQuestion = "";
    liveVoiceBubble = null;
    liveVoiceAccumulator = "";
    liveVoiceUserBubble = null;
    if (liveVoiceDebounceTimer) { clearTimeout(liveVoiceDebounceTimer); liveVoiceDebounceTimer = null; }
    localRecognitionPaused = false;

    // Reset robot animation if present
    if (window.setRobotState) window.setRobotState("idle");
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
  // EXTERNAL API (for test page sidebar / embedding)
  // ========================================

  window.wishoniaChatWidget = {
    startNewChat: function () { startNewChat(); },
    loadChat: function (msgs) {
      messages = (msgs || []).filter(function (m) {
        return m.content && m.content !== "[voice response]";
      });
      ChatStorage.saveMessages(messages);
      if (msgContainer) {
        msgContainer.innerHTML = "";
        if (messages.length > 0) {
          messages.forEach(function (m) {
            appendMessage(m.role, m.content, true);
          });
        } else {
          showWelcome();
        }
      }
    },
    getMessages: function () { return messages.slice(); },
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
