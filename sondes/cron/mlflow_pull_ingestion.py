import schedule

from datahub.ingestion.run.pipeline import Pipeline


def mlflow_pull_ingestion():
    pipeline = Pipeline.create(
        {
            "source": {
                "type": "mlflow",
                "config": {
                    'tracking_uri': 'localhost:5000'
                },
            },
            "sink": {
                "type": "datahub-rest",
                "config": {"server": "http://localhost:8080"},
            },
        }
    )
    pipeline.run()
    pipeline.raise_from_status()
    pipeline.pretty_print_summary()


def mlflow_pull_ingestion_cron():
    schedule.every().day.do(mlflow_pull_ingestion)
    while True:
        schedule.run_pending()
