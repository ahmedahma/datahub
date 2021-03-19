[DOCUMENT EN CONSTRUCTION]

Ce document a pour objectif de référencer les pratiques de développement conventionnelles pour le projet TDF INnovation.
En cours de construction, y sont répertoriés les choix que nous faisons en tant qu'équipe de développement

***

# 1. Git


- [Trello](https://trello.com/b/cVeAOlWg/tdf-innovation) est utilisé pour référencer des tâches de développement.
- Pour chaque ticket, une branche est créée et peut être mergée sur master après une review par un membre de l'équipe.


***

# 2. Conception

#### Clean Archi :

Arborescence dans le projet où la logique métier se retrouve dans les dossiers 'domain', la logique purement technique 
dans l' 'infrastrcuture' et le croisement des logiques dans le dossier 'usecase'. 

### Typage :

Par défaut, les méthodes et variables sont décrites par type hitting.
Un typage plus fort peut être mis en place sur les APIs.
