from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.prompts.base import BasePromptTemplate
from common import get_prompt_from_file
from decouple import config

class InfoPrompter():        

    @classmethod
    def get_prompter(cls) -> BasePromptTemplate:
        return InfoPrompter.__get_chat_prompt_template()

    @classmethod
    def __get_chat_prompt_template(cls) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                get_prompt_from_file(
                    path=config('PROMPT_GENERIC_FOLDER_PATH')
                )
            ),
            MessagesPlaceholder("chat_history"),
            HumanMessagePromptTemplate.from_template("""
                Abaixo há informações úteis do nosso conhecimento.
                Contexto: {context}
                Pergunta: {question}
            """),
        ])
