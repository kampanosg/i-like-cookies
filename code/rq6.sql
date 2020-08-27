select cta_accept as cta, count(cta_accept) as total
from cookie_options
where has_accept_btn = 1
group by cta
order by total desc;

select cta_decline as cta, count(cta_decline) as total
from cookie_options
where has_decline_btn = 1
group by cta
order by total desc;

select cta_options as cta, count(cta_options) as total
from cookie_options
where has_options_btn = 1
group by cta
order by total desc;

select cta_info as cta, count(cta_info) as total
from cookie_options
where has_info_btn = 1
group by cta
order by total desc;