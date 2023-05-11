insert into recruiting_test.portfolio
    (user_id, name, birth_date, address, sex, about)
    VALUE ('$portfolio_user_id', '$portfolio_name', '$portfolio_birth_date', '$portfolio_address', '$portfolio_sex',
           '$portfolio_about')
;
