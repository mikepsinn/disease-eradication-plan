(function () {
  "use strict";

  var ROOT_CLASS = "wishonia-chat-route";
  var READY_CLASS = "wishonia-chat-ready";
  var STORE_KEY = "wishonia-chats";
  var SESSION_KEY = "wishonia-chat";
  var MAX_MOUNT_ATTEMPTS = 100;
  var SAVE_INTERVAL_MS = 3000;

  document.documentElement.classList.add(ROOT_CLASS);

  function parseStorage(storage, key) {
    try {
      var raw = storage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    } catch (_) {
      return null;
    }
  }

  function loadStore() {
    var stored = parseStorage(localStorage, STORE_KEY);
    if (stored && stored.chats) {
      return stored;
    }
    return { current: null, chats: {} };
  }

  function saveStore() {
    localStorage.setItem(STORE_KEY, JSON.stringify(store));
  }

  function genId() {
    return "chat-" + Date.now() + "-" + Math.random().toString(36).slice(2, 10);
  }

  function getSessionMessages() {
    var messages = parseStorage(sessionStorage, SESSION_KEY);
    return Array.isArray(messages) ? messages : [];
  }

  function chatTitle(chat) {
    if (chat.title) return chat.title;
    var messages = Array.isArray(chat.messages) ? chat.messages : [];
    for (var i = 0; i < messages.length; i += 1) {
      if (messages[i].role === "user" && messages[i].content) {
        return messages[i].content.slice(0, 56);
      }
    }
    return "New talk";
  }

  function ensureStoreSeeded() {
    var chatIds = Object.keys(store.chats);
    if (chatIds.length > 0) {
      if (!store.current || !store.chats[store.current]) {
        store.current = chatIds[0];
      }
      return;
    }

    var initialMessages = getSessionMessages();
    var id = genId();
    store.chats[id] = {
      id: id,
      title: "",
      created: new Date().toISOString(),
      messages: initialMessages,
    };
    store.current = id;
    saveStore();
  }

  function syncSessionFromCurrent() {
    var chat = store.chats[store.current];
    if (chat && Array.isArray(chat.messages) && chat.messages.length > 0) {
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(chat.messages));
      return;
    }
    sessionStorage.removeItem(SESSION_KEY);
  }

  var store = loadStore();
  ensureStoreSeeded();
  syncSessionFromCurrent();

  function closeSidebar() {
    var sidebar = document.getElementById("wishonia-chat-sidebar");
    var overlay = document.getElementById("wishonia-chat-overlay");
    if (sidebar) sidebar.classList.remove("is-open");
    if (overlay) overlay.classList.remove("is-open");
  }

  function renderSidebar() {
    var list = document.getElementById("wishonia-chat-list");
    if (!list) return;

    list.innerHTML = "";

    var ids = Object.keys(store.chats).sort(function (a, b) {
      return new Date(store.chats[b].created).getTime() - new Date(store.chats[a].created).getTime();
    });

    ids.forEach(function (chatId) {
      var chat = store.chats[chatId];
      var item = document.createElement("div");
      item.className = "wishonia-chat-item" + (chatId === store.current ? " is-active" : "");
      item.setAttribute("role", "button");
      item.setAttribute("tabindex", "0");

      var title = document.createElement("span");
      title.className = "wishonia-chat-item-title";
      title.textContent = chatTitle(chat);

      var del = document.createElement("button");
      del.type = "button";
      del.className = "wishonia-chat-item-delete";
      del.setAttribute("aria-label", "Delete talk");
      del.textContent = "x";
      del.addEventListener("click", function (event) {
        event.stopPropagation();
        deleteChat(chatId);
      });

      item.appendChild(title);
      item.appendChild(del);
      item.addEventListener("click", function () {
        switchChat(chatId);
      });
      item.addEventListener("keydown", function (event) {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          switchChat(chatId);
        }
      });
      list.appendChild(item);
    });
  }

  function saveCurrent() {
    if (!store.current || !window.wishoniaChatWidget) return;

    var messages = window.wishoniaChatWidget.getMessages();
    if (!store.chats[store.current]) return;

    store.chats[store.current].messages = messages;
    if (!store.chats[store.current].title) {
      for (var i = 0; i < messages.length; i += 1) {
        if (messages[i].role === "user" && messages[i].content) {
          store.chats[store.current].title = messages[i].content.slice(0, 56);
          break;
        }
      }
    }

    syncSessionFromCurrent();
    saveStore();
    renderSidebar();
  }

  function createNewChat() {
    saveCurrent();

    var id = genId();
    store.chats[id] = {
      id: id,
      title: "",
      created: new Date().toISOString(),
      messages: [],
    };
    store.current = id;
    syncSessionFromCurrent();
    saveStore();

    if (window.wishoniaChatWidget) {
      window.wishoniaChatWidget.startNewChat();
    }

    renderSidebar();
    closeSidebar();
  }

  function switchChat(chatId) {
    if (chatId === store.current) {
      closeSidebar();
      return;
    }

    saveCurrent();
    store.current = chatId;
    syncSessionFromCurrent();
    saveStore();

    if (window.wishoniaChatWidget) {
      var chat = store.chats[chatId];
      window.wishoniaChatWidget.loadChat(chat ? chat.messages : []);
    }

    renderSidebar();
    closeSidebar();
  }

  function deleteChat(chatId) {
    delete store.chats[chatId];

    var remainingIds = Object.keys(store.chats);
    if (remainingIds.length === 0) {
      createNewChat();
      return;
    }

    if (store.current === chatId) {
      store.current = remainingIds[0];
      syncSessionFromCurrent();
      if (window.wishoniaChatWidget) {
        var current = store.chats[store.current];
        window.wishoniaChatWidget.loadChat(current ? current.messages : []);
      }
    }

    saveStore();
    renderSidebar();
  }

  function mountWidget(attempt) {
    var mainArea = document.getElementById("wishonia-chat-main");
    var loading = document.getElementById("wishonia-chat-loading");
    var fab = document.querySelector(".chat-fab");
    var panel = document.querySelector(".chat-panel");

    if (!mainArea || !fab || !panel || !window.wishoniaChatWidget) {
      if (attempt >= MAX_MOUNT_ATTEMPTS) {
        if (loading) {
          loading.querySelector("span").textContent =
            "The talk shell loaded, but the widget never mounted.";
        }
        return;
      }
      window.setTimeout(function () {
        mountWidget(attempt + 1);
      }, 100);
      return;
    }

    if (!panel.classList.contains("chat-visible")) {
      fab.click();
      window.setTimeout(function () {
        mountWidget(attempt + 1);
      }, 80);
      return;
    }

    if (panel.parentNode !== mainArea) {
      mainArea.appendChild(panel);
    }

    var current = store.chats[store.current];
    window.wishoniaChatWidget.loadChat(current ? current.messages : []);

    if (loading) loading.hidden = true;
    document.documentElement.classList.add(READY_CLASS);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.getElementById("wishonia-chat-sidebar-toggle");
    var sidebar = document.getElementById("wishonia-chat-sidebar");
    var overlay = document.getElementById("wishonia-chat-overlay");
    var newChatBtn = document.getElementById("wishonia-chat-new");

    if (toggle && sidebar && overlay) {
      toggle.addEventListener("click", function () {
        sidebar.classList.toggle("is-open");
        overlay.classList.toggle("is-open");
      });

      overlay.addEventListener("click", closeSidebar);
    }

    if (newChatBtn) {
      newChatBtn.addEventListener("click", createNewChat);
    }

    renderSidebar();
    mountWidget(0);

    window.setInterval(saveCurrent, SAVE_INTERVAL_MS);
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) saveCurrent();
    });
    window.addEventListener("pagehide", saveCurrent);
  });
})();
