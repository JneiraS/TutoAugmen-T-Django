// websocket-server.js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', function connection(ws) {
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
    ws.send('Hello from server');
  });

  ws.send('Connection established');
});

console.log('WebSocket server is running on ws://localhost:8080');