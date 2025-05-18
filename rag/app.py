import uuid
import gradio as gr
from graph import route_and_generate

async def chat_fn(user_message: str, history: list, session_id: str):
    # Inicializa a lista de turnos (cada turno = [usuário, assistente])
    history = history or []

    # Gera session_id uma única vez
    if session_id is None:
        session_id = str(uuid.uuid4())

    # Chama seu pipeline (com RunnableWithMessageHistory)
    assistant_reply = await route_and_generate(
        user_message=user_message,
        session_id=session_id
    )

    # Append como uma tupla/lista de 2 elementos
    history.append([user_message, assistant_reply])

    # Retorna o histórico de turnos e o session_id
    return history, session_id

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("""
        ## Assistente de Vendas JVF Máquinas  
        * Posso te ajudar com informações sobre nossas mandriladoras e atendimento técnico.
        """)
        chatbot      = gr.Chatbot()
        session_state = gr.State(None)
        txt_input     = gr.Textbox(
            placeholder="Digite sua mensagem…",
            show_label=False
        )

        txt_input.submit(
            fn=chat_fn,
            inputs=[txt_input, chatbot, session_state],
            outputs=[chatbot, session_state]
        )
        txt_input.submit(lambda: "", None, txt_input)

    demo.launch(inbrowser=True, share=False, debug=True)
