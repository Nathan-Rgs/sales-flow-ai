from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.prompts.base import BasePromptTemplate
from decouple import config

class InfoPrompter():        

    @classmethod
    def get_prompter(cls) -> BasePromptTemplate:
        return InfoPrompter.__get_chat_prompt_template()

    @classmethod
    def get_prompt(cls) -> str:
        return open(
            file=config('PROMPT_GENERIC_FOLDER_PATH'),
            mode='r', encoding='utf8'
        ).read()

    @classmethod
    def __get_chat_prompt_template(cls) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                InfoPrompter().get_prompt()
            ),
            MessagesPlaceholder("chat_history"),
            HumanMessagePromptTemplate.from_template("""
                Abaixo há informações úteis do nosso conhecimento.
                Contexto: {context}
                Pergunta: {question}
            """),
        ])
