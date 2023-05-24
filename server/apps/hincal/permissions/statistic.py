import rules
from rules.predicates import always_allow

rules.set_perm('hincal.view_statistic', always_allow)
rules.set_perm('hincal.add_statistic', always_allow)
rules.set_perm('hincal.change_statistic', always_allow)
rules.set_perm('hincal.delete_statistic', always_allow)
rules.set_perm('hincal.list_statistic', always_allow)
