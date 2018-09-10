select * from PRODATA t order by t.create_date, to_number(t.pointid);
select count(*) from PRODATA t;
(select t.create_date,t.pointid,count(*) from prodata t-- where t.create_date>=to_date('2016/5/1 0','YYYY-MM-DD HH24') and t.create_date < to_date('2016/6/1 0','YYYY-MM-DD HH24')
group by t.create_date,t.pointid having count(*)>=1) order by t.create_date, to_number(t.pointid);
select t.create_date,count(*) from PRODATA t group by t.create_date order by t.create_date;
select distinct t.create_date,count(*) from PRODATA t group by t.create_date having count(*)>13 order by t.create_date;
select t.pointid,count(*) from  PRODATA t group by t.pointid;
