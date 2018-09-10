select * from VALDATA t order by t.create_date,to_number(t.pointid);
select t.create_date,count(*) from VALDATA t group by t.create_date order by t.create_date;
--select t.create_date,t.pointid,count(*) from VALDATA t group by t.create_date,t.pointid order by t.create_date,t.pointid;

select max(t.pm25),min(t.pm25),max(t.pm10),min(t.pm10),max(t.no2),min(t.no2),
max(t.so2),min(t.so2),max(t.o3),min(t.o3),max(t.co),min(t.co) from VALDATA t ;
select max(t.date_processed),min(t.date_processed),max(t.temperature),min(t.temperature),max(t.pressure),min(t.pressure),
max(t.humidity),min(t.humidity) from VALDATA t ;
--select * from VALDATA t where t.temperature=0 ;
--select * from VALDATA t where t.create_date=to_date('2017-2-11 7','YYYY-MM-DD HH24') ;


--select * from VALDATA t where t.pm10>0.25 ;
select * from VALDATA t where t.co<0 ;
--select * from VALDATA t where t.o3<0 ;
--update VALDATA t set  t.co= 0-t.co  where t.co<0 --and t.o3>-0.05-- and t.pm25>0.3;--t.create_date=to_date('2017-2-11 7','YYYY-MM-DD HH24');
--select avg(t.pm25),avg(pm10),avg(no2),avg(so2),avg(co),avg(o3) from VALDATA t ;

--update VALDATA t set t.pm25=t.pm25-0.75  where  t.pm25>0.25;
--delete from VALDATA;
