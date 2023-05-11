select year, month
from recruiting_test.employee_report
where year =  '$year' and month = '$month'
group by month, year
;
