// Connexion au serveur WebSocket
const wsSubmit = new WebSocket('ws://localhost:8080');
// Fonction appelée lorsque la connexion au serveur WebSocket est établie.
wsSubmit.onopen = function() {
};
// Fonction appelée lorsque le serveur envoie un message.
wsSubmit.onmessage = function(event) {
};
// Écouteur d'événement, quand le contenu du DOM est chargé.
document.addEventListener('DOMContentLoaded', function () {
  //L'élément de formulaire à écouter pour les événements de soumission.
  const form = document.querySelector('#post-form');

  if (form) {
    form.addEventListener('submit', function(event) {
      // Envoyer un message au serveur WebSocket
      if (wsSubmit.readyState === WebSocket.OPEN) {
        wsSubmit.send('Form submitted'); // Message pour notifier le serveur
      } else {
        console.error("WebSocket is not open. Cannot send message.");
      }
    });
  } else {
    console.error("Le formulaire #post-form n'a pas été trouvé dans le DOM.");
  }
});