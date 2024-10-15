const socket = new WebSocket('ws://localhost:8080');

socket.onopen = function() {
  console.log('Connected to WebSocket server');
};

socket.onmessage = function(event) {
  console.log('Message from server ', event.data);
};

socket.onclose = function() {
  console.log('WebSocket connection closed');
};
