commands: list[str] = [
    "filter",
    "save",
    "stop",
    "help",
    "reset",
    "sort",
    "group_by",
    "save_query",
    "call",
]
int_fields: list[str] = ["size", "stars", "forks", "issues", "watchers"]
str_fields: list[str] = [
    "name",
    "description",
    "url",
    "home_page",
    "language",
    "license",
    "default_branch",
]
bool_fields: list[str] = [
    "has_issues",
    "has_projects",
    "has_downloads",
    "has_wiki",
    "has_pages",
    "has_discussions",
    "is_fork",
    "is_archived",
    "is_template",
]
datetime_fields: list[str] = ["created_at", "updated_at"]
array_fields: list[str] = ["topics"]
all_fields: list[str] = (
    int_fields + str_fields + bool_fields + datetime_fields + array_fields
)
all_fields_ordered: list[str] = [
    "name",
    "description",
    "url",
    "created_at",
    "updated_at",
    "home_page",
    "size",
    "stars",
    "forks",
    "issues",
    "watchers",
    "language",
    "license",
    "topics",
    "has_issues",
    "has_projects",
    "has_downloads",
    "has_wiki",
    "has_pages",
    "has_discussions",
    "is_fork",
    "is_archived",
    "is_template",
    "default_branch",
]
compare_operators: list[str] = ["==", "!=", "<", ">", "<=", ">="]
