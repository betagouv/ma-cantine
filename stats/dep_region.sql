-- we did not save department and region data in the TD object or any JSON data :(
select *
from
data_teledeclaration
left join (
    select distinct city_insee_code, department, region from data_canteen
    -- our geolocation bot hasn't been run yet on some lines so check both insee code and dep fields
    where city_insee_code is not null and city_insee_code != '' and department is not null and department != ''
) as geo_data
on city_insee_code = declared_data -> 'canteen' ->> 'city_insee_code'
where data_teledeclaration.year = 2022 and data_teledeclaration.status = 'SUBMITTED'
