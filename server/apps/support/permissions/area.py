import rules
from rules.predicates import always_true

rules.set_perm('support.view_area', always_true)
rules.set_perm('support.list_area', always_true)
