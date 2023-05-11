select vacancy_id,
       user_id,
       portfolio_id,
       enroll_date,
       interview_id,
       employee_id,
       interview_enroll_id,
       date,
       result
from recruiting_test.interview_enroll
         left join recruiting_test.interview using (interview_enroll_id)
where vacancy_id = '$vacancy_id'
  and user_id = '$user_id'
;
