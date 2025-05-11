from decouple import config
from typing import List

def get_tags() -> List[str]:
    """
    Function to acces environment variables, and get the tags for classification as a string list.

    Returns
    -------
    List[str]
        String list of the tags.
    """
    tags: str = config('TAGS')
    return tags.lower().split(sep=', ')
