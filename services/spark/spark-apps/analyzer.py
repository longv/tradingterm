import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.sql.window import Window
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


def sanitize(df):
    renamed_columns = [col.replace(" ", "_").lower() for col in df.columns]
    df = df.toDF(*renamed_columns)

    project_columns = ["id", "sectype", "last", "trading_time", "trading_date"]

    df = df.select(
        project_columns
    ).filter(
        F.col("last").isNotNull() &
        F.col("trading_time").isNotNull() &
        F.col("trading_date").isNotNull()
    ).withColumn(
        "last",
        F.col("last").cast("float")
    ).withColumn(
        "trading_date",
        F.to_date(F.col("trading_date"), "dd-MM-yyyy")
    )

    return df


# Keep the symbol's last price within the 5-min windows
def retainWindowLastPrice(df):
    df = df.withColumn(
        "timestamp",
        F.concat_ws(
            " ",
            F.col("trading_date"),
            F.col("trading_time")
        ).cast("timestamp")
    ).drop(
        "trading_date", "trading_time"
    ).withColumn(
        "5min_window",
        (F.unix_timestamp("timestamp") / 300).cast("integer") * 300
    )

    # Add a row number column to identify the last record in each window
    window_spec = Window.partitionBy("id", "sectype", "5min_window") \
        .orderBy(F.col("timestamp").desc())

    df = df.withColumn(
        "row_num",
        F.row_number().over(window_spec)
    ).filter(
        F.col("row_num") == 1
    ).drop(
        "row_num"
    ).orderBy(
        "id", "sectype", "timestamp"
    )

    return df


def calculateEmaUdf(prices):
    j = 38
    alpha = 2 / (1 + j)

    ema = 0
    ema_values = []

    for price in prices:
        ema = price * alpha + ema * (1 - alpha)
        ema_values.append(ema)

    return ema_values


def calculateEma(df):
    ema_udf = F.udf(calculateEmaUdf, ArrayType(DoubleType()))

    df = df.groupBy("id", "sectype").agg(
        F.collect_list("last").alias("prices"),
        F.collect_list("timestamp").alias("timestamps")
    ).withColumn(
        "ema_values",
        ema_udf(F.col("prices"))
    ).withColumn(
        "zipped",
        F.arrays_zip(F.col("prices"), F.col(
            "ema_values"), F.col("timestamps"))
    ).select(
        F.col("id"),
        F.col("sectype"),
        F.explode(F.col("zipped")).alias("exploded")
    ).select(
        F.col("id"),
        F.col("sectype"),
        F.col("exploded.prices").alias("last"),
        F.col("exploded.ema_values").alias("ema"),
        F.col("exploded.timestamps").alias("timestamp")
    )

    return df


def main():

    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("ReadGCS") \
        .getOrCreate()

    # Load CSV data
    # gcs_path = "gs://cs-e4780/debs2022-gc-trading-day-08-11-21.csv"
    gcs_path = "/Users/longv/Study/aalto/scalable-systems/debs2022-gc-trading-day-08-11-21.csv"
    df = spark.read.option("header", "true") \
        .option("comment", "#") \
        .csv(gcs_path)

    # Perform EMA calculation
    df = sanitize(df)
    df = retainWindowLastPrice(df)
    df = calculateEma(df)

    df.show()

    # Stop SparkSession
    spark.stop()


if __name__ == "__main__":
    main()
