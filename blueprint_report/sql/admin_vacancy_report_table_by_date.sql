select year,
       month,
       vacancy_report_id,
       vacancy_id,
       job_name,
       candidate_count
from recruiting_test.vacancy_report
where year = '$year'
  and month = '$month'
group by year, month, vacancy_report_id
;
