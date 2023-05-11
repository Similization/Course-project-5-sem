select user_id, user_group
from recruiting_test.internal_user
where login = '$login'
  and password = '$password'
;
