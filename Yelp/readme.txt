1. First, we downloaded and converted data from the Yelp dataset challenge. This challenge is located here:
http://www.yelp.com/dataset_challenge. Download to /data/Yelp/json
2. Next, we converted Yelp data from json to csv.
sh /data/Yelp/ServingScripts/ConvertData/Serconvert_yelp_json_to_csv.sh
3. After, we copied "yelp_academic_dataset_business.csv" back to PC using FileZilla. We used OpenRefine to select businesses that are restaurants, as yelp has other types of businesses such as barbers and insurance companies. We transfer cleaned data back to EBS.
4. Start HDFS Hadoop(environment has been setup by downloading and running wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh)
/root/start©\hadoop.sh
5. Start Postgres:
/data/start_postgres.sh
4. Load data into the data lake:
sh /data/Yelp/loading_and_modelling/load_data_lake.sh

