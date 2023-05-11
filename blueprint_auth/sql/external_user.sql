select user_id, NULL as user_group
from recruiting_test.external_user
where login = '$login'
  and password = '$password'
;
