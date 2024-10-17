// Connexion au serveur WebSocket
const wsSubmit = new WebSocket('ws://92.134.222.0:8089');

// Fonction appelée lorsque la connexion au serveur WebSocket est établie.
wsSubmit.onopen = function() {
  console.log('Connected to WebSocket server on submit page');
};
// Fonction appelée lorsque le document est chargé.
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le formulaire avec l'ID "post-form".
    const form = document.getElementById('post-form');
    // Ajouter un gestionnaire d'évènement pour le formulaire.
    form.addEventListener('submit', function(e) {
        //e.preventDefault();
        // Récupérer la valeur de la case à cocher sélectionnée.
        const selectedChoice = document.querySelector('input[name="choice"]:checked');
        if (selectedChoice) {
            // Envoie le choix au serveur via WebSocket
            if (wsSubmit.readyState === WebSocket.OPEN) {
                wsSubmit.send(selectedChoice.value);
            } else {
                console.error("WebSocket is not open. Cannot send message.");
            }
        } else {
            console.log('Aucun choix n\'est sélectionné.');
        }
    });
});