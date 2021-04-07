# TDF_Innovation

Le dossier datahub comporte toutes les images nécessaires pour déployer datahub en local ( on peut se baser sur le readme du dossier ), ainsi que toutes les fonctions qu'on utilise pour construire les sondes ( qui sont plutôt dans le sous-dossier metadata-ingestion).

Le dossier sample_pipeline comporte un exemple de pipeline de transformation de données. C'est sur cet exemple qu'on essaie de tester notre sonde.

Le dossier sondes comporte les sondes qu'on a construites, qu'on peut retrouver dans le sous dossier use_case.

Ces sondes ont été conçues pour envoyer les métadonnées extraites ( depuis une pipeline de traitement de données par exemple ) à la plateforme Datahub

Pour tester une extraction via ces sondes, il suffit de faire appel à la sonde dans un use case de la pipeline, par exemple:

* Dans sample_pipeline/usecase/orchestrate_pipeline.py on peut importer la sonde ingest_dataset et l'appeler dans la fonction construct_temporal_trace_refined_table_from_rousset_fdc_data

Ensuite, il faudra lancer l'application qui gère la pipeline et faire un GET ou un POST sur la route sur laquelle est exposé le use_case

Finalement, pour visualiser les résultats de l'extraction de ces métadonnées, on peut les retrouver dans l'interface datahub, disponible sur localhost:9002 ( ou localhost:9001 ), en supposant qu'on a déjà déployé Datahub en local.