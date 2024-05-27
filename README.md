# Chat Killer Project

## Informations Générales

- **Prénom:** Marius
- **Date de début:** 17/04/2024
- **Date de fin:** 12/05/2024
- **Groupe:** Devoir effectué seul
- **Note obtenue lors de la démo de projet:** 14/20
- **Auto-évaluation:** 17/20

## Fonctionnalités

- **Commandes disponibles:**
  - `!start`
  - `!list` (avec état: vivant, mort)
  - `@pseudo !ban` (avec mise à jour de `!list` en temps réel)
- **Messages:**
  - Public
  - Privé
  - Admin

## Lancement

Pour démarrer le serveur:

> python3 chat_killer_server.py 1111

Pour démarrer le client:

> python3 chat_killer_client.py 127.0.0.1 1111

Versions
Versions stables: 4
Versions instables: 2
La version finale soumise est stable et permet de constater l'évolution entre le début et la fin du projet. Un fichier Readme.md est également disponible dans la version stable_v1 du projet.

Impressions Personnelles
J'ai pris goût à travailler sur ce projet depuis le début. Il s'agit du premier vrai devoir concret et utile que j'ai réalisé depuis le début de ma licence. J'ai appris à gérer des erreurs, comprendre plus en détail des concepts systèmes grâce à la programmation Python. De plus, j'ai réussi à être cohérent dans mon code et bien m'organiser de manière à rendre des problèmes complexes en sous-problèmes afin de rendre la réalisation du projet plus simple.

J'ai utilisé des ressources des TP et TD, le site Stack Overflow ainsi que de l'entraide entre étudiants du même groupe. Mes parties préférées ont été la gestion des messages publics et privés ainsi que la commande !start du modérateur. Mes regrets sont de ne pas avoir été plus loin avec la tolérance aux pannes côté client et les cookies. J'ai eu du mal à aborder la lecture des messages depuis le FIFO avec pas mal de bugs et retouches et aussi pour écouter les entrées du serveur dont la solution a été de démarrer un thread.

Améliorations Post-Démo
J'ai pu améliorer la commande !list et coder les fonctions !start et @pseudo !ban entre la démo et le rendu.

Remerciements
Merci,

En espérant que tout fonctionne bien pour vous.
