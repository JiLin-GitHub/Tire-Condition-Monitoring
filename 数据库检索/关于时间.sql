--1¡¢2¡¢3¡¢4¡¢5¡¢6¡¢7¡¢8¡¢9¡¢12¡¢31¡¢35¡¢38  £¨13¸ö£©
--select * from AQF_FORECAST_ONE_DAY_WX_PM25 t where t.create_date=to_date('2016-6-15 15','YYYY-MM-DD HH24');
select * from AQF_FORECAST_ONE_DAY_WX_PM25 t where t.create_date=to_timestamp('02-5ÔÂ -16 01.00.00 ÏÂÎç','DD-MON -YY HH.MI.SS AM');
--delete from  Aqf_Forecast_One_Day_Wx_SO2 t where t.create_date<=to_date('2017-5-16 15','YYYY-MM-DD HH24') and t.create_date>=to_date('2017-5-13 15','YYYY-MM-DD HH24');
--SELECT CAST(sysdate as timestamp(3)) from dual;

--select CAST( t.create_date AS date ) from AQF_FORECAST_ONE_DAY_WX_PM25 t;
