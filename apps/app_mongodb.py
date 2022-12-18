from pyspark.sql import SparkSession
from pyspark import SparkContext

sc= SparkContext("local", "discentes_mongodb")

spark = SparkSession(sc)

discentes = spark.read.format("mongodb").option("database","ufrn").option("collection", "discentes").load()

#discentes = spark.read.format("mongodb").option("uri", "mongodb://127.0.0.1/ufrn.discentes").load()
#discentes = spark.read.format("mongodb").load()
print('Dataset lido do mongodb:\n')
#discentes.describe().show()

ingresso_sisu = discentes.filter(discentes['forma_ingresso'] == 'SiSU').count()
total = discentes.count()
print(f'{round((ingresso_sisu/total)*100)}%')
#teste.show(teste.count())
