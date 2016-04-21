1. download and convert yelp data from http://www.yelp.com/dataset_challenge. Download to /data/Yelp/json
2. convert yelp data from json to csv
sh /data/Yelp/ServingScripts/ConvertData/Serconvert_yelp_json_to_csv.sh
3. copy "yelp_academic_dataset_business.csv" back to PC using FileZilla. Use OpenRefine to clear data and keep only restaurant business. And remove attributes only belong to other business
such as hair, insurance 
Transfer cleaned data back to EBS.
4. Start HDFS Hadoop(environment has been setup by downloading and running wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh)
/root/start©\hadoop.sh
5. Start Postgres:
/data/start_postgres.sh
4. load data into data lake.
sh /data/Yelp/loading_and_modelling/load_data_lake.sh

