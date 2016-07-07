CREATE TABLE Event(
	event_id INT PRIMARY KEY,
	event_date DATE NOT NULL,
	reason VARCHAR(250) NOT NULL,
	company_release_link TEXT NOT NULL,
	photos_link TEXT NOT NULL
);

CREATE TABLE Company(
	company_id BIGINT PRIMARY KEY,
	company_name VARCHAR(100) NOT NULL	
);

ALTER TABLE Event
ADD COLUMN company_id BIGINT REFERENCES Company(company_id)

CREATE TABLE Brand(
	brand_id BIGINT PRIMARY KEY,
	brand_name VARCHAR(100) NOT NULL,
	company_id BIGINT REFERENCES Company(company_id)
);

CREATE TABLE Product(
	product_id BIGINT PRIMARY KEY,
	brand_id BIGINT REFERENCES Brand(brand_id),
	asin CHAR(10),
	upc VARCHAR(12),
	product_description TEXT
);

CREATE TABLE Recall(
	recall_id BIGINT PRIMARY KEY,
	event_id INT REFERENCES Event(event_id),
	product_id BIGINT REFERENCES Product(product_id)
);

CREATE TABLE Reviewer(
	reviewer_id BIGINT PRIMARY KEY,
	reviewer_name VARCHAR(30)
);

CREATE TABLE Review(
	review_id BIGINT PRIMARY KEY,
	reviewer_id BIGINT REFERENCES Reviewer(reviewer_id),
	product_id BIGINT REFERENCES Product(product_id),
	review_text TEXT,
	summary VARCHAR(300),
	overall SMALLINT,
	unix_review_time BIGINT,
	review_time TIME
);

#Create indeces for the primary keys
CREATE SEQUENCE recall_serial START 10001;
CREATE SEQUENCE company_serial START 10001;
CREATE SEQUENCE brand_serial START 10001;
CREATE SEQUENCE product_serial START 1000001;
CREATE SEQUENCE recall_hist_serial START 1000001;
CREATE SEQUENCE reviewer_serial START 10000001;
CREATE SEQUENCE review_serial START 1000000001;


