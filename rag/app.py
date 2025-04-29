import gradio as gr
from graph import route_and_generate

async def chat_fn(user_message, history):
    # history já inclui a mensagem do usuário
    history = history or []
    # gera a resposta
    assistant_reply = await route_and_generate(user_message, history)
    # retorna só a resposta, o Gradio cuida de anexar ao histórico
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
    ).launch(inbrowser=True, share=False)
