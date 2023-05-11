update recruiting_test.employee
set name       = '$employee_name',
    birth_date = '$employee_birth_date',
    address    = '$employee_address',
    education  = '$employee_education',
    job_id     = '$employee_job_id'
where employee_id = '$employee_id'
;
