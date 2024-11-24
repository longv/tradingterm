import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
# from org.apache.hadoop.hbase import HBaseConfiguration
# from org.apache.hadoop.hbase.client import Put, ConnectionFactory
# from org.apache.hadoop.hbase.util import Bytes


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("spark_job.log"),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)


def write_to_bigtable(row, table):
    """
    Function to write a single row to Bigtable.
    :param row: A Spark Row object
    :param table: HBase Table object
    """
    # row_key = row["id"]  # Use a unique field as the row key
    # put = Put(Bytes.toBytes(row_key))
    #
    # # Add each column from the row into Bigtable
    # for column, value in row.asDict().items():
    #     if column != "id":  # Skip the row key column
    #         put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes(
    #             column), Bytes.toBytes(str(value)))
    #
    # table.put(put)


def main():

    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("ReadGCS") \
        .getOrCreate()
    # .config("spark.jars", "./libs/bigtable-hbase-2.x-hadoop-2.14.7.jar") \
    # hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    # for conf_key in hadoop_conf.iterator():
    #     print(conf_key.getKey(), conf_key.getValue())

    # # Configure Bigtable
    # conf = HBaseConfiguration.create()
    # conf.set("google.bigtable.project.id", "trading-term")
    # conf.set("google.bigtable.instance.id", "dev-bigtable-instance")
    # # conf.set("google.bigtable.auth.service.account.json.keyfile",
    # #          "/path/to/keyfile.json")
    #
    # # Create an HBase connection
    # connection = ConnectionFactory.createConnection(conf)
    # table = connection.getTable(Bytes.toBytes("trading-data-table"))
    # Path to your GCS file
    gcs_path = "gs://cs-e4780/debs2022-gc-trading-day-08-11-21.csv"

    # Load CSV data
    # csv_file = "./data/debs2022-gc-trading-day-08-11-21.csv"
    df = spark.read.option("header", "true") \
        .option("comment", "#") \
        .csv(gcs_path)

    df.show(5)
    # Write each row to Bigtable
    # df.foreach(lambda row: write_to_bigtable(row, table))

    # Close the connection
    # table.close()
    # connection.close()

    # Stop SparkSession
    spark.stop()


if __name__ == "__main__":
    main()
