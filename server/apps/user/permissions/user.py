import rules
from rules.predicates import always_true

rules.set_perm('user.view_user', always_true)
rules.set_perm('user.add_user', always_true)
rules.set_perm('user.change_user', always_true)
rules.set_perm('user.delete_user', always_true)
rules.set_perm('user.list_user', always_true)
