from model.factory import ModelFactory
from info.prompt import InfoPrompter
from info.retreive import InfoRetreiver
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

class InfoController():
    __prompter: InfoPrompter
    __model: BaseChatModel
    __chain: ConversationalRetrievalChain

    def __init__(self):
        self.__prompter = InfoPrompter().get_prompter()
        self.__model = ModelFactory().connect_factory(temperature=0.8)
        self.__retreiver = InfoRetreiver()
        self.__retreiver.factory_connect_database()
        self.__retreiver.factory_retreiver()
        self.__chain = ConversationalRetrievalChain.from_llm(
            llm=self.__model,
            retriever=self.__retreiver.get_retriver(),
            memory=None,
            return_source_documents=False,
            combine_docs_chain_kwargs={"prompt": self.__prompter},
        )

    async def get_response(self, input: str) ->  str:
        result = await self.__chain.ainvoke(input=input, chat_history=[()])
        return self.__process_response(msg=result)

    def __process_response(self, msg: str) -> str:
        return str(msg).lower()
