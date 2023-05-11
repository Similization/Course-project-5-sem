select year,
       month,
       employee_report_id,
       employee_id,
       employee_name,
       interview_count
from recruiting_test.employee_report
where year = '$year'
  and month = '$month'
group by month, year, employee_report_id
;
