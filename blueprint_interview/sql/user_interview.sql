select job_name as 'вакансия',
       date as 'дата',
       result as 'результат собсеседования',
       portfolio_id as 'ID портфолио',
       vacancy_id as 'ID вакансии',
       user_id as 'ID пользователя'
from recruiting_test.interview
         join recruiting_test.interview_enroll using (interview_enroll_id)
         join recruiting_test.vacancy using (vacancy_id)
         join recruiting_test.staffing using (job_id)
where user_id = '$user_id'
;
