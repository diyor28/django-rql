from ctypes import Union
from typing import List, Iterable, TypedDict


class RQL_FILTER_TYPE(TypedDict, total=False):
    filter: str
    namespace: str
    source: str
    sources: Iterable
    custom: bool
    dynamic: bool
    field: dict
    lookups: set
    qs: dict
    use_repr: str
    ordering: bool
    search: bool
    hidden: bool


RQL_FILTERS_TYPE = Union[List[str], List[RQL_FILTER_TYPE]]
