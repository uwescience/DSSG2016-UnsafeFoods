insert into reviewer (amazon_reviewer_id, reviewer_name)
select distinct reviewerid, reviewername from review_temp;

insert into product (asin, product_description, product_name)
select distinct asin,description, title from meta_temp;

select reviewtime from review_temp limit 5;

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
join product p on p.asin = rt.asin;

select * from review
order by random()
limit 25;

insert into brand (brand_name)
select distinct brand from meta_temp
where brand is not null;

alter table product
add column brand_name text;

UPDATE product p
SET brand_name = mt.brand
FROM meta_temp mt
WHERE p.asin = mt.asin;

select p.brand_name, mt.brand
from product p join meta_temp mt on p.asin = mt.asin
order by random() limit 30;

update product p
set brand_id = b.brand_id
from brand b
where p.brand_name = b.brand_name;

select p.brand_name, p.brand_id, b.brand_name, b.brand_id
from product p join brand b on p.brand_id = b.brand_id
order by random() limit 30;

alter table product
drop column brand_name;



