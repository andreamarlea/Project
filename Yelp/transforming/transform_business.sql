--create simple table "business" in ER diagram
DROP TABLE business;
CREATE TABLE business AS
SELECT business_id,name,open,categories,stars,review_count,city,state,full_address,latitude,longitude FROM business_raw;