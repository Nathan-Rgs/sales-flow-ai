import gradio as gr

from graph import route_and_generate
from chains.price      import price_chain
from chains.info       import info_chain
from chains.smalltalk  import smalltalk_chain

async def chat_fn(user_message: str, history: str) -> str:
    if not history:
        info_chain.memory.memories[0].clear()
        price_chain.memory.clear()
        smalltalk_chain.memory.clear()

    assistant_reply = await route_and_generate(user_message)
    return assistant_reply

if __name__ == "__main__":
    gr.ChatInterface(
        fn=chat_fn,
        title="Assistente de Vendas JVF Máquinas",
        description=(
            "Sou um assistente comercial da JVF Máquinas. "
            "Posso te ajudar com informações sobre nossas mandriladoras e atendimento técnico."
        ),
        theme="default",
        type="messages",
    ).launch(inbrowser=True, share=False, debug=True)
