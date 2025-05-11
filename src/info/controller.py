from common import get_prompt_from_file
from decouple import config
from model.factory import ModelFactory
from info.prompt import InfoPrompterFactory
from info.retreive import InfoRetreiver
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

class InfoController():
    __retriver: InfoRetreiver
    __model: BaseChatModel
    __chain: Runnable

    def __init__(self):
        self.__model = ModelFactory().connect_factory(temperature=0.8)
        self.__retriver = InfoRetreiver()
        self.__retriver.connect_database()
        self.__retriver.init_retreiver()
        self.__setup()

    def __setup(self) -> None:
        qa_chain: Runnable = create_stuff_documents_chain(
            llm=self.__model,
            prompt=InfoPrompterFactory().factory_prompter(
                system_msg=get_prompt_from_file(path=config('PROMPT_GENERIC_FOLDER_PATH')),
                human_msg="""
                    Abaixo há informações úteis do nosso conhecimento
                    Contexto: {context}
                    Pergunta: {question}
                """
            )
        )
        self.__chain: Runnable = create_retrieval_chain(
            retriever=self.__retriver.get_retriver(),
            combine_docs_chain=qa_chain
        )

    async def get_response(self, input: str) ->  str:
        result = await self.__chain.ainvoke({"input": input, "chat_history": []})
        return self.__process_response(msg=result)

    def __process_response(self, msg: str) -> str:
        return str(msg).lower()
