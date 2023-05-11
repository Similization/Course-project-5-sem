insert into recruiting_test.interview_enroll (vacancy_id, user_id, portfolio_id, enroll_date)
values ('$vacancy_id', '$user_id', null, now())
on duplicate key update vacancy_id=vacancy_id
;
