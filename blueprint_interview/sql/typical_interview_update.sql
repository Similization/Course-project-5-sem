update recruiting_test.interview
set employee_id         = '$interview_interviewer',
    interview_enroll_id = '$interview_enroll_id',
    date                = '$interview_date',
    result              = '$interview_result'
where interview_id = '$interview_id'
;
