CREATE TABLE Recalls(
	recall_id INT PRIMARY KEY NOT NULL,
	recall_date DATE NOT NULL,
	reason VARCHAR(100) NOT NULL,
	company_release_link TEXT NOT NULL,
	photos_link TEXT NOT NULL
);

CREATE TABLE Companies(
	company_id BIGINT PRIMARY KEY,
	company_name VARCHAR(100) NOT NULL	
);

CREATE TABLE Brands(
	brand_id BIGINT PRIMARY KEY,
	brand_name VARCHAR(100) NOT NULL,
	company_id BIGINT REFERENCES Companies(company_id)
);

CREATE TABLE Products(
	product_id BIGINT PRIMARY KEY,
	recall_id INT REFERENCES Recalls(recall_id),
	brand_id BIGINT REFERENCES Brands(brand_id),
	asin CHAR(10),
	upc VARCHAR(12),
	product_description TEXT
);

CREATE TABLE Reviewers(
	reviewer_id BIGINT PRIMARY KEY,
	reviewer_name VARCHAR(30)
);

CREATE TABLE Reviews(
	review_id BIGINT PRIMARY KEY,
	reviewer_id BIGINT REFERENCES Reviewers(reviewer_id),
	product_id BIGINT REFERENCES Products(product_id),
	review_text TEXT,
	summary VARCHAR(300),
	overall SMALLINT,
	unix_review_time BIGINT,
	review_time TIME
);

