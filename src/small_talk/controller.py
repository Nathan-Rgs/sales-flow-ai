from common import get_prompt_from_file
from decouple import config
from model.factory import ModelFactory
from small_talk.prompt import SmalltalkPrompterFactory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable, RunnableWithMessageHistory
from memory.shared_memory import get_shared_history

class SmalltalkController():

    __model: BaseChatModel
    __chain: Runnable

    def __init__(self):
        self.__model = ModelFactory().connect_factory(temperature=0.0)
        self.__init_chain()

    def __init_chain(self) -> None:
        smalltalk_prompt = SmalltalkPrompterFactory().factory_prompter(
            system_msg=get_prompt_from_file(config('PROMPT_GENERIC_FOLDER_PATH')),
            human_msg="""
                Histórico da conversa:\n{chat_history}\n
                Seja amigável e descontraído quando o usuário quiser apenas bater papo. Porém NÃO SAIA DO CONTEXTO (se sair informe que você não conhece/pode falar sobre tais assuntos), NEM SEJA ANTI PROFISSIONAL.
                "Usuário: {input}
            """
        )
        self.__chain = RunnableWithMessageHistory(
            runnable=smalltalk_prompt | self.__model,
            get_session_history=get_shared_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    async def get_response(self, input: str, session_id: str) ->  str:
        result = await self.__chain.ainvoke(
            input={"input": input},
            config={"configurable": {"session_id": session_id}}
        )
        return self.__process_response(msg=result)

    def __process_response(self, msg) -> str:
        if isinstance(msg, dict):
            if "answer" in msg: return msg["answer"]
            return msg.get("response") or next(iter(msg.values()), None)
        elif hasattr(msg, "content"): return msg.content
