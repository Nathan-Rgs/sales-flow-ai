from utils.common import get_prompt_from_file
from decouple import config
from utils.llm import LLMFactory
from utils.prompt import PrompterFactory
from utils.database import Database
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable, RunnableWithMessageHistory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from logging import getLogger, Logger
from interface.controller import InfoControllerInterface
from utils.shared_memory import get_shared_history

class InfoController(InfoControllerInterface):

    __db: Database
    __model: BaseChatModel
    __chain: Runnable
    __logger: Logger

    def __init__(self):
        self.__logger = getLogger('root')
        self.__model = LLMFactory().connect_factory(temperature=0.8)
        self.__db = Database()
        self.__db.connect_database()
        self.__db.init_retreiver()
        self.__init_chain()

    def __init_chain(self) -> None:
        question_prompt = PrompterFactory().factory_prompter(
            tag='info',
            system_msg=get_prompt_from_file(config('PROMPT_GENERIC_FOLDER_PATH')),
            human_msg="""
                Histórico da conversa:\n\n{chat_history}
                Contextos recuperados:\n\n{context}
                Pergunta:\n\n{question}
            """
        )
        refine_prompt = PrompterFactory().factory_prompter(
            tag='info',
            system_msg=get_prompt_from_file(config('PROMPT_GENERIC_FOLDER_PATH')),
            human_msg="""
                Histórico da conversa:\n\n{chat_history}\n
                Pergunta original:\n\n{question}\n
                Resposta-base até agora:\n\n{existing_answer}\n
                Novos contextos:\n\n{context}\n
                Por favor, refine a resposta mantendo-se fiel às fontes e ao histórico.
            """
        )
        self.__chain = RunnableWithMessageHistory(
            runnable=ConversationalRetrievalChain.from_llm(
                llm=self.__model,
                retriever=self.__db.get_retriver(),
                return_source_documents=True,
                chain_type="refine",
                combine_docs_chain_kwargs={
                    "question_prompt": question_prompt,
                    "refine_prompt": refine_prompt,
                    "document_variable_name": "context",
                },
            ),
            get_session_history=get_shared_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

    async def get_response(self, input: str, session_id: str) -> str:
        self.__logger.info("Invoking response from Info Chain")
        result = await self.__chain.ainvoke(
            input={"question": input},
            config={"configurable": {"session_id": session_id}}
        )
        return self.__process_response(msg=result)

    def __process_response(self, msg) -> str:
        self.__logger.info("Processing response from Info Chain")
        if isinstance(msg, dict):
            if "answer" in msg: return msg["answer"]
            return msg.get("response") or next(iter(msg.values()), None)
        elif hasattr(msg, "content"): return msg.content
