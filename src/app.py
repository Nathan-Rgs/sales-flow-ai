from application.Application import ApplicationRAG
from log.setup import setup_logging
import gradio as gr
import uuid

APP = ApplicationRAG()
setup_logging()

def user_message_fn(request, history, session_id):
    history = history or []
    if session_id is None:
        session_id = str(uuid.uuid4())
    history.append({"role": "user", "content": request})
    return history, session_id

async def bot_response_fn(history, session_id):
    last_user_msg = history[-1]["content"]
    response = await APP.run(input=last_user_msg, session_id=session_id)
    history.append({"role": "assistant", "content": response})
    return history

if __name__ == "__main__":
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
            fn=user_message_fn,
            inputs=[txt_input, chatbot, session_state],
            outputs=[chatbot, session_state]
        ).then(
            fn=lambda: "",
            inputs=[],
            outputs=[txt_input]
        ).then(
            fn=bot_response_fn,
            inputs=[chatbot, session_state],
            outputs=[chatbot]
        )
        send_btn.click(
            fn=user_message_fn,
            inputs=[txt_input, chatbot, session_state],
            outputs=[chatbot, session_state]
        ).then(
            fn=lambda: "",
            inputs=[],
            outputs=[txt_input]
        ).then(
            fn=bot_response_fn,
            inputs=[chatbot, session_state],
            outputs=[chatbot]
        )
        demo.launch(inbrowser=True, share=False, debug=True)
