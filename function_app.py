import logging
import azure.functions as func

from src.pipeline import load_data, clean_data, merge_data, save_to_duckdb


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="refresh-pipeline", methods=["POST"])
def refresh_pipeline(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to trigger the ETL pipeline refresh.
    """

    logging.info("Azure Function: Starting pipeline refresh.")

    try:
        # Load source datasets
        retail_df, crm_df = load_data()

        # Clean retail data
        retail_df = clean_data(retail_df)

        # Merge Retail and CRM data
        merged_df = merge_data(retail_df, crm_df)

        # Save refreshed data to DuckDB
        save_to_duckdb(merged_df)

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