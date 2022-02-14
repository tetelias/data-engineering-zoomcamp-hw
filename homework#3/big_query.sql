-- Create table for Q1 and Q2
CREATE OR REPLACE EXTERNAL TABLE `ultimate-life-338623.ny_taxi_trips.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc_tlc_files/trip data/fhv_tripdata_2019-*.csv']
);

-- Query for Q1
SELECT COUNT(1) FROM ultimate-life-338623.ny_taxi_trips.external_fhv_tripdata;

-- Query for Q2
SELECT COUNT(DISTINCT dispatching_base_num) FROM ultimate-life-338623.ny_taxi_trips.external_fhv_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE ultimate-life-338623.ny_taxi_trips.fhv_tripdata_partitoned
PARTITION BY
  DATE(dropoff_datetime) AS
SELECT * FROM ultimate-life-338623.ny_taxi_trips.external_fhv_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE ultimate-life-338623.ny_taxi_trips.fhv_tripdata_partitoned_clustered
PARTITION BY
  DATE(dropoff_datetime) 
  CLUSTER BY dispatching_base_num AS
SELECT * FROM ultimate-life-338623.ny_taxi_trips.external_fhv_tripdata;

-- Query for Q4s
SELECT count(*) as trips
FROM ultimate-life-338623.ny_taxi_trips.fhv_tripdata_partitoned_clustered
WHERE DATE(dropoff_datetime) BETWEEN '2019-01-01' AND '2019-03-31'
  AND dispatching_base_num IN ('B00987', 'B02060', 'B02279');