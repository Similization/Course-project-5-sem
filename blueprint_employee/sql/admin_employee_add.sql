insert into recruiting_test.employee (name,
                                      birth_date,
                                      address,
                                      education,
                                      job_id,
                                      salary,
                                      enrollment_date,
                                      dismissal_date)
    value ('$employee_name', '$employee_birth_date',
           '$employee_address', '$employee_education',
           '$employee_job_id', '555', now(), null)
;
