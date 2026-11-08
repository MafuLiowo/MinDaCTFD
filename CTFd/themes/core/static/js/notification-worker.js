"use strict";

const ports = new Set();

let source = null;
let eventUrl = null;
let reconnectDelay = 2000;
let reconnectTimer = null;

function send(port, message) {
  try {
    port.postMessage(message);
  } catch (error) {
    ports.delete(port);
  }
}

function broadcast(message) {
  for (const port of [...ports]) {
    send(port, message);
  }
}

function connect() {
  if (!eventUrl || ports.size === 0) {
    return;
  }

  if (source) {
    if (source.readyState !== EventSource.CLOSED) {
      return;
    }

    source = null;
  }

  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }

  broadcast({ type: "status", status: "connecting" });

  try {
    source = new EventSource(eventUrl);
  } catch (error) {
    source = null;
    broadcast({
      type: "status",
      status: "source-error",
      detail: String(error),
    });

    if (!reconnectTimer) {
      reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        connect();
      }, reconnectDelay);
      reconnectDelay = Math.min(reconnectDelay * 2, 30000);
    }
    return;
  }

  source.addEventListener("open", () => {
    reconnectDelay = 2000;
    broadcast({ type: "status", status: "open" });
  });

  source.addEventListener("notification", (event) => {
    let data;

    try {
      data = JSON.parse(event.data);
    } catch (error) {
      console.error("Invalid notification payload", error);
      return;
    }

    broadcast({
      type: "notification",
      data: data,
    });
  });

  source.addEventListener("error", () => {
    broadcast({ type: "status", status: "error" });

    source?.close();
    source = null;

    if (!reconnectTimer && ports.size > 0) {
      reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        connect();
      }, reconnectDelay);
      reconnectDelay = Math.min(reconnectDelay * 2, 30000);
    }
  });
}

function disconnectIfIdle() {
  if (ports.size === 0 && source) {
    source.close();
    source = null;
  }

  if (ports.size === 0 && reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
}

self.onconnect = (event) => {
  const port = event.ports[0];

  ports.add(port);
  port.start();
  send(port, { type: "ready" });

  port.onmessage = (messageEvent) => {
    const message = messageEvent.data;

    if (message?.type === "init" && message.eventsUrl) {
      eventUrl = message.eventsUrl;
      connect();
    }

    if (message?.type === "disconnect") {
      ports.delete(port);
      port.close();
      disconnectIfIdle();
    }
  };
};
