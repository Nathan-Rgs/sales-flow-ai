# memory/shared_memory.py

import os
from pathlib import Path
from langchain_community.chat_message_histories import FileChatMessageHistory

def shared_history(session_id: str):
  folder = Path("rag/memory/history/global")
  folder.mkdir(parents=True, exist_ok=True)

  path = folder / f"{session_id}.json"
  
  print(f"[histórico] Usando arquivo: {path}")
  if path.exists():
    print("[histórico] ✅ Histórico já existe")
    print("[histórico] Conteúdo:")
    with open(path, "r", encoding="utf-8") as f:
      print(f.read())
  else:
    print("[histórico] ❌ Histórico ainda não existe")

  return FileChatMessageHistory(path)
