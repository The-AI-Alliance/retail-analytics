from aws_cdk import aws_s3 as s3, aws_glue as glue, aws_athena as athena, Stack

from constructs import Construct


class AnalyticsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        tag: str,
        env: str,
        datalake_bucket_name: str,
        demo_dataset_name: str,
        application_ci: str,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        if len(tag) > 0:
            tag = tag[:-1]

        # Reference existing S3 bucket for Athena data
        datalake_bucket = s3.Bucket.from_bucket_name(
            self, id=f"{application_ci}DatalakeBucket", bucket_name=datalake_bucket_name
        )

        db_name = "retail_decision_support_demo"
        athena_catalog_name = "AwsDataCatalog"
        # Create a Glue database for Athena
        glue_db = glue.CfnDatabase(
            self, db_name, catalog_id=self.account, database_input={"name": db_name}
        )

        # Athena table definition for ProductCategories table
        product_categories_table = glue.CfnTable(
            self,
            "ProductCategoriesTable",
            catalog_id=self.account,
            database_name=db_name,
            table_input={
                "name": "productcategories",
                "tableType": "EXTERNAL_TABLE",
                "parameters": {"classification": "json", "has_encrypted_data": "false"},
                "storageDescriptor": {
                    "columns": [
                        {"name": "productcategoryid", "type": "string"},
                        {"name": "createdby", "type": "string"},
                        {"name": "createdat", "type": "string"},
                    ],
                    "location": f"{datalake_bucket.s3_url_for_object()}/{demo_dataset_name}/productcategories/",
                    "inputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "outputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "serdeInfo": {
                        "serializationLibrary": "org.apache.hadoop.hive.serde2.OpenCSVSerde",
                        "parameters": {"skip.header.line.count": "1"},
                    },
                },
            },
        )
        product_categories_table.add_dependency(glue_db)
