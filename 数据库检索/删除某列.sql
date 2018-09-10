--select * from PRODATA t where t.one_hour_before is NULL order by t.create_date,t.pointid ;
/*alter table PRODATA1_VAL drop (
factor_code,
pm10factor_code,
cofactor_code,
no2factor_code,
so2factor_code,
o3factor_code,
pm10pointid,
no2pointid,
so2pointid,
copointid,
o3pointid,
pm10create_date,
no2create_date,
so2create_date,
cocreate_date,
o3create_date,
one_hour_before,
pm10one_hour_before,
no2one_hour_before,
so2one_hour_before,
coone_hour_before,
o3one_hour_before
);*/
select * from PRODATA1_VAL t;
--alter table PRODATA1_VAL rename column o3factor_value to o3;


