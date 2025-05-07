# graph.py

from chains.router     import router_chain
from chains.price      import price_chain
from chains.info       import info_chain
from chains.smalltalk  import smalltalk_chain

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

async def route_and_generate(user_message: str) -> str:
    # 1) Detecta a intenção utilizando o método ainvoke
    router_result = await router_chain.ainvoke({"input": user_message})
    intent = router_result.get("text", "").strip().lower()
    print(f"[router] Intenção detectada: {intent}")

    cfg = _dispatch_map.get(intent)
    if not cfg:
        return "Desculpe, não entendi sua intenção."

    chain = cfg["chain"]
    key = cfg["input_key"]

    # 2) Executa sempre com ainvoke
    result = await chain.ainvoke({key: user_message})

    # 3) Se vier dict, trata specially a info_chain
    if isinstance(result, dict):
        if "answer" in result:
            # log de fontes
            for doc in result.get("source_documents", []):
                print("Fonte:", doc.metadata.get("source", "<sem source>"))
            return result["answer"]
        # para price_chain e smalltalk_chain (LLMChain), usa a chave padrão 'text'
        return result.get("text", next(iter(result.values())))

    # 4) Fallback: se não for dict, retorna como string
    return str(result)
