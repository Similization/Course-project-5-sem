select year, month
from recruiting_test.vacancy_report
where year =  '$year' and month = '$month'
group by year, month
;
