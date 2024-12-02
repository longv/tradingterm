import logging
import signal
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # Log to a file
        # logging.FileHandler("spark_job.log"),  # Log to a file
        # Log to console
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("DataIngestor") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
        .getOrCreate()

    # Kafka Parameters
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "trade-event-topic"

    # Read from Kafka
    kafka_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .load()

    # Kafka messages are read as bytes, convert to string
    # messages = kafka_stream.selectExpr(
    #     "CAST(value AS STRING)")
    processed_df = kafka_stream.select(
        F.col("key").cast("string").alias("key"),
        F.col("value").cast("string").alias("value"),
        F.col("topic"),
        F.col("partition"),
        F.col("offset"),
        F.col("timestamp")
    )

    # Process the messages (example: printing to console)
    query = processed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    def stopQuery(signum, frame):
        query.stop()
        spark.stop()

    signal.signal(signal.SIGINT, stopQuery)
    signal.signal(signal.SIGTERM, stopQuery)

    # Wait for the query to terminate
    query.awaitTermination()


if __name__ == "__main__":
    main()
