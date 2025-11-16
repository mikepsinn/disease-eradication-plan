/**
 * Chat Widget for Book
 * Embeddable chat interface that connects to the book chat agent
 */

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

class BookChatWidget {
  private container: HTMLElement;
  private apiUrl: string;
  private messages: ChatMessage[] = [];
  private isOpen: boolean = false;
  private conversationId?: string;
  private userId?: string;

  constructor(containerId: string, apiUrl: string = "http://localhost:3141") {
    const container = document.getElementById(containerId);
    if (!container) {
      throw new Error(`Container with id "${containerId}" not found`);
    }
    this.container = container;
    this.apiUrl = apiUrl;
    this.userId = this.getOrCreateUserId();
    this.render();
  }

  private getOrCreateUserId(): string {
    let userId = localStorage.getItem("bookChatUserId");
    if (!userId) {
      userId = `user-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      localStorage.setItem("bookChatUserId", userId);
    }
    return userId;
  }

  private render(): void {
    this.container.innerHTML = `
      <div class="book-chat-widget">
        <button class="book-chat-toggle" id="bookChatToggle">
          💬 Chat with the Book
        </button>
        <div class="book-chat-panel" id="bookChatPanel" style="display: none;">
          <div class="book-chat-header">
            <h3>Chat with the Book</h3>
            <button class="book-chat-close" id="bookChatClose">×</button>
          </div>
          <div class="book-chat-messages" id="bookChatMessages"></div>
          <div class="book-chat-input-container">
            <textarea 
              class="book-chat-input" 
              id="bookChatInput" 
              placeholder="Ask a question about the book..."
              rows="2"
            ></textarea>
            <button class="book-chat-send" id="bookChatSend">Send</button>
          </div>
          <div class="book-chat-feedback">
            <button class="book-chat-feedback-btn" id="bookChatFeedback">Report Issue</button>
          </div>
        </div>
      </div>
    `;

    this.attachEventListeners();
  }

  private attachEventListeners(): void {
    const toggle = document.getElementById("bookChatToggle");
    const close = document.getElementById("bookChatClose");
    const send = document.getElementById("bookChatSend");
    const input = document.getElementById("bookChatInput") as HTMLTextAreaElement;
    const feedback = document.getElementById("bookChatFeedback");

    toggle?.addEventListener("click", () => this.toggle());
    close?.addEventListener("click", () => this.toggle());
    send?.addEventListener("click", () => this.sendMessage());
    feedback?.addEventListener("click", () => this.showFeedbackDialog());

    input?.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
  }

  private toggle(): void {
    this.isOpen = !this.isOpen;
    const panel = document.getElementById("bookChatPanel");
    if (panel) {
      panel.style.display = this.isOpen ? "block" : "none";
    }
    if (this.isOpen) {
      const input = document.getElementById("bookChatInput") as HTMLTextAreaElement;
      input?.focus();
    }
  }

  private async sendMessage(): Promise<void> {
    const input = document.getElementById("bookChatInput") as HTMLTextAreaElement;
    const message = input?.value.trim();
    if (!message) return;

    // Add user message
    this.addMessage("user", message);
    input!.value = "";

    // Show loading
    const loadingId = this.addMessage("assistant", "Thinking...");

    try {
      const response = await fetch(`${this.apiUrl}/agents/bookChat/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: this.messages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
          conversationId: this.conversationId,
          userId: this.userId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Remove loading message
      this.removeMessage(loadingId);

      // Stream response
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let assistantMessageId: string | null = null;
      let buffer = "";

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split("\n");
          buffer = lines.pop() || "";

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.substring(6);
              if (data === "[DONE]") continue;

              try {
                const parsed = JSON.parse(data);
                if (parsed.type === "text-delta" && parsed.textDelta) {
                  if (!assistantMessageId) {
                    assistantMessageId = this.addMessage("assistant", "");
                  }
                  this.updateMessage(assistantMessageId, parsed.textDelta);
                } else if (parsed.type === "finish") {
                  if (parsed.conversationId) {
                    this.conversationId = parsed.conversationId;
                  }
                }
              } catch (e) {
                // Ignore parse errors
              }
            }
          }
        }
      }
    } catch (error) {
      this.removeMessage(loadingId);
      this.addMessage("assistant", `Sorry, I encountered an error: ${error}`);
      console.error("Chat error:", error);
    }
  }

  private addMessage(role: "user" | "assistant", content: string): string {
    const message: ChatMessage = {
      role,
      content,
      timestamp: new Date(),
    };
    this.messages.push(message);

    const id = `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    const messagesContainer = document.getElementById("bookChatMessages");
    if (messagesContainer) {
      const messageEl = document.createElement("div");
      messageEl.className = `book-chat-message book-chat-message-${role}`;
      messageEl.id = id;
      messageEl.innerHTML = `
        <div class="book-chat-message-content">${this.escapeHtml(content)}</div>
        <div class="book-chat-message-time">${message.timestamp.toLocaleTimeString()}</div>
      `;
      messagesContainer.appendChild(messageEl);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    return id;
  }

  private updateMessage(id: string, additionalContent: string): void {
    const messageEl = document.getElementById(id);
    if (messageEl) {
      const contentEl = messageEl.querySelector(".book-chat-message-content");
      if (contentEl) {
        const currentContent = contentEl.textContent || "";
        contentEl.textContent = currentContent + additionalContent;
      }
      const messagesContainer = document.getElementById("bookChatMessages");
      if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
      }
    }
  }

  private removeMessage(id: string): void {
    const messageEl = document.getElementById(id);
    if (messageEl) {
      messageEl.remove();
    }
  }

  private escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  private showFeedbackDialog(): void {
    const message = prompt(
      "Please describe the issue or provide feedback:"
    );
    if (message) {
      this.submitFeedback(message);
    }
  }

  private async submitFeedback(feedback: string): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/api/feedback`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: feedback,
          userId: this.userId,
          pageUrl: window.location.href,
          context: this.messages
            .slice(-5)
            .map((m) => `${m.role}: ${m.content}`)
            .join("\n"),
        }),
      });

      if (response.ok) {
        alert("Thank you for your feedback! We'll review it and create a GitHub issue if needed.");
      } else {
        throw new Error("Failed to submit feedback");
      }
    } catch (error) {
      console.error("Feedback submission error:", error);
      alert("Sorry, we couldn't submit your feedback. Please try again later.");
    }
  }
}

// Auto-initialize if script is loaded
if (typeof window !== "undefined") {
  (window as any).BookChatWidget = BookChatWidget;
  
  // Auto-initialize if container exists
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("book-chat-widget");
    if (container) {
      const apiUrl = container.getAttribute("data-api-url") || "http://localhost:3141";
      new BookChatWidget("book-chat-widget", apiUrl);
    }
  });
}

export { BookChatWidget };

