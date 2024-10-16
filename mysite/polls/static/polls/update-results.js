// Client WebSocket sur la page statistics
const wsStatistics = new WebSocket('ws://localhost:8080');


wsStatistics.onopen = function() {
  console.log('Connected to WebSocket server on statistics page');
};

wsStatistics.onmessage = function(event) {
  // Vérifie si le message est un Blob
  if (event.data instanceof Blob) {
    const reader = new FileReader();

    // Quand la lecture est terminée, le contenu est dans reader.result
    reader.onload = function() {
      const message = reader.result; // Contenu du Blob converti en texte
      console.log('Message from server on statistics page (b): ', message);
    };
    // Lire le Blob en tant que texte
    reader.readAsText(event.data);
  } else {
    // Si le message n'est pas un Blob, le traiter directement comme texte
    const message = event.data;
    console.log('Message from server on statistics page (nb): ', message);

    // Si le message est "refresh-statistics", on rafraîchit la page
    if (message === 'refresh-statistics') {
      console.log("Refreshing statistics page...");
      location.reload(true); // Rafraîchit la page
    }
  }
};
