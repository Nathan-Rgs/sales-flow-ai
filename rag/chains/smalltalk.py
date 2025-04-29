from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from config import LLM_MODEL, OLLAMA_URL, GENERIC_SYSTEM_PROMPT

llm = ChatOllama(model=LLM_MODEL, base_url=OLLAMA_URL, temperature=0.0, streaming=False)

smalltalk_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GENERIC_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template("Usuário: {input}")
])

smalltalk_chain = LLMChain(llm=llm, prompt=smalltalk_prompt)
