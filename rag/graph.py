from chains.router     import router_chain
from chains.price      import price_chain
from chains.info       import info_chain
from chains.smalltalk  import smalltalk_chain

from langchain.memory import FileChatMessageHistory, ConversationBufferMemory

# Configuração de cada intent
_dispatch_map = {
    "price": {
        "chain": price_chain,
        "input_key": "question",
    },
    "info": {
        "chain": info_chain,
        "input_key": "question",
    },
    "smalltalk": {
        "chain": smalltalk_chain,
        "input_key": "input",
    },
}

async def route_and_generate(user_message: str, session_id: str) -> str:
    # 1) Detecta a intenção com a router_chain
    router_result = await router_chain.ainvoke({"input": user_message})
    intent = router_result.content.strip().lower()
    print(f"[router] Intenção detectada: {intent}")

    # 2) Busca a chain correspondente
    cfg = _dispatch_map.get(intent)
    if not cfg:
        return "Desculpe, não entendi sua intenção."

    chain = cfg["chain"]
    key = cfg["input_key"]

    # 3) Executa a chain com session_id (para manter histórico compartilhado)
    result = await chain.ainvoke(
        {key: user_message},
        config={"configurable": {"session_id": session_id}}
    )

    # 4) Se resultado for dict (como em info/price), extrai resposta e fontes
    if isinstance(result, dict):
        if "answer" in result:
            for doc in result.get("source_documents", []):
                print("Fonte:", doc.metadata.get("source", "<sem source>"))
            return result["answer"]
        return result.get("response") or next(iter(result.values()), None)

    # 5) Se for mensagem estruturada (ex: AIMessage), extrai conteúdo
    if hasattr(result, "content"):
        return result.content

    # 6) Fallback final (string, número, etc.)
    return str(result)
