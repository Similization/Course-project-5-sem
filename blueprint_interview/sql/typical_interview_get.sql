select e.name as 'interviewer',
       employee_id as 'interviewer_id',
       interview_enroll_id,
       date,
       result
from recruiting_test.interview
         left join recruiting_test.employee e using (employee_id)
where interview_id = '$interview_id'
;
