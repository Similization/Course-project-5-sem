select employee_id,
       name,
       birth_date,
       address,
       education,
       job_id,
       job_name,
       salary,
       enrollment_date,
       dismissal_date
from recruiting_test.employee
         join recruiting_test.staffing s using (job_id)
where employee_id = '$employee_id'
;
