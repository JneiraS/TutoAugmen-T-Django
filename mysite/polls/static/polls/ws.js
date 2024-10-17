// Client WebSocket sur la page statistics
const wsStatistics = new WebSocket("ws://92.134.222.0:8089");
// Fonction appelée lorsque la connexion au serveur WebSocket est établie.
wsStatistics.onopen = function () {};
// Fonction appelée lorsque le serveur envoie un message.
wsStatistics.onmessage = function (event) {
  // Vérifie si le message est un Blob
  if (event.data instanceof Blob) {
    const reader = new FileReader();




    // Quand la lecture est terminée, le contenu est dans reader.result
    reader.onload = function () {
      const message = reader.result; // Contenu du Blob converti en texte
       const actualNotification = parseInt(document.querySelector(`.notification`).innerHTML
      );
      document.querySelector(`.notification`).innerHTML += "<li> Notifications: " + message  + "</li>";
    };

    // Lire le Blob en tant que texte
    reader.readAsText(event.data);
  }
};