// websocket-server.js
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 8080 });

// Lorsqu'un client se connecte
wss.on("connection", function connection(ws) {
  // Lorsqu'un message est reçu
  ws.on("message", function incoming(message) {
    console.log("received: %s", message);

    // Envoyer le message reçu à tous les clients connectés
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message); // Relayer le message
      }
    });
  });

  // Envoyer un message de bienvenue
  ws.send("Connection established");
});

console.log("WebSocket server is running on ws://localhost:8080");
