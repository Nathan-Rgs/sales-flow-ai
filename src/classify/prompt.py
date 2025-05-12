from common import get_tags
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from typing import List

class ClassifierPrompterFactory():

    @classmethod
    def factory_prompter(cls) -> BasePromptTemplate:
        return ClassifierPrompterFactory.__get_chat_prompt_template()

    @classmethod
    def __get_chat_prompt_template(cls) -> PromptTemplate:
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
