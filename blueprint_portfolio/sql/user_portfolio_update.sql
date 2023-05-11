update recruiting_test.portfolio
set name='$portfolio_name',
    birth_date='$portfolio_birth_date',
    address='$portfolio_address',
    sex='$portfolio_sex',
    about='$portfolio_about'
where portfolio_id = '$portfolio_id'
;
