# TDF_Innovation

Le dossier datahub comporte toutes les images nécessaires pour déployer datahub en local ( on peut se baser sur le readme du dossier ), ainsi que toutes les fonctions qu'on utilise pour construire les sondes (qui sont plutôt dans le sous-dossier metadata-ingestion). Pour utiliser ces fonctions il faudra installer les librairies du setup.py du dossier metadata_ingestion.

**Extractionn des méta données:**

Pour déployer datahub en local, il suffit de se placer dans le dossier datahub et lancer la commande ./quickstart.sh depuis le terminal.

La documentation officielle de Datahub est disponible ici: https://datahubproject.io/docs/

Le dossier sample_pipeline comporte un exemple de pipeline de transformation de données. C'est sur cet exemple qu'on essaie de tester notre sonde.

Le dossier sondes comporte les sondes qu'on a construites, qu'on peut retrouver dans le sous dossier use_case.

Ces sondes ont été conçues pour envoyer les métadonnées extraites ( depuis une pipeline de traitement de données par exemple ) à la plateforme Datahub

1 - Sondes d'ingestion d'une pipeline de traitement de données:

Pour tester une extraction via ces sondes, il suffit de faire appel à la sonde dans un use case de la pipeline, par exemple:

* Dans sample_pipeline/usecase/orchestrate_pipeline.py on peut importer la sonde ingest_dataset et l'appeler dans la fonction construct_temporal_trace_refined_table_from_rousset_fdc_data

Ensuite, il faudra lancer l'application qui gère la pipeline et faire un GET ou un POST sur la route sur laquelle est exposé le use_case

Finalement, pour visualiser les résultats de l'extraction de ces métadonnées, on peut les retrouver dans l'interface datahub, disponible sur localhost:9002 ( ou localhost:9001 ), en supposant qu'on a déjà déployé Datahub en local.

2 - Sondes d'ingestion d'une pipeline de Machine Learning:

Des exemples de pipeline de Machine Learning sont disponibles dans le dossier sample_pipeline/machine_learning_pipeline. Il suffit d'exécuter le fichier python de la pipeline depuis le terminal pour lancer la pipeline.

La sonde qui s'occupe de l'ingestion des modèles de Machine Learning est présente dans le fichier src/use_case/ingest_model.

On peut la tester à l'instar des sondes de pipeline de traitement des données. Les résultats seront présents dans le fichier PROD/machine_learning dans la UI de Datahub.

 
On peut également réaliser l'ingestion dans l'outil DataGalaxy qui permet de faire du cataloguing de données.

Pour ce faire, on peut utiliser par exemple la sonde présente dans le fichier usecase/ingest_dataset_in_datagalaxy.py
 
et suivre les mêmes étapes concernant les sondes de type Datahub. La documentation officielle de l'API de Datagalaxy

est disponible ici : https://api.datagalaxy.com/v2/documentation/beta

NB: Pour pouvoir tester l'ingestion et la visualiser sur Datagalaxy, il faut avoir un token d'integration au projet

Datagalaxy en question au préalable. Il faudra aussi rajouter ce token aux variables d'environnement pour que les tests

d'intégration fonctionnent correctement.

**Deduplication:**

Le dossier deduplicate contient un ensemble de fichier .py representant les différentes étapes à effectuer pour faire une déduplication sur un dataset. Ces étapes sont explicitées dans les deux notebooks d'exemple du dossier notebooks. Ils montrent un exemple d'utilisation de recordlinkge sur les données febrl et d'autres données d'usines.

Dans le dossier local_deps on retrouve les dépendances nécessaires pour lancer les notebooks, notamment les outils shapash et codecarbon. Pour voir les résultats de codecarbon il suffit de se placer dans le dossier ou est stocké le fichier emissions.csv puis de lancer la commande carbonboard --filepath="emissions.csv".

Le dossier notebook/streamlit contient tous les élements nécessaires pour lancer la model_card. Pour afficher la model card il suffit de se placer dans le dossier streamlit et lancer la commande streamlit run model_card.py.
