select interview_id        as 'ID интервью',
       e.name              as 'интервьюер',
       interview_enroll_id as 'ID заявки',
       date                as 'дата',
       result              as 'результат собседования',
       portfolio_id        as 'ID портфолио',
       user_id             as 'ID пользователя'
from recruiting_test.interview
         left join recruiting_test.employee e using (employee_id)
         left join recruiting_test.interview_enroll using (interview_enroll_id)
where employee_id is null
;