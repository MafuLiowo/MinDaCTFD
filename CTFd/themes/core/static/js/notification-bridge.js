(function () {
  const NativeEventSource = window.EventSource;

  if (!NativeEventSource || !window.SharedWorker) {
    return;
  }

  const root = String(window.init?.urlRoot || "").replace(/\/$/, "");
  const isAuthenticated = Number(window.init?.userId) > 0;
  const workerUrl =
    root + "/themes/core/static/js/notification-worker.js?v=5";

  class SharedEventSource {
    constructor(url, options) {
      this.url = new URL(url, window.location.href).href;
      this.withCredentials = Boolean(options?.withCredentials);
      this.readyState = 0;
      this.onopen = null;
      this.onerror = null;
      this.onmessage = null;

      this._active = false;
      window.__CTFD_EVENT_BRIDGE_STATE__ = {
        status: "created",
        workerUrl: workerUrl,
      };
      this._listeners = {
        open: [],
        error: [],
        message: [],
        notification: [],
      };

      this._worker = new SharedWorker(workerUrl, {
        name: "ctfd-notification-stream",
      });
      this._port = this._worker.port;
      this._port.onmessage = (event) => this._handleWorkerMessage(event);
      this._port.start();
      this._port.postMessage({
        type: "init",
        eventsUrl: this.url,
      });
    }

    addEventListener(type, listener, options) {
      if (!listener || !this._listeners[type]) {
        return;
      }

      if (!this._listeners[type].includes(listener)) {
        this._listeners[type].push(listener);
      }

      if (type === "notification") {
        this._active = true;
        window.__CTFD_EVENT_BRIDGE_STATE__ = {
          status: "active",
          workerUrl: workerUrl,
        };
      }
    }

    removeEventListener(type, listener) {
      if (!this._listeners[type]) {
        return;
      }

      this._listeners[type] = this._listeners[type].filter(
        (candidate) => candidate !== listener,
      );
    }

    close() {
      this._active = false;
      this.readyState = SharedEventSource.CLOSED;

      for (const type of Object.keys(this._listeners)) {
        this._listeners[type] = [];
      }
    }

    _dispatch(type, event) {
      const handler = this["on" + type];

      if (typeof handler === "function") {
        handler.call(this, event);
      }

      for (const listener of this._listeners[type] || []) {
        if (typeof listener === "function") {
          listener.call(this, event);
        } else if (listener?.handleEvent) {
          listener.handleEvent(event);
        }
      }
    }

    _handleWorkerMessage(messageEvent) {
      const message = messageEvent.data;

      if (message?.type === "ready") {
        window.__CTFD_EVENT_BRIDGE_STATE__ = {
          status: "worker-ready",
          workerUrl: workerUrl,
        };
        return;
      }

      if (message?.type === "status") {
        window.__CTFD_EVENT_BRIDGE_STATE__ = {
          status: message.status,
          workerUrl: workerUrl,
          detail: message.detail || null,
        };

        if (message.status === "open") {
          this.readyState = SharedEventSource.OPEN;
          this._dispatch("open", new Event("open"));
        } else if (message.status === "error") {
          this.readyState = SharedEventSource.CONNECTING;
          this._dispatch("error", new Event("error"));
        }
        return;
      }

      if (message?.type !== "notification" || !this._active) {
        return;
      }

      const event = new MessageEvent("notification", {
        data: JSON.stringify(message.data),
        origin: window.location.origin,
      });

      this._dispatch("notification", event);
      this._dispatch("message", event);
    }
  }

  SharedEventSource.CONNECTING = 0;
  SharedEventSource.OPEN = 1;
  SharedEventSource.CLOSED = 2;

  function EventSourceBridge(url, options) {
    const pathname = new URL(url, window.location.href).pathname;

    if (
      !pathname.endsWith("/events") ||
      !window.SharedWorker ||
      !isAuthenticated
    ) {
      return new NativeEventSource(url, options);
    }

    return new SharedEventSource(url, options);
  }

  EventSourceBridge.CONNECTING = 0;
  EventSourceBridge.OPEN = 1;
  EventSourceBridge.CLOSED = 2;

  window.EventSource = EventSourceBridge;
})();
