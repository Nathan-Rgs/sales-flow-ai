from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.prompts.base import BasePromptTemplate

class SmalltalkPrompterFactory():        

    @classmethod
    def factory_prompter(cls, system_msg: str, human_msg: str) -> BasePromptTemplate:
        return SmalltalkPrompterFactory.__get_chat_prompt_template(system_msg=system_msg, human_msg=human_msg)

    @classmethod
    def __get_chat_prompt_template(cls, system_msg: str, human_msg: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_msg),
            HumanMessagePromptTemplate.from_template(human_msg),
        ])
