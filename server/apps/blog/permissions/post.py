import rules
from rules.predicates import always_allow

rules.set_perm('blog.view_post', always_allow)
rules.set_perm('blog.list_post', always_allow)
