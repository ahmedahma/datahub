# TDF_Innovation

Extractionn des méta données:

Le dossier datahub comporte toutes les images nécessaires pour déployer datahub en local ( on peut se baser sur le readme du dossier ), ainsi que toutes les fonctions qu'on utilise pour construire les sondes ( qui sont plutôt dans le sous-dossier metadata-ingestion).

Pour déployer datahub en local, il suffit de se placer dans le dossier datahub et lancer la commande ./quickstart.sh depuis le terminal.

Le dossier sample_pipeline comporte un exemple de pipeline de transformation de données. C'est sur cet exemple qu'on essaie de tester notre sonde.

Le dossier sondes comporte les sondes qu'on a construites, qu'on peut retrouver dans le sous dossier use_case.

Ces sondes ont été conçues pour envoyer les métadonnées extraites ( depuis une pipeline de traitement de données par exemple ) à la plateforme Datahub

Pour tester une extraction via ces sondes, il suffit de faire appel à la sonde dans un use case de la pipeline, par exemple:

* Dans sample_pipeline/usecase/orchestrate_pipeline.py on peut importer la sonde ingest_dataset et l'appeler dans la fonction construct_temporal_trace_refined_table_from_rousset_fdc_data

Ensuite, il faudra lancer l'application qui gère la pipeline et faire un GET ou un POST sur la route sur laquelle est exposé le use_case

Finalement, pour visualiser les résultats de l'extraction de ces métadonnées, on peut les retrouver dans l'interface datahub, disponible sur localhost:9002 ( ou localhost:9001 ), en supposant qu'on a déjà déployé Datahub en local.

Deduplication

Le dossier deduplicate contient un ensemble de fichier .py qui representent les différentes étapes 
à effectuer pour faire une déduplication sur un dataset.
Ces étapes sont explicitées dans les deux notebook d'exemples du dossier 
notebooks. Les notebooks montrent un exemple d'utilisation de recordlinkge sur les données 
febrl fournies par l'outil et d'autres données d'usines présents dans le dossier data.

Pour déployer datahub en local, il suffit de se placer dans le dossier datahub et lancer la commande ./quickstart.sh depuis le terminal.

Le dossier sample_pipeline comporte un exemple de pipeline de transformation de données. C'est sur cet exemple qu'on essaie de tester notre sonde.

Le dossier notebook/streamlit contient tous les élements nécessaires pour 
lancer la model_card. Pour afficher la model card deux solutions sont possibles :
- Se placer dans le dossier streamlit et lancer la commande suivante : streamlit run model_card.py


Le dossier sondes comporte les sondes qu'on a construites, qu'on peut retrouver dans le sous dossier use_case.

Ces sondes ont été conçues pour envoyer les métadonnées extraites ( depuis une pipeline de traitement de données par exemple ) à la plateforme Datahub

Pour tester une extraction via ces sondes, il suffit de faire appel à la sonde dans un use case de la pipeline, par exemple:

* Dans sample_pipeline/usecase/orchestrate_pipeline.py on peut importer la sonde ingest_dataset et l'appeler dans la fonction construct_temporal_trace_refined_table_from_rousset_fdc_data

Ensuite, il faudra lancer l'application qui gère la pipeline et faire un GET ou un POST sur la route sur laquelle est exposé le use_case

Finalement, pour visualiser les résultats de l'extraction de ces métadonnées, on peut les retrouver dans l'interface datahub, disponible sur localhost:9002 ( ou localhost:9001 ), en supposant qu'on a déjà déployé Datahub en local.

Le dossier **notebooks** comprennent les notebooks pour tester les outils recordlinkage
et holoclean en utilisant les données présents dans le dossier **data**.

Dans le dossier **local_deps** on retrouve les dépendances nécessaires pour tester
les outils, notament les outils shapash et codecarbon.

Le dossier **streamlit** contient tous les élements nécessaires pour 
lanceer la model_card. Pour afficher la model card, il faut se placer dans le dossier streamlit
et lancer la commande streamlit run model_card.py. Il est possible de lancer la 
model card sans se déplacer dans le dossier en lançant la commande
streamlit run wher_you_are/notebooks/streamlit/model_card.py 
