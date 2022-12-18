from pyspark.sql import SparkSession
from pyspark import SparkContext

sc= SparkContext("local", "discentes_mongodb")

spark = SparkSession(sc)

df = spark.read.csv("discentes-2022.csv")

#df.write.format("mongodb").mode("append").save()

df.write.format("mongodb").mode("append").option("database",
"ufrn").option("collection", "discentes").save()

discentes = spark.read.format("mongodb").option("uri", "mongodb://127.0.0.1/ufrn.discentes").load()

