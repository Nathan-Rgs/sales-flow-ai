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

def get_prompt_from_file(path: str) -> str:
    """
    Function to get a prompt in a file content from File System.

    Parameters
    ----------
    path : str
        Absolute or relative file path.

    Returns
    -------
    str
        Content of file.
    """
    return open(file=path, mode='r', encoding='utf8').read()
