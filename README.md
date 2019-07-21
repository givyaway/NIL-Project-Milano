# NIL-Project-Milano

Progetto interattivo per valutare le zone (i.e. Nuclei di Identità Locale) della città di Milano tramite voto degli utenti.

Il progetto è basato su un Frontend per renderizzare la mappa della città e mostrare le categorie di voto e un semplicissimo Backend per elaborare e salvare le informazioni.

Scopo del progetto è fornire un rating alle zone che compongono Milano ottenendo così una colorazione finale della mappa basata sulla media voti della zona. I colori delle zone saranno gradazioni dei seguenti valori:

* Rosso = Pessimo
* Verde = Ottimo

Le categorie di voto per ogni zona riguardano:

* Rapporto qualità della zona / prezzo degli immobili
* Servizi disponibili, clima e ambiente
* Cultura e tempo libero
* Sicurezza e vivibilità della zona

Le uniche informazioni richieste agli utenti per poter votare è il loro indirizzo IP, ottenuto da una API esterna (https://api.ipify.org).
L'IP serve a poter identificare il voto di ogni utente e ad evitare che uno stesso utente possa votare piu volte la stessa zona.

_Frontend_

* HTML + CSS
* Bootstrap
* JQuery
* Openlayers
* Rateit.js

_Backend_

* Python
* Flask

Infine, lo script in python update_votes si occuperà di aggiornare periodicamente i files riguardanti la media voti di ogni NIL e il geojson della mappa.
