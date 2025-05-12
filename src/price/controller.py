from utils.common import get_prompt_from_file
from decouple import config
from model.factory import ModelFactory
from utils.prompt import PrompterFactory
from database.database import Database
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable, RunnableWithMessageHistory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from memory.shared_memory import get_shared_history

class PriceController():

    __db: Database
    __model: BaseChatModel
    __chain: Runnable

    def __init__(self):
        self.__model = ModelFactory().connect_factory(temperature=0.0)
        self.__db = Database()
        self.__db.connect_database()
        self.__db.init_retreiver()
        self.__init_chain()

    def __init_chain(self) -> None:
        price_prompt = PrompterFactory().factory_prompter(
            system_msg=get_prompt_from_file(config('PRICE_GENERIC_FOLDER_PATH')),
            human_msg="""
                Responda **EXATAMENTE** o valor em reais, e complemente com as informações necessárias.
                Histórico da conversa:\n{chat_history}\n
                Catálogo de produtos:\n{context}\n
                Pergunta: Qual é o preço em reais do produto “{question}”?"""
        )
        self.__chain = RunnableWithMessageHistory(
            runnable=ConversationalRetrievalChain.from_llm(
                llm=self.__model,
                retriever=self.__db.get_retriver(),
                return_source_documents=True,
                chain_type="stuff",
                combine_docs_chain_kwargs={"prompt": price_prompt},
            ),
            get_session_history=get_shared_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

    async def get_response(self, input: str, session_id: str) ->  str:
        result = await self.__chain.ainvoke(
            input={"question": input},
            config={"configurable": {"session_id": session_id}}
        )
        return self.__process_response(msg=result)

    def __process_response(self, msg) -> str:
        if isinstance(msg, dict):
            if "answer" in msg: return msg["answer"]
            return msg.get("response") or next(iter(msg.values()), None)
        elif hasattr(msg, "content"): return msg.content
