from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
from src.infra.setting import Settings

llm = OllamaLLM(model="llama3.2:1b", temperature=0.2, verbose=False, base_url=Settings().LLM_URL)

class LLMService:
    @staticmethod
    def agent_invoke(prompt_template: str, context_data: Dict[str, Any]) ->  str:
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | llm
        response = chain.invoke(context_data)
        return response
