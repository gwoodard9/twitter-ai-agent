from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI()
llm.invoke("how can langsmith help with testing?")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])
chain = prompt | llm 
api_key = os.getenv('OPENAI_API_KEY')
chain.invoke({"input": "how can langsmith help with testing?"})
output_parser = StrOutputParser()