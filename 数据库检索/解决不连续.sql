/*
delete from prodata_part1 where rowid not in (select min(rowid) from prodata t group by t.create_date,t.pointid,t.one_hour_before,t.factor_value,
t.pm10one_hour_before,t.pm10factor_value,t.coone_hour_before,t.cofactor_value,t.no2one_hour_before,t.no2factor_value,
t.o3one_hour_before,t.o3factor_value,t.so2one_hour_before,t.so2factor_value having count(*)>=1);;
*/
/*
select t.create_date,t.pointid,count(*) from prodata
 t group by t.create_date,t.pointid,t.one_hour_before,t.factor_value,
t.pm10one_hour_before,t.pm10factor_value,t.coone_hour_before,t.cofactor_value,t.no2one_hour_before,t.no2factor_value,
t.o3one_hour_before,t.o3factor_value,t.so2one_hour_before,t.so2factor_value having count(*)=1;
*/

--select distinct * from prodata t where t.create_date=to_date('2017/6/9 14','YYYY-MM-DD HH24');



--select t.create_date,count(*) from prodata t group by t.create_date;
--delete from prodata t where t.create_date=to_date('2016/8/3 9','YYYY-MM-DD HH24');


delete from PRODATA1_VAL where rowid not in (select min(rowid) from PRODATA1_VAL t group by t.create_date,t.pointid having count(*)>=1);

--delete from prodata t;


--(select t.create_date,t.pointid,count(*) from prodata t-- where t.create_date>=to_date('2016/5/1 0','YYYY-MM-DD HH24') and t.create_date < to_date('2016/6/1 0','YYYY-MM-DD HH24')
--group by t.create_date,t.pointid having count(*)>=1);

--select * from prodata t order by t.create_date,to_number(t.pointid);
