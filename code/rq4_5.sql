select count(*) as 'no options' from cookie_options 
where has_accept_btn = 0 AND
	  has_decline_btn = 0 AND
	  has_info_btn = 0 AND
	  has_options_btn = 0;

select count(*) as 'only info' from cookie_options 
where has_accept_btn = 0 AND
	  has_decline_btn = 0 AND
	  has_info_btn = 1 AND
	  has_options_btn = 0;

select count(*) as 'only accept' from cookie_options 
where has_accept_btn = 1 AND
	  has_decline_btn = 0 AND
	  has_info_btn = 0 AND
	  has_options_btn = 0;

select count(*) as 'only reject' from cookie_options 
where has_accept_btn = 0 AND
	  has_decline_btn = 1 AND
	  has_info_btn = 0 AND
	  has_options_btn = 0;