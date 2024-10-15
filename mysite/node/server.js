const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('../db.sqlite3');

// websocket-server.js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

// Lorsqu'un client se connecte
wss.on('connection', function connection(ws) {
  // Lorsqu'un message est reçu
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
    // Envoyer un message à tous les clients connectés
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  });

  // Envoyer un message de bienvenue
  ws.send('Connection established');
});

// Vérifier les nouvelles données toutes les 5 secondes
setInterval(() => {
  db.all('SELECT * FROM polls_question', (err, rows) => {
    if (err) {
      console.error(err);
    } else {
      wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(rows));
        }
      });
    }
  });
}, 5000);

console.log('WebSocket server is running on ws://localhost:8080');