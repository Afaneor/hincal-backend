import rules
from rules.predicates import always_true

rules.set_perm('hincal.view_indicator', always_true)
rules.set_perm('hincal.add_indicator', always_true)
rules.set_perm('hincal.change_indicator', always_true)
rules.set_perm('hincal.delete_indicator', always_true)
rules.set_perm('hincal.list_indicator', always_true)
