from common import get_tags
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from typing import List

class ClassifyPrompter():
    templater: BasePromptTemplate

    def __init__(self):
        tags: List[str] = get_tags()
        self.templater = PromptTemplate(
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

    def get_templater(self) -> BasePromptTemplate:
        return self.templater
