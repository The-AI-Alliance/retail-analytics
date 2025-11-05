import asyncio
import logging
import os
import time

from fastmcp import FastMCP
import boto3
import awswrangler as wr
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Retail Analytics Server for MCP")


@mcp.tool()
def get_schema(product: str) -> str:
    """This tools will return the schema (DDL) for the given product.

    Args:
        product: The product name.
        Currently supported: retail_analytics

    Returns:
        String format of the DDL for the given product.
    """
    # Below is not support on FastMCP Cloud
    """
    try:
        with open(f"{product}.ddl") as f:
            return f.read()
    except Exception as e:
        return f"No schema available for {product}"
    """
    try:
        s3 = boto3.client("s3", region_name=os.environ["AWS_REGION"])
        response = s3.get_object(
            Bucket=os.environ["ANALYTICS_BUCKET"], Key="schemas/retail_schema.ddl"
        )
        return response["Body"].read().decode("utf-8")
    except Exception as e:
        return f"Error getting schema for {product}. Error: {e}"


@mcp.tool()
def get_product_requirements(product: str) -> str:
    """This tools will return the given product requirements in text format.

    Args:
        product: The product name.
        Currently supported: retail_analytics

    Returns:
        String format of the requirements for the given product.
    """
    try:
        with open(f"{product}.txt") as f:
            return f.read()
    except Exception as e:
        return f"No requirements available for {product}"


@mcp.tool()
def execute_sql_query(sql_query: str):
    try:
        logger.info(f"Executing sql: {sql_query}")
        boto3.setup_default_session(region_name=os.environ["AWS_REGION"])

        logger.info(f"Connecting to Athena")
        results_df = wr.athena.read_sql_query(
            sql=sql_query, database=os.environ["RETAIL_DATABASE_NAME"]
        )
        logger.info(f"Query Executed")
        return results_df.to_csv(index=False)
    except Exception as e:
        msg = f"Unable to execute query: {e}"
        logger.info(msg)
        return msg


if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            # transport="http",
            transport="streamable-http",
            # host="127.0.0.1",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )
