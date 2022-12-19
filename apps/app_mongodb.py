from pyspark.sql import SparkSession
from pyspark import SparkContext

sc= SparkContext("local", "discentes_mongodb")

spark = SparkSession(sc)

spark.sparkContext.setLogLevel('WARN')

discentes = spark.read.format("mongodb").option("database","ufrn").option("collection", "discentes").load()
print('### DATASET LIDO DO MONGODB ###')

#Quantidade de ingressantes
total = discentes.count()

# #Ingressantes por forma de ingresso
forma_ingresso = discentes.groupBy(['forma_ingresso']).count()
forma_ingresso = forma_ingresso.withColumn("Porcentagem (%)", (forma_ingresso["count"]/total)*100)
forma_ingresso = forma_ingresso.rdd.map(lambda x: (x[0], x[1], round(x[2],2) if x[2] else 0.00)).toDF(['forma_ingresso','count','Porcentagem (%)'])
forma_ingresso = forma_ingresso.orderBy('Porcentagem (%)',ascending=False)

#Ingressantes 
total_mulheres = discentes.filter(discentes['sexo'] == 'F').count()
total_homens = discentes.filter(discentes['sexo'] == 'M').count()

data = [(total_mulheres,total_homens,round(total_mulheres/total,2)*100,round(total_homens/total,2)*100)]

columns = ["Mulheres","Homens","Mulheres(%)","Homens (%)"]
ingressantes = spark.createDataFrame(data=data, schema = columns)

# #Quantidade de pessoas por sexo por curso
discentes_por_curso = discentes.groupBy(['nome_curso']).count().orderBy('nome_curso')
discentes_por_curso = discentes_por_curso.withColumnRenamed("count","count_total")
sexo_por_curso = discentes.groupBy(['nome_curso','sexo']).count().orderBy('nome_curso')
sexo_por_curso = sexo_por_curso.withColumnRenamed("count","count_sexo")

perc_sexo_por_curso = sexo_por_curso.join(discentes_por_curso,on='nome_curso',how='left')
perc_sexo_por_curso = perc_sexo_por_curso.withColumn("Porcentagem (%)", (perc_sexo_por_curso["count_sexo"]/perc_sexo_por_curso['count_total'])*100)
perc_sexo_por_curso = perc_sexo_por_curso.rdd.map(lambda x: (x[0], x[1], x[2], x[3], round(x[4],2) if x[4] else 0.00)).toDF(['nome_curso','sexo', 'count_sexo','count_total','Porcentagem (%)'])

# nível de ensino
nivel_ensino = discentes.groupBy(['nivel_ensino']).count()
nivel_ensino = nivel_ensino.withColumn("Porcentagem (%)", (nivel_ensino["count"]/total)*100)
nivel_ensino = nivel_ensino.rdd.map(lambda x: (x[0], x[1], round(x[2],1) if x[2] else 0.00)).toDF(['nivel_ensino','count','Porcentagem (%)'])
nivel_ensino = nivel_ensino.orderBy('Porcentagem (%)',ascending=False)

# Salvando resultados
forma_ingresso.write.mode("overwrite").options(header='True', delimiter=';').csv("resultados/forma_ingresso")
ingressantes.write.mode("overwrite").options(header='True', delimiter=';').csv("resultados/ingressantes")
perc_sexo_por_curso.write.mode("overwrite").options(header='True', delimiter=';').csv("resultados/perc_sexo_curso")
nivel_ensino.write.mode("overwrite").options(header='True', delimiter=';').csv("resultados/nivel_ensino")

print('### RESULTADOS SALVOS COM SUCESSO ###')