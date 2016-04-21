#!/bin/sh
# convert yelp json data to csv
# yelp json data is downloaded from http://www.yelp.com/dataset_challenge to /data/Yelp/json
# installed python version should be above 2.6
# written by Sue Yang March -2016

# download and extract files
# install packages
echo "installing simplejson"
pip install simplejson
echo "installing argparse"
pip install argparse
echo "installing mrjob"
pip install mrjob

# create directory for CSV data
mkdir /data/Yelp/CSV

# convert json files in "json" to CSV 
for file in /data/Yelp/json/*.json; do
	echo "Converting $file file..."
	python /data/Yelp/ServingScripts/ConvertData/json_to_csv_converter.py $file

done
mv /data/Yelp/json/*.csv /data/Yelp/CSV/
echo "Converting done"
exit 0