# TDF_Innovation


## Extraction des métadonnées

### Datahub

Le dossier datahub comporte toutes les images nécessaires pour déployer datahub en local ( on peut se baser sur le readme du dossier ), ainsi que toutes les fonctions qu'on utilise pour construire les sondes (qui sont plutôt dans le sous-dossier metadata-ingestion). Pour utiliser ces fonctions il faudra installer les librairies du setup.py du dossier metadata_ingestion.

Pour déployer datahub en local, il suffit de se placer dans le dossier datahub/docker/ et lancer la commande ./quickstart.sh depuis le terminal.

La documentation officielle de Datahub est disponible ici: https://datahubproject.io/docs/

### Ingestion en mode push: sondes

Le dossier sample_pipeline comporte un exemple de pipeline de transformation de données. C'est sur cet exemple qu'on essaie de tester notre sonde.

Le dossier sondes comporte les sondes qu'on a construites, qu'on peut retrouver dans le sous dossier use_case.

Ces sondes ont été conçues pour envoyer les métadonnées extraites ( depuis une pipeline de traitement de données par exemple ) à la plateforme Datahub

#### 1 - Sondes d'ingestion d'une pipeline de traitement de données:

Pour tester une extraction via ces sondes, il suffit de faire appel à la sonde dans un use case de la pipeline, par exemple:

* Dans sample_pipeline/usecase/orchestrate_pipeline.py on peut importer la sonde ingest_dataset et l'appeler dans la fonction construct_temporal_trace_refined_table_from_rousset_fdc_data

Ensuite, il faudra lancer l'application qui gère la pipeline et faire un GET ou un POST sur la route sur laquelle est exposé le use_case.

Finalement, pour visualiser les résultats de l'extraction de ces métadonnées, on peut les retrouver dans l'interface datahub, disponible sur localhost:9002 ( ou localhost:9001 ), en supposant qu'on a déjà déployé Datahub en local.

#### 2 - Sondes d'ingestion d'une pipeline de Machine Learning:

Des exemples de pipeline de Machine Learning sont disponibles dans le dossier sample_pipeline/machine_learning_pipeline. Il suffit d'exécuter le fichier python de la pipeline depuis le terminal pour lancer la pipeline.

La sonde qui s'occupe de l'ingestion des modèles de Machine Learning est présente dans le fichier src/use_case/ingest_model.

On peut la tester à l'instar des sondes de pipeline de traitement des données. Les résultats seront présents dans le fichier PROD/machine_learning dans la UI de Datahub.

On peut également réaliser l'ingestion dans l'outil DataGalaxy qui permet de faire du cataloguing de données.

Pour ce faire, on peut utiliser par exemple la sonde présente dans le fichier usecase/ingest_dataset_in_datagalaxy.py et suivre les mêmes étapes concernant les sondes de type Datahub. La documentation officielle de l'API de Datagalaxy est disponible ici : https://api.datagalaxy.com/v2/documentation/beta

NB: Pour pouvoir tester l'ingestion et la visualiser sur Datagalaxy, il faut avoir un token d'integration au projet Datagalaxy en question au préalable. Il faudra aussi rajouter ce token aux variables d'environnement pour que les tests d'intégration fonctionnent correctement.


### Ingestion en mode pull: connecteurs


Les exemples de sondes qu'on a illustré servent à faire de l'ingestion de métadonnées à partir d'une pipeline dans une approche Push.

Il est cependant possible aussi de réaliser de l'ingestion de métadonnées en mode pull grâce à Datahub. En effet, Datahub fournit plusieurs sources de métadonnées, en créant un connecteur pour chaque source ( qu'on peut retrouver dans le dossier sources dans /datahub/metadata_ingestion/).

Un schéma qui explique les différentes approches Pull/Push et les différentes méthodes d'ingestion que propose Datahub est disponible

ici : https://datahubproject.io/docs/architecture/metadata-ingestion/

#### Connecteur MlFlow

L'un des aspects qu'on a creusé durant notre projet c'est l'injection des métadonnées de machine learning depuis un server mlflow, dans une approche Pull. Pour ce faire on a développé un nouveau connecteur mlflow sur Datahub ( MlFlowSource ) qui permettra de faire la connexion à un server mlflow et récupérer les métadonnées qui nous intéressent, selon le modèle de métadonnées qu'on a fixé. 

Pour illustrer cette ingestion en pull, on peut monter un server mlflow ( généralement dans le localhost:5000) et créer des expériences dessus. Ensuite il suffit de créer la bonne configuration de la pipeline d'ingestion (un exemple est donné dans le fichier datahub/docker/ingestion/sample_recipe.yml) et lancer la commande suivante depuis le terminal :

`datahub ingest -c datahub/docker/ingestion/sample_recipe.yml`



- Pour l'instant on ne pourra pas visualiser les résultats sur Datahub car l'affichage des modèles ML est toujours en cours de développement de leur côté. Cependant on pourra visualiser les logs au niveau du terminal pour s'assurer que l'ingestion s'est bien déroulée.

- On peut également choisir notre console ou un fichier de notre choix où on pourra répertorier les résultats de l'ingestion, il suffit de changer la configuration du fichier sample_recipe.yml.

- Pour bien voir les résultats de l'ingestion il faut s'assurer que les nouvelles experiments qu'on a créé côté mlflow ne se retrouvent pas dans la Default experiment de mlflow, car on filtre sur cette dernière au niveau du connecteur.

- Pour exploiter ce connecteur on a créé un exemple de cron qui tourne chaque jour pour récupérer les métadonnées générées par MlFlow et les ingérer sur Datahub. L'exemple est disponible dans le fichier cron/mlflow_pull_ingestion. On pourra configurer ce cron selon notre besoin d'ingestion.


### Déploiement


Concernant le déploiement, on a packagé le dossier sondes et on a choisi tox comme techno pour gérer les tests. La documentation de tox est disponible ici: https://tox.readthedocs.io/en/latest/. 

Les fonctions de datahub qu’on utilise ont été importées du repository https://github.com/linkedin/datahub. 

On a également mis en place une CI sur gitlab, où on lance principalement les tests unitaires et les tests d’intégration. 


## Deduplication:

Le dossier deduplicate contient un ensemble de fichier .py representant les différentes étapes à effectuer pour faire une déduplication sur un dataset. Ces étapes sont explicitées dans les deux notebooks d'exemple du dossier notebooks. Ils montrent un exemple d'utilisation de recordlinkge sur les données febrl et d'autres données d'usines.

Dans le dossier local_deps on retrouve les dépendances nécessaires pour lancer les notebooks, notamment les outils shapash et codecarbon. Pour voir les résultats de codecarbon il suffit de se placer dans le dossier ou est stocké le fichier emissions.csv puis de lancer la commande carbonboard --filepath="emissions.csv".

Le dossier notebook/streamlit contient tous les élements nécessaires pour lancer la model_card. Pour afficher la model card il suffit de se placer dans le dossier streamlit et lancer la commande streamlit run model_card.py.
