var ws = require("nodejs-websocket");

// Crée un serveur WebSocket sur le port 8089
var server = ws.createServer(function(conn) {

    console.log("Nouvelle connexion");

    // Réception d'un message texte
    conn.on("text", function(msg) {
      console.log("Texte reçu : " + msg);
      // Envoi d'un message de bienvenue
      if (msg == "hello") {
        conn.send("Bonjour, comment puis-je vous aider ?");
      }
      // Envoi de la date actuelle
      else if (msg == "date") {
        conn.send(new Date().toString());
      }
      // Envoi d'un message relatif à la météo
      else if (msg == "meteo") {
        conn.send("Il suffit de regarder dehors pour avoir une idée du temps qu'il fait");
      }
      // Envoi d'un message pour demander comment va le serveur
      else if (msg == "comment ca va") {
        conn.send("Ça va bien, merci !");
      }
      // Envoi d'un message pour demander qui est le serveur
      else if (msg == "qui es-tu") {
        conn.send("Je suis un serveur WebSocket, ici pour répondre à vos questions !");
      }
      // Envoi d'un message pour demander le nom du serveur
      else if (msg == "quel est ton nom") {
        conn.send("Je n'ai pas de nom, mais vous pouvez m'appeler 'Serveur'.");
      }
      // Envoi d'un message pour demander le prénom du serveur
      else if (msg == "comment tu t'appelles") {
        conn.send("Je n'ai pas de prénom, mais vous pouvez me considérer comme 'le serveur'.");
      }
      // Envoi d'un message pour demander une blague
      else if (msg == "joke") {
        conn.send("Pourquoi les plongeurs plongent-ils toujours en arrière et jamais en avant ? Parce que sinon ils tombent toujours dans le bateau !");
      }
      // Envoi d'un message pour prendre  quitter
      else if (["bye", "ciao"].includes(msg)) {
        conn.send("Au revoir !");
        // Ferme la connexion
        conn.close();

      }
      else conn.sendText("Désolé, je n'ai pas compris votre demande !");
    });

    // Fermeture de connexion
    conn.on("close", function(code, reason) {
        console.log("Connexion fermée");
    });

    // En cas d'erreur
    conn.on("error", function(err) {
      console.log(err);
    });

}).listen(8089);