import uuid
import gradio as gr
from graph import route_and_generate

def user_message_fn(user_message, history, session_id):
    history = history or []
    if session_id is None:
        session_id = str(uuid.uuid4())
    history.append({"role": "user", "content": user_message})
    return history, session_id

async def bot_response_fn(history, session_id):
    last_user_msg = history[-1]["content"]
    assistant_reply = await route_and_generate(
        user_message=last_user_msg,
        session_id=session_id
    )
    history.append({"role": "assistant", "content": assistant_reply})
    return history

with gr.Blocks(title="Assistente de Vendas JVF Máquinas") as demo:
    gr.Markdown("""
    ## Assistente de Vendas JVF Máquinas  
    *Posso ajudar com informações sobre nossas mandriladoras portáteis e atendimento técnico.*
    """)
    chatbot = gr.Chatbot(type="messages")
    session_state = gr.State(None)

    with gr.Row():
        with gr.Column(scale=8):
            txt_input = gr.Textbox(
                placeholder="Digite sua mensagem…",
                show_label=False,
                lines=1
            )
        with gr.Column(scale=2):
            send_btn = gr.Button("Enviar")

    txt_input.submit(
        user_message_fn,
        [txt_input, chatbot, session_state],
        [chatbot, session_state]
    ).then(
        lambda: "",
        [],
        [txt_input]
    ).then(
        bot_response_fn,
        [chatbot, session_state],
        [chatbot]
    )

    send_btn.click(
        user_message_fn,
        [txt_input, chatbot, session_state],
        [chatbot, session_state]
    ).then(
        lambda: "",
        [],
        [txt_input]
    ).then(
        bot_response_fn,
        [chatbot, session_state],
        [chatbot]
    )

    demo.launch(inbrowser=True, share=False, debug=True)
