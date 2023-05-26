import rules
from rules.predicates import always_true

rules.set_perm('blog.view_support', always_true)
rules.set_perm('blog.list_support', always_true)
