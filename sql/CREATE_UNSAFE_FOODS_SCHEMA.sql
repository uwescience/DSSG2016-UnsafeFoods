CREATE TABLE Recall(
	recall_id INT PRIMARY KEY,
	recall_date DATE NOT NULL,
	reason VARCHAR(100) NOT NULL,
	company_release_link TEXT NOT NULL,
	photos_link TEXT NOT NULL
);

CREATE TABLE Company(
	company_id BIGINT PRIMARY KEY,
	company_name VARCHAR(100) NOT NULL	
);

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

CREATE TABLE RecallHistory(
	recall_history_id BIGINT PRIMARY KEY,
	recall_id INT REFERENCES Recall(recall_id),
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

