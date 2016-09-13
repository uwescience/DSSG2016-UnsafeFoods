--This file is the SQL create script needed to create an empty table
-- to contain the amazon review and fda recall/enforcement data.

-- this table contains enforcement data.
-- import the enforcement data csv with the end 'formatted_for_import'
-- from the github_data folder.
CREATE TABLE public.enforce_temp
(
  product_type text,
  event_id integer,
  status text,
  recalling_firm text,
  address1 text,
  address2 text,
  city text,
  state_province text,
  postal_code integer,
  country text,
  voluntary_mandated text,
  initial_public_notification text,
  distribution_pattern text,
  recall_number text,
  classification text,
  product_description text,
  product_quantity text,
  reason_for_recall text,
  recall_initiation_date text,
  center_classification_date text,
  termination_date text,
  report_date text,
  code_info text,
  upc_asin_dict text,
  enforce_temp_id integer NOT NULL DEFAULT nextval('enforce_temp_enforce_temp_id_seq'::regclass),
  CONSTRAINT enforce_temp_pkey PRIMARY KEY (enforce_temp_id)
);

-- This table contains the preprocessed category assignments.
-- However, the insert sql script named 'insert_from_imported_tables'
-- located in this sql folder
-- has an insert query that inserts assignments by substring. That is more efficient,
-- but this table is included for archive purposes.
CREATE TABLE public.cat_assn_temp
(
  productcategory text,
  parentcategory text,
  cat_id integer NOT NULL DEFAULT nextval('cat_assn_temp_cat_id_seq'::regclass),
  parent_id integer
);

-- this table is created and then used to import the formatted
-- amazon metadata. This data can be downloaded from 
-- http://jmcauley.ucsd.edu/data/amazon/
CREATE TABLE public.meta_temp
(
  salesrank text,
  title text,
  categories text,
  asin text,
  imurl text,
  description text,
  related text,
  price text,
  brand text,
  meta_id integer NOT NULL DEFAULT nextval('meta_temp_meta_id_seq'::regclass),
  CONSTRAINT meta_temp_pkey PRIMARY KEY (meta_id)
);

-- This table contains the press release recall-to-product dictionary
--as processed by our asin-upc matching algorithms. The recall ID was generated
-- in the Pandas dataframe and is to be used in the Database to reference
-- recalls and products to fetch their db-specific unique identifiers.
CREATE TABLE public.press_recall_dict_temp
(
  upc character varying(14),
  asin text,
  recall_id integer,
  press_recall_temp_id integer NOT NULL DEFAULT nextval('press_recall_temp_press_recall_temp_id_seq'::regclass),
  CONSTRAINT press_recall_temp_pkey PRIMARY KEY (press_recall_temp_id)
);

-- This table is to import the formatted FDA press release data.
-- The version formatted for import can be found in the github_data 
-- folder named 'press_upc_asin_formatted_For_import.csv'.
CREATE TABLE public.press_recall_temp
(
  recall_temp_id integer NOT NULL,
  recall_date text,
  brand_name text,
  product_description text,
  reason_for_recall text,
  company text,
  company_release_link text,
  photos_links text,
  upc_processed_string text,
  asin_string text,
  upcs_string text,
  CONSTRAINT press_recall_temp_pkey1 PRIMARY KEY (recall_temp_id)
);

--This table is to contain the dictionary of recalled products
-- extracted from the enforcement dataset. The insert script
-- contains the query that matches these products on recall_id.
CREATE TABLE public.recalledproduct_temp
(
  recall_id text,
  asin text,
  upc bigint,
  rp_temp_id integer NOT NULL DEFAULT nextval('recalledproduct_temp_rp_temp_id_seq'::regclass),
  CONSTRAINT recalledproduct_temp_pkey PRIMARY KEY (rp_temp_id)
);

-- This table is to contain the amazon review data formatted for import.
-- It is recommended to import a dataset this large with psql in the terminal
-- rather than in the pgadminIII client. The Amazon review data can be 
-- retrieved at http://jmcauley.ucsd.edu/data/amazon/
CREATE TABLE public.review_temp
(
  reviewerid text,
  asin text,
  reviewername text,
  reviewtext text,
  overall integer,
  summary text,
  unixreviewtime integer,
  reviewtime text,
  review_temp_id integer NOT NULL DEFAULT nextval('review_temp_review_temp_id_seq'::regclass),
  CONSTRAINT review_temp_pkey PRIMARY KEY (review_temp_id)
);

-- This table contains the options for whether or not a recall was 
-- volunteered by the firm or mandated by the fda.
CREATE TABLE public.voluntarymandated
(
  voluntary_mandated_id integer NOT NULL DEFAULT nextval('voluntarymandated_voluntary_mandated_id_seq'::regclass),
  voluntary_mandated_name character varying(100) NOT NULL,
  CONSTRAINT voluntarymandated_pkey PRIMARY KEY (voluntary_mandated_id)
);

-- Insert the three options
insert into voluntarymandated (voluntary_mandated_name)
values
('Voluntary: Firm Initiated'),
('Voluntary: FDA Requested'),
('FDA Mandated');

-- Table to contain category tree from Amazon metadata.
CREATE TABLE public.category
(
  category_id integer NOT NULL DEFAULT nextval('category_category_id_seq'::regclass),
  parent_id integer,
  category_name character varying(100),
  CONSTRAINT category_pkey PRIMARY KEY (category_id)
);

-- Table to contain companies. Company data is extracted from
-- amazon and fda data.
CREATE TABLE public.company
(
  company_id integer NOT NULL DEFAULT nextval('company_company_id_seq'::regclass),
  company_name character varying(100) NOT NULL,
  CONSTRAINT company_pkey PRIMARY KEY (company_id)
);

-- table to contain brands. Brands can reference a company
-- but not always, as not all data is complete.
CREATE TABLE public.brand
(
  brand_id integer NOT NULL DEFAULT nextval('brand_brand_id_seq'::regclass),
  brand_name character varying(200) NOT NULL,
  company_id bigint,
  CONSTRAINT brand_pkey PRIMARY KEY (brand_id),
  CONSTRAINT brand_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (company_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- table to contain recall events. A single record from the enforcement data
-- has a 1:N relationship with recalls, so 1 or more record in the recall
-- table might reference an event. However, the FDA recall press release data
-- has a 1:1 relationship between events and recalls, as this data had 1 less
-- layer in its organization of recalls.
CREATE TABLE public.event
(
  event_id integer NOT NULL DEFAULT nextval('event_event_id_seq'::regclass),
  initiation_date date,
  reason text NOT NULL,
  company_id bigint,
  voluntary_mandated smallint,
  classification smallint,
  classification_date date,
  termination_date date,
  description text,
  fda_event_id integer,
  press_recall_id integer,
  CONSTRAINT event_pkey PRIMARY KEY (event_id),
  CONSTRAINT event_company_id_fkey FOREIGN KEY (company_id)
      REFERENCES public.company (company_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT event_voluntary_mandated_fkey FOREIGN KEY (voluntary_mandated)
      REFERENCES public.voluntarymandated (voluntary_mandated_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT check_classification CHECK (classification >= 1 AND classification <= 3)
);

-- This table contains instances of a recall. One or more recalls refers
-- to a single enforcement event, but only one recall can refer to a press release event.
CREATE TABLE public.recall
(
  recall_id integer NOT NULL DEFAULT nextval('recall_recall_id_seq'::regclass),
  event_id integer,
  fda_recall_id character varying(15),
  company_release_link text,
  photos_link text,
  CONSTRAINT recall_pkey PRIMARY KEY (recall_id),
  CONSTRAINT recall_event_id_fkey FOREIGN KEY (event_id)
      REFERENCES public.event (event_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- This table contains amazon reviewers from the review data.
-- A single reviewer could be linked to 1 or more reviews.
CREATE TABLE public.reviewer
(
  reviewer_id integer NOT NULL DEFAULT nextval('reviewer_reviewer_id_seq'::regclass),
  reviewer_name character varying(75),
  amazon_reviewer_id character varying(30),
  CONSTRAINT reviewer_pkey PRIMARY KEY (reviewer_id)
);

-- This table contains Amazon products. No products are added as of now 
-- that are only in the FDA data. This is not a constraint, and data from other sources
-- can be added. The current product data comes from the UC website listed above.
CREATE TABLE public.product
(
  product_id integer NOT NULL DEFAULT nextval('product_product_id_seq'::regclass),
  brand_id bigint,
  asin text,
  upc character varying(14),
  product_description text,
  product_name text,
  CONSTRAINT product_pkey PRIMARY KEY (product_id),
  CONSTRAINT product_brand_id_fkey FOREIGN KEY (brand_id)
      REFERENCES public.brand (brand_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- This table contains the amazon reviews. It comes from the UC website listed above.
CREATE TABLE public.review
(
  review_id integer NOT NULL DEFAULT nextval('review_review_id_seq'::regclass),
  reviewer_id bigint,
  product_id bigint,
  review_text text,
  summary text,
  overall smallint,
  unix_review_time bigint,
  review_time date,
  CONSTRAINT review_pkey PRIMARY KEY (review_id),
  CONSTRAINT review_product_id_fkey FOREIGN KEY (product_id)
      REFERENCES public.product (product_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT review_reviewer_id_fkey FOREIGN KEY (reviewer_id)
      REFERENCES public.reviewer (reviewer_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- This is a dictionary of amaon products linked to a recall.
-- As non-amazon review products are added, this table can be populated
-- with recalled products from other data sources.
CREATE TABLE public.recalledproduct
(
  recalledproduct_id integer NOT NULL DEFAULT nextval('recalledproduct_recalledproduct_id_seq'::regclass),
  recall_id integer,
  product_id integer,
  CONSTRAINT recalledproduct_pkey PRIMARY KEY (recalledproduct_id),
  CONSTRAINT recalledproduct_product_id_fkey FOREIGN KEY (product_id)
      REFERENCES public.product (product_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT recalledproduct_recall_id_fkey FOREIGN KEY (recall_id)
      REFERENCES public.recall (recall_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- This table contains a dictionary of product category assignments.
CREATE TABLE public.categoryassignment
(
  category_assn_id integer NOT NULL DEFAULT nextval('categoryassignment_category_assn_id_seq'::regclass),
  product_id bigint,
  category_id integer,
  CONSTRAINT categoryassignment_pkey PRIMARY KEY (category_assn_id),
  CONSTRAINT categoryassignment_category_id_fkey FOREIGN KEY (category_id)
      REFERENCES public.category (category_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT categoryassignment_product_id_fkey FOREIGN KEY (product_id)
      REFERENCES public.product (product_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)