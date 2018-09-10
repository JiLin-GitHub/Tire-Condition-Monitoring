--select count(*) from AQF_FORECAST_ONE_DAY_WX_PM25 t;
-- count(*) from AQF_FORECAST_ONE_DAY_WX_CO t;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_SO2 t group by t.pointid;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_O3 t group by t.pointid;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_NO2 t group by t.pointid;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_CO t group by t.pointid;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_PM25 t group by t.pointid;
select t.pointid,count(*) from AQF_FORECAST_ONE_DAY_WX_PM10 t group by t.pointid;


select t.create_date,count(*) from AQF_FORECAST_ONE_DAY_WX_PM25 t group by t.create_date order by t.create_date,count(*);
select t.create_date,count(*) from AQF_FORECAST_ONE_DAY_WX_O3 t  group by t.create_date order by t.create_date,count(*);


--select t.create_date,count(*) from AQF_FORECAST_ONE_DAY_WX_PM10 t where t.pointid = 3 or t.pointid = 5  group by t.create_date order by t.create_date,count(*);
--select t.create_date,count(*) from AQF_FORECAST_ONE_DAY_WX_PM10 t where t.pointid = 3 or t.pointid = 5 or t.pointid = 7  group by t.create_date order by t.create_date,count(*);
--select t.create_date,count(*) from AQF_FORECAST_ONE_DAY_WX_PM10 t where t.pointid = 3 or t.pointid = 5 or t.pointid = 7 or t.pointid = 12  group by t.create_date order by t.create_date,count(*);
select count(*) from AQF_FORECAST_ONE_DAY_WX_PM25;
