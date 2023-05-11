select vacancy_id,
       open_date,
       close_date,
       info,
       criteria,
       criteria_full,
       job_id,
       job_name,
       min_salary,
       max_salary,
       division_code
from recruiting_test.vacancy
         join recruiting_test.staffing using (job_id)
where close_date is null
;
