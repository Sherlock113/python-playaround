from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOllama

summary_template = """
    Based on the information {information} provided, I want you to:
    1. Write a short summary
    2. Translate it into Simplified Chinese
"""

information = """
    Add your info here
"""

summary_prompt_template = PromptTemplate(
    input_variables=["information"], template=summary_template
)
# temperature decides how creative the model will be, 0 means no creativity
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

# use Ollama for a local llm
# llm = ChatOllama(model="llama3")

chain = summary_prompt_template | llm

result = chain.invoke(input={"information": information})
print(result.content)
