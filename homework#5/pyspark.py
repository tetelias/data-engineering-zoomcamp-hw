import pandas as pd
import pyspark
from pyspark.sql import functions as F, SparkSession, types

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

# HWQ#1: spark.version --> "res0: String = 3.0.3"

schema = types.StructType([
    types.StructField('hvfhs_license_num', types.StringType(), True),
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True),
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True),
    types.StructField('DOLocationID', types.IntegerType(), True),
    types.StructField('SR_Flag', types.StringType(), True)
])

df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv('fhvhv_tripdata_2021-02.csv')

df = df.repartition(24)
df.write.parquet('partitions/2021/02')

# HWQ#2: "ls -lh partitions/2021/02/" --> "total 208M"

df1 = spark.read.parquet('partitions/2021/02/')

# Try #1
df1 \
    .where((df1.pickup_datetime >= '2021-02-15') & (df1.pickup_datetime < '2021-02-16')) \
    .count()

# Try #2
df1 \
    .withColumn('pickup_date', F.to_date(df1.pickup_datetime)) \
    .where(F.col('pickup_date') == '2021-02-15') \
    .count()

# HWQ#3: 367170

df1 \
    .withColumn('DiffInSeconds', F.col("dropoff_datetime").cast("long") - F.col('pickup_datetime').cast("long")) \
    .sort(F.col('DiffInSeconds').desc()) \
    .show(1)

# HWQ#4: "2021-02-11"

df1 \
    .groupby('dispatching_base_num') \
    .count() \
    .sort(F.col("count").desc()) \
    .show(1)

# HWQ#5: 2 stages

def combine(x, y):
    return f'{x}/{y}'

combine_cols = F.udf(combine, types.StringType())

df1 \
    .select('PULocationID', 'DOLocationID') \
    .withColumn('Result', combine_cols('PULocationID', 'DOLocationID')) \
    .groupby('Result') \
    .count() \
    .sort(F.col("count").desc()) \
    .show(1)

# HWQ#6: 76/76 - East New York / East New York

