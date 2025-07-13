import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_openai import ChatOpenAI

load_dotenv()

# Load prompt template
with open("prompts/job_targeted_prompt.txt", "r") as f:
    prompt_template = f.read()

prompt = PromptTemplate.from_template(prompt_template)

# LLM setup using OpenRouter
llm = ChatOpenAI(
    model="deepseek/deepseek-r1-0528-qwen3-8b:free",
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.3
)

def get_chain():
    return (
        RunnableMap({
            "document": lambda x: x["resume"],
            "instruction": lambda x: x["job_description"]
        })
        | prompt
        | llm
        | StrOutputParser()
    )
