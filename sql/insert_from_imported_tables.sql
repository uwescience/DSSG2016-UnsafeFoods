-- add reviewers from imported table
insert into reviewer (amazon_reviewer_id, reviewer_name)
select distinct reviewerid, reviewername from review_temp;

-- add products from imported table
insert into product (asin, product_description, product_name)
select distinct asin,description, title from meta_temp;

-- add reviews from imported table
insert into review (reviewer_id, product_id, review_text, summary, overall, unix_review_time, review_time)
select 
r.reviewer_id,
p.product_id,
rt.reviewtext,
rt.summary,
rt.overall,
rt.unixreviewtime,
to_date(rt.reviewtime,'MM DD, YYYY')
from review_temp rt
join reviewer r on rt.reviewerid = r.amazon_reviewer_id
join product p on p.asin = rt.asin

--add brands from imported (review) table
insert into brand (brand_name)
select distinct brand from meta_temp
where brand is not null;

-- this makes for easier joins
alter table product
add column brand_name text;

-- add brand names
UPDATE product p
SET brand_name = mt.brand
FROM meta_temp mt
WHERE p.asin = mt.asin;

-- check success of insert
select p.brand_name, mt.brand
from product p join meta_temp mt on p.asin = mt.asin
order by random() limit 30;

-- add brand id, join on name
update product p
set brand_id = b.brand_id
from brand b
where p.brand_name = b.brand_name;

-- check for insert query success
select p.brand_name, p.brand_id, b.brand_name, b.brand_id
from product p join brand b on p.brand_id = b.brand_id
order by random() limit 30;

-- drop the brand name column - no longer needed
alter table product
drop column brand_name;

-- add table for enforcement import
create table enforce_temp (
product_type text,
event_id int,
status text,
recalling_firm text,
address1 text,
address2 text,
city text,
state_province text,
postal_code int,
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
enforce_temp_id serial primary key
);

-- add table for recalled product import tabe (enforcements)
create table recalledproduct_temp
(
recall_id text,
asin text,
upc bigint,
rp_temp_id serial primary key
);

-- insert event enforcements
insert into event (fda_event_id, description, termination_date, classification_date,
			classification, reason, initiation_date)
select distinct on (1) event_id, product_description,
to_date(termination_date, 'MM/DD/YYYY'),
to_date(center_classification_date, 'MM/DD/YYYY'),
CASE WHEN classification LIKE '%III' THEN 3
            WHEN classification LIKE '%II' THEN 2
            ELSE 1
       END,
reason_for_recall,
to_date(recall_initiation_date, 'MM/DD/YYYY')
from enforce_temp;

/*count(*) should always be 1*/
select fda_event_id, count(*) from event
group by fda_event_id;

insert into voluntarymandated (voluntary_mandated_name)
select distinct voluntary_mandated
from enforce_temp;

insert into recall (fda_recall_id, event_id)
select et.recall_number, e.event_id
from enforce_temp et join event e
on et.event_id = e.fda_event_id;

update product
set upc = rpt.upc
from recalledproduct_temp rpt
where rpt.asin = product.asin;


insert into recalledproduct  (recall_id, product_id)
select r.recall_id, p.product_id
from recall r join recalledproduct_temp rpt on r.fda_recall_id = rpt.recall_id
join product p on rpt.asin = p.asin;

select count(*) from review r
where product_id in (
select product_id from recalledproduct);

insert into categoryassignment (product_id, category_id)
select p.product_id,c.category_id
from product p join meta_temp mt on p.asin = mt.asin
join category c on mt.categories LIKE '%' || c.category_name || '%';

select category_name from category limit 100;

select c.category_name, count(*)
from category c join categoryassignment ca on c.category_id = ca.category_id
group by c.category_id
order by count(*) desc;

-- create table to import fda recall press release data product dictionary
create table press_recall_dict_temp(
upc varchar(14),
asin text,
recall_id int,
press_recall_temp_id serial primary key
);

-- import data (in psql or in pgadmin)

-- create table to import fda recall press release data
create table press_recall_temp (
recall_temp_id int primary key, -- this is not a serial because the key is set in the dictionary of recalled products above
recall_date text,
brand_name text,
product_description text,
reason_for_recall text,
company text,
company_release_link text,
photos_links text,
upc_processed_string text,
asin_string text,
upcs_string text
);

-- import data (in psql or pgadmin client)

-- Add unknown reason for reason_for_recall column
-- where it is null to handle non-nul constraint in the event table 
update press_recall_temp
set reason_for_recall = 'reason unavailable'
where reason_for_recall is null;

-- add id in event to track recall press releases
alter table event
add column press_recall_id int;

-- insert recall events
insert into event (initiation_date, reason, description, press_recall_id)
select to_date(recall_date, 'Dy DD Mon YYYY HH24:MI:SS'), reason_for_recall, product_description,
recall_temp_id
from press_recall_temp;

-- insert recalls
insert into recall (event_id, company_release_link,
	photos_link)
select e.event_id, rt.company_release_link,
rt.photos_links
from event e join press_recall_temp rt
on e.press_recall_id = rt.recall_temp_id;

-- update upcs from press release recall product dictionary
update product
set upc = pd.upc
from press_recall_dict_temp pd
where product.asin = pd.asin;


-- insert recalled products from press release 
-- recall product dictionary
insert into recalledproduct (product_id, recall_id)
select p.product_id, r.recall_id
from product p
join press_recall_dict_temp prt
on p.upc = prt.upc
join event e on e.press_recall_id = prt.recall_id
join recall r 
on r.event_id = e.event_id;

-- check number of reviews linked to a recall now
select count(*) from review
where product_id in 
(select product_id from recalledproduct);