from enum import Enum


class GroupType(Enum):
    LANGUAGE = 1
    LICENSE = 2
    DEFAULT_BRANCH = 3
    HAS_ISSUES = 4
    HAS_PROJECTS = 5
    HAS_DOWNLOADS = 6
    HAS_WIKI = 7
    HAS_PAGES = 8
    HAS_DISCUSSIONS = 9
    IS_FORK = 10
    IS_ARCHIVED = 11
    IS_TEMPLATE = 12
