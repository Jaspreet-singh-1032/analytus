import typing


class Query(object):
    """
    query structure to be used by frontend
    to retrieve data

    eg:-
    {
        "query": {
            "author": "random",
            "date": {"$lt": someDate}
        },
        "sorting": {
            "username": 1, # Ascending by username
            "created": -1  # Descending by created
        }
    }
    """

    query = typing.Dict[str, typing.Union[str, dict]]
    sorting = typing.Dict[str, typing.Literal[-1, 1]]
