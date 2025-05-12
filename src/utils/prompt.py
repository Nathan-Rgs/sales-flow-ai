from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from interface.prompt import PrompterFactoryInterface
from utils.common import get_tags
from typing import List

class PrompterFactory(PrompterFactoryInterface):        

    @classmethod
    def factory_prompter(cls, tag: str | None,  system_msg: str | None, human_msg: str | None) -> BasePromptTemplate:
        if tag == None: return PrompterFactory.__get_prompt_template()
        else:
            if tag not in get_tags():
                raise ValueError("'tag' must be a valid chain tag.")
            elif system_msg == None or len(system_msg) <= 1 or human_msg == None or len(human_msg) <= 1 :
                raise ValueError("'system_msg' and 'human_msg' must have a text to create a prompt.")
            return PrompterFactory.__get_chat_prompt_template(
                system_msg=system_msg, human_msg=human_msg
            )

    @classmethod
    def __get_chat_prompt_template(cls, system_msg: str, human_msg: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_msg),
            HumanMessagePromptTemplate.from_template(human_msg),
        ])

    @classmethod
    def __get_prompt_template(cls) -> PromptTemplate:
        tags: List[str] = get_tags()
        return PromptTemplate(
            input_variables=["input"],
            template=f"""
            Classifique a mensagem em exatamente uma destas categorias:
            - {tags[0]}
            - {tags[1]}
            - {tags[2]}

            Retorne apenas a etiqueta (em caixa baixa).

            Mensagem: {{input}}
            """
        )
