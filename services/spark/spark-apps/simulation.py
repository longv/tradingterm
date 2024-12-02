import logging
import signal
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType, StructField

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
        .appName("TradingSimulation") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
        .getOrCreate()

    # Kafka Parameters
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "trade-event-topic"

    # Example: Create a DataFrame with messages to send
    schema = StructType([
        StructField("key", StringType(), True),
        StructField("value", StringType(), True)
    ])

    # Sample data to send to Kafka
    data = [
        ("key1", "Hello Kafka!"),
        ("key2", "This is a test message."),
        ("key3", "PySpark producing to Kafka.")
    ]

    df = spark.createDataFrame(data, schema)

    # Write to Kafka
    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
      .write \
      .format("kafka") \
      .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
      .option("topic", kafka_topic) \
      .save()

    print("Messages produced to Kafka successfully!")

    # Stop the SparkSession
    spark.stop()


if __name__ == "__main__":
    main()
