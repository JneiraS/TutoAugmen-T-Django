// Connexion au serveur WebSocket
const wsSubmit = new WebSocket('ws://localhost:8080');

wsSubmit.onopen = function() {
  console.log('Connected to WebSocket server on submit page');
};

wsSubmit.onmessage = function(event) {
  console.log('Message from server on submit page: ', event.data);
};

document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('#post-form');

  if (form) {
    form.addEventListener('submit', function(event) {
      console.log("Form submit button clicked");

      // Envoyer un message au serveur WebSocket
      if (wsSubmit.readyState === WebSocket.OPEN) {
        wsSubmit.send('Form submitted'); // Message pour notifier le serveur
        console.log("Message sent to WebSocket server.");
      } else {
        console.error("WebSocket is not open. Cannot send message.");
      }

      // Indiquer au serveur de rafraîchir la page 'statistics' via WebSocket
      if (wsSubmit.readyState === WebSocket.OPEN) {
        wsSubmit.send('refresh-statistics'); // Demande de rafraîchissement
      }

      // Utiliser un délai pour permettre l'envoi avant de rediriger
      setTimeout(function() {
        console.log("Redirecting to statistics page...");
        window.location.href = 'http://127.0.0.1:8000/polls/statistics/'; // Rediriger vers la page statistics
      }, 500); // Délai de 500ms pour garantir que le message soit envoyé avant redirection
    });
  } else {
    console.error("Le formulaire #post-form n'a pas été trouvé dans le DOM.");
  }
});
