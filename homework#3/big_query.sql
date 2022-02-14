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