--create simple table "review" in ER diagram
DROP TABLE review;
CREATE TABLE revoew AS
SELECT review_id,business_id,text,stars,date FROM review_raw;