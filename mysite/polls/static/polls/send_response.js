// Connexion au serveur WebSocket
const wsSubmit = new WebSocket('ws://localhost:8080');

wsSubmit.onopen = function() {
  console.log('Connected to WebSocket server on submit page');
};

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('post-form');
    
    form.addEventListener('submit', function(e) {
        //e.preventDefault(); // commenter pour valider le formulaire
        const selectedChoice = document.querySelector('input[name="choice"]:checked');
        if (selectedChoice) {
            console.log('Le choix sélectionné est:', selectedChoice.value);
            
            // Envoie le choix au serveur via WebSocket
            if (wsSubmit.readyState === WebSocket.OPEN) {
                wsSubmit.send(selectedChoice.value);
            } else {
                console.error("WebSocket is not open. Cannot send message.");
            }
            // Redirige vers la page des résultats
            //window.location.href = window.location.href.replace('vote', 'results');
        } else {
            console.log('Aucun choix n\'est sélectionné.');
        }
    });
});