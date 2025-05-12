from decouple import config
from pathlib import Path
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

def get_shared_history(session_id: int) -> BaseChatMessageHistory:
  """
  Function to get persisted memory.

  Parameters
  ----------
  session_id : int
      Unique identifier for the conversation.

  Returns
  -------
  BaseChatMessageHistory
      Abstract base class for storing chat message history.
  """
  folder = Path(config('MEMORY_FOLDER_PATH'))
  path = folder / f"{session_id}.json"
  return FileChatMessageHistory(path)
