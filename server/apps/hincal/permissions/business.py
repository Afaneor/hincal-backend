import rules
from rules.predicates import always_allow

rules.set_perm('hincal.view_business', always_allow)
rules.set_perm('hincal.add_business', always_allow)
rules.set_perm('hincal.change_business', always_allow)
rules.set_perm('hincal.delete_business', always_allow)
rules.set_perm('hincal.list_business', always_allow)
