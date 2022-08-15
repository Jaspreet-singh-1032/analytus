import typing


class Query(object):
    """
    query structure to retrieve data
    """

    filters = typing.Dict[str, typing.Union[str, int]]
    sorting = typing.Dict[str, str]
    ranges = typing.Dict[str, typing.Dict[str, typing.Union[str, int]]]
