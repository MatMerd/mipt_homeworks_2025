from enum import Enum


class WhereType(Enum):
    NAME = 1
    DESCRIPTION = 2
    URL = 3
    CREATED_AT = 4
    UPDATED_AT = 5
    HOMEPAGE = 6
    SIZE = 7
    STARS = 8
    FORKS = 9
    ISSUES = 10
    WATCHERS = 11
    LANGUAGE = 12
    LICENSE = 13
    TOPICS_NUMBER = 14
    HAS_ISSUES = 15
    HAS_PROJECTS = 16
    HAS_DOWNLOADS = 17
    HAS_WIKI = 18
    HAS_PAGES = 19
    HAS_DISCUSSIONS = 20
    IS_FORK = 21
    IS_ARCHIVED = 22
    IS_TEMPLATE = 23
    DEFAULT_BRANCH = 24
