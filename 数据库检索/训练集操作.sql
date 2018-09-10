select * from TRAININGDATA t order by t.create_date,to_number(t.pointid);
--select count(*) from TRAININGDATA t;
--select t.create_date,count(*) from TRAININGDATA t group by t.create_date order by t.create_date;
--select * from TRAININGDATA t where t.pm10>0.5;
--select * from TRAININGDATA t where t.pm10>0.5;
--select * from TRAININGDATA t where t.pm25<0;
--select max(t.temperature),min(t.temperature) from TRAININGDATA t;
--delete from trainingdata;
select max(t.wind_direction),min(t.wind_direction) from TRAININGDATA t;

