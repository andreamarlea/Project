#!/bin/sh
# rename and load data to HDFS
# written by Sue Yang April -2016

# rename and copy data files to "exercise1" folder
echo "renaming data and removing headers..."
echo "generating business.csv"
tail -n +2  /data/Yelp/CSV/"yelp_academic_dataset_business.csv" > /data/Yelp/CSV/business.csv
echo "generating review.csv"
tail -n +2  /data/Yelp/CSV/"yelp_academic_dataset_review.csv" > /data/Yelp/CSV/review.csv

# create folder in HDFS
echo "creating folders in HDFS..."
hdfs dfs -mkdir /user/w205/Yelp
hdfs dfs -mkdir /user/w205/Yelp/business
hdfs dfs -mkdir /user/w205/Yelp/review

# copy files into HDFS
echo "copying data to HDFS..."
hdfs dfs -put /data/Yelp/CSV/business.csv /user/w205/Yelp/business
hdfs dfs -put /data/Yelp/CSV/review.csv /user/w205/Yelp/review

echo "load_data_lake done"
exit 0