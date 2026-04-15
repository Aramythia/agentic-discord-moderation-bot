from langchain_openai import ChatOpenAI


class AIService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini")