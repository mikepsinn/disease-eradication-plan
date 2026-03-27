/**
 * ChatStorage — centralised persistence for the Wishonia chat widget.
 *
 * All localStorage access goes through this module so keys stay consistent
 * and every save/restore path handles the same data shape.
 *
 * Storage keys:
 *   wishonia-chat        — message array (role, content, visuals)
 *   wishonia-rag-cache   — RAG context cache {queryLower: {context, results, ts}}
 *   wishonia-image-index — image index metadata array
 */
// eslint-disable-next-line no-unused-vars
var ChatStorage = (function () {
  "use strict";

  var KEYS = {
    messages:   "wishonia-chat",
    ragCache:   "wishonia-rag-cache",
    imageIndex: "wishonia-image-index",
  };

  // Max age for cached RAG entries (24 hours)
  var RAG_TTL_MS = 24 * 60 * 60 * 1000;

  // ── helpers ──────────────────────────────────────────────────────

  function _get(key) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  function _set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (_) {
      // quota exceeded — silently fail
    }
  }

  function _remove(key) {
    localStorage.removeItem(key);
  }

  // ── messages ─────────────────────────────────────────────────────

  /**
   * Load saved messages. Returns an array (possibly empty).
   * Filters out placeholder entries like "[voice response]".
   */
  function loadMessages() {
    var arr = _get(KEYS.messages);
    if (!Array.isArray(arr)) return [];
    return arr.filter(function (m) {
      return m && m.content && m.content !== "[voice response]";
    });
  }

  /**
   * Persist the full messages array.
   * Call this after every mutation (push, content update, visuals attach).
   */
  function saveMessages(messages) {
    _set(KEYS.messages, messages);
  }

  /** Wipe message history (New Chat). */
  function clearMessages() {
    _remove(KEYS.messages);
  }

  /**
   * Attach visuals to the last assistant message and save.
   * No-op if the last message isn't an assistant message.
   * Returns true if visuals were attached.
   */
  function attachVisuals(messages, visuals) {
    if (!visuals) return false;
    var last = messages[messages.length - 1];
    if (!last || last.role !== "assistant") return false;
    last.visuals = visuals;
    saveMessages(messages);
    return true;
  }

  // ── RAG cache ────────────────────────────────────────────────────

  function loadRagCache() {
    var cache = _get(KEYS.ragCache);
    if (!cache || typeof cache !== "object") return {};
    // Evict stale entries
    var now = Date.now();
    var clean = {};
    for (var key in cache) {
      if (cache[key] && cache[key].ts && now - cache[key].ts < RAG_TTL_MS) {
        clean[key] = cache[key];
      }
    }
    return clean;
  }

  function saveRagCache(cache) {
    _set(KEYS.ragCache, cache);
  }

  function clearRagCache() {
    _remove(KEYS.ragCache);
  }

  // ── image index ──────────────────────────────────────────────────

  function loadImageIndex() {
    return _get(KEYS.imageIndex);
  }

  function saveImageIndex(index) {
    _set(KEYS.imageIndex, index);
  }

  function clearImageIndex() {
    _remove(KEYS.imageIndex);
  }

  // ── bulk clear (New Chat) ────────────────────────────────────────

  function clearAll() {
    clearMessages();
    clearRagCache();
    // Keep image index — it's global, not per-conversation
  }

  // ── public API ───────────────────────────────────────────────────

  return {
    KEYS: KEYS,

    loadMessages:   loadMessages,
    saveMessages:   saveMessages,
    clearMessages:  clearMessages,
    attachVisuals:  attachVisuals,

    loadRagCache:   loadRagCache,
    saveRagCache:   saveRagCache,
    clearRagCache:  clearRagCache,

    loadImageIndex:  loadImageIndex,
    saveImageIndex:  saveImageIndex,
    clearImageIndex: clearImageIndex,

    clearAll: clearAll,
  };
})();
