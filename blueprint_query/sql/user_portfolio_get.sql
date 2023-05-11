select portfolio_id,
       user_id,
       name,
       birth_date,
       address,
       sex,
       about
from recruiting_test.portfolio
where user_id = '$user_id'
  and portfolio_id = '$portfolio_id'
;
