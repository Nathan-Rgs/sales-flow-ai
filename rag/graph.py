# graph.py

from chains.router     import router
from chains.price      import price_chain
from chains.info       import info_chain
from chains.smalltalk  import smalltalk_chain
from chains.rag_conv   import conv_rag

async def route_and_generate(user_message: str, history: list) -> str:
    chat_history = [(m["role"], m["content"]) for m in history or []]

    # get the router’s reply
    router_msg = await router.ainvoke(input=user_message)
    tag = router_msg.content.strip().lower()
    print(f"Intenção: {tag}")

    if tag == "price":
        return await price_chain.ainvoke(
            input=user_message,
            chat_history=chat_history
        )
    elif tag == "info":
        return await info_chain.ainvoke(
            input=user_message,
            chat_history=chat_history
        )
    elif tag == "smalltalk":
        return await smalltalk_chain.ainvoke(input=user_message)
    else:
        return await conv_rag.ainvoke(
            input=user_message,
            chat_history=chat_history
        )
