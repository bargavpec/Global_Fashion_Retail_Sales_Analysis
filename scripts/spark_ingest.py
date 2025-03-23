import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


parser = argparse.ArgumentParser()

parser.add_argument('--input_transactions', required=True)
parser.add_argument('--input_products', required=True)
parser.add_argument('--input_stores', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--output_store', required=True)

args = parser.parse_args()

input_transactions = args.input_transactions
input_products = args.input_products
input_stores = args.input_stores
output = args.output
output_store = args.output_store


spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', 'dataproc-staging-us-central1-963999301031-laa3vslq')

df_transactions = spark.read.parquet(input_transactions)
df_products = spark.read.parquet(input_products)
df_stores=spark.read.parquet(input_stores)

# Print schema for debugging
df_transactions.printSchema()
df_products.printSchema()
df_stores.printSchema()

df_transactions.createOrReplaceTempView('transactions')
df_products.createOrReplaceTempView('products')
df_stores.createOrReplaceTempView('stores')

df_result = spark.sql("""
SELECT pr.`Sub Category` AS Product_category,
                      trunc(tr.date, 'month') AS Invoice_month,
       SUM(tr.quantity) AS Total_sales_quantity
FROM transactions AS tr
JOIN products AS pr
ON tr.`Product ID` = pr.`Product ID`
where tr.`Transaction Type`='Sale'
GROUP BY 1,2
""")

df_result.write.format('bigquery') \
    .option('table', output) \
    .mode('overwrite') \
    .save()

df_store_result=spark.sql("""
SELECT st.Country,sum(case when `Transaction Type`='Sale' then tr.Quantity else 0 end) as Sales_Qty,
sum(case when `Transaction Type`='Return' then tr.Quantity else 0 end) as Returns_Qty,
sum(case when `Payment Method`='Cash' then tr.Quantity else 0 end) as Products_purchased_in_cash,
sum(case when `Payment Method`='Credit Card' then tr.Quantity else 0 end) as Products_purchased_in_CreditCards
 from transactions AS tr
JOIN stores AS st
on tr.`Store ID`=st.`Store ID`
group by 1
""")

df_store_result.write.format('bigquery') \
    .option('table', output_store) \
    .mode('overwrite') \
    .save()
