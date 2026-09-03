import logging
import os
import tempfile
import azure.functions as func
from azure.storage.blob import BlobServiceClient

from src.pipeline import load_data, clean_data, merge_data, save_to_duckdb


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="refresh-pipeline", methods=["POST"])
def refresh_pipeline(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to trigger the ETL pipeline refresh.
    """

    logging.info("Azure Function: Starting pipeline refresh.")

    try:
        # Download source datasets from Azure Blob Storage
        connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
        blob_service = BlobServiceClient.from_connection_string(connection_string)
        container = blob_service.get_container_client("raw-data")

        temp_dir = tempfile.gettempdir()
        retail_path = os.path.join(temp_dir, "online_retail_II.csv")
        crm_path = os.path.join(temp_dir, "crm_customers.csv")

        with open(retail_path, "wb") as f:
            f.write(container.download_blob("online_retail_II.csv").readall())

        with open(crm_path, "wb") as f:
            f.write(container.download_blob("crm_customers.csv").readall())

        # Load source datasets
        retail_df, crm_df = load_data(retail_path, crm_path)

        # Clean retail data
        retail_df = clean_data(retail_df)

        # Merge Retail and CRM data
        merged_df = merge_data(retail_df, crm_df)

        # Save refreshed data to DuckDB
        save_to_duckdb(merged_df, "/tmp/customer_analytics.duckdb")

        logging.info("Azure Function: Pipeline refresh completed successfully.")

        return func.HttpResponse(
            "Pipeline refresh completed successfully.",
            status_code=200
        )

    except Exception as e:
        logging.exception("Pipeline refresh failed.")

        return func.HttpResponse(
            f"Pipeline refresh failed: {str(e)}",
            status_code=500
        )