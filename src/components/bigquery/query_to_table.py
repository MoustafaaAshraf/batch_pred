from pathlib import Path
from typing import Optional

from kfp.v2.dsl import component

from src.components.dependencies import GOOGLE_CLOUD_BIGQUERY, LOGURU, PYTHON


@component(
    base_image=PYTHON,
    packages_to_install=[GOOGLE_CLOUD_BIGQUERY, LOGURU],
    # output_component_file=str(Path(__file__).with_suffix(".yaml")),
)
def bq_query_to_table(
    query: str,
    bq_client_project_id: str,
    destination_project_id: str,
    dataset_id: str = Optional[None],
    table_id: str = Optional[None],
    dataset_location: str = "europe-west2",
    query_job_config: dict = Optional[None],
) -> None:
    """
    Run query and create a new BQ table.

    Args:
        query (str): SQL query to execute, results are saved in a BQ table.
        bq_client_project_id (str): Project ID that will be used by the BQ client.
        destination_project_id (str): Project ID where BQ table will be created.
        dataset_id (Optional[str], optional): Dataset ID where BQ table will be
            created. Defaults to None.
        table_id (Optional[str], optional): Table name (without project ID and
            dataset ID) that will be created. Defaults to None.
        dataset_location (str): BQ dataset location.
        query_job_config (dict): Dict containing optional parameters required
            by the bq query operation. No need to specify destination param.
            Defaults to None.
            See available parameters here
            https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.job.QueryJobConfig.html
    """
    from google.cloud import bigquery
    from google.cloud.exceptions import GoogleCloudError
    from loguru import logger

    if query_job_config is None:
        query_job_config = {}
    if (dataset_id is not None) and (table_id is not None):
        dest_table_ref = f"{destination_project_id}.{dataset_id}.{table_id}"
    else:
        dest_table_ref = None
    job_config = bigquery.QueryJobConfig(destination=dest_table_ref, **query_job_config)

    bq_client = bigquery.client.Client(
        project=bq_client_project_id, location=dataset_location
    )
    query_job = bq_client.query(query, job_config=job_config)

    try:
        _ = query_job.result()
        logger.info(f"BQ table {dest_table_ref} created.")
    except GoogleCloudError as e:
        logger.error(e)
        logger.error(query_job.error_result)
        logger.error(query_job.errors)
        raise e
