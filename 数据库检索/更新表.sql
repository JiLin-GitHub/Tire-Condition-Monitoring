select count(*) from PRODATA t;
update prodata t set t.pointid=t.so2pointid,t.factor_code='a34004',t.create_date=t.so2create_date,
       t.date_processed=t.so2date_processed,t.temperature=t.so2temperature,t.pressure=t.so2pressure,
       t.humidity=t.so2humidity,t.wind_speed=t.so2wind_speed,t.wind_direction=t.so2wind_direction,
       t.rainfall=t.so2rainfall,t.cloudage=t.so2cloudage
       where t.pointid is NULL and t.so2pointid is not NULL;
