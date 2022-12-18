from pyspark.sql import SparkSession
from pyspark import SparkContext

sc= SparkContext("local", "discentes_mongodb")

spark = SparkSession(sc)

df = spark.read.options(header='True', inferSchema='True', delimiter=';').csv("discentes-2022.csv")

df.write.format("mongodb").mode("append").option("database",
"ufrn").option("collection", "discentes").save()