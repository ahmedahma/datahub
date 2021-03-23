from fastapi import FastAPI
from sample_pipeline.usecase.orchestrate_pipeline import construct_temporal_trace_refined_table_from_rousset_fdc_data

app = FastAPI()


@app.get("/fdc_rousset_temporal_traces")
async def fdc_rousset_temporal_traces():
    """
    Transform rousset data to extract temporal traces.

    This will let the API user (some external developer) launch a job for this extraction.

    And this path operation will:

    * Load test dump files (with no parameter yet).
    * Apply transformations on rawd ata.
    * Send a notification back to the API user, as a return.
        * At this point the return corresponds to the total temporal traces generated
    """
    temporal_traces = construct_temporal_trace_refined_table_from_rousset_fdc_data()
    state = 'Total {temporal_traces} temporal traces have been parsed'.format(
        temporal_traces=len(temporal_traces)
    )
    return {
        "message": str(state)

    }
