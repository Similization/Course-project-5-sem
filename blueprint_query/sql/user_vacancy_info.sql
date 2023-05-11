select vacancy_id,
       job_name,
       min_salary,
       max_salary,
       division_code,
       info,
       criteria,
       criteria_full
from recruiting_test.vacancy
         join recruiting_test.staffing using (job_id)
where vacancy_id = '$vacancy_id'
;
