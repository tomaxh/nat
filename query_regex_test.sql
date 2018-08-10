\c nat;
select super_match_str, match_str, found 
	from (
		select (regexp_matches(found, '(?:Canada |)pipe'))[1] as super_match_str, (regexp_matches(found, 'Canada'))[1] as match_str, found 
		from (
			select description as found 
			from names_and_terms 
			where description ~ 'pipe|Canada'
		) as t
	)  as t2
	order by super_match_str is not null desc, length(super_match_str) desc, match_str is not null desc;