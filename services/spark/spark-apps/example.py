from pyspark.sql import SparkSession
import random

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("SimplePiCalculation") \
    .getOrCreate()

# Function to calculate Pi using Monte Carlo method


def monte_carlo_pi(num_samples):
    count = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            count += 1
    return 4.0 * count / num_samples


# Parallelize the task across Spark workers
num_samples = 1000000
rdd = spark.sparkContext.parallelize([num_samples] * 100)

# Perform the calculation using the RDD
pi_estimate = rdd.map(monte_carlo_pi).reduce(lambda x, y: x + y) / 100

print(f"Estimated Pi value: {pi_estimate}")

# Stop the Spark session
spark.stop()
