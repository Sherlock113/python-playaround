from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
# llm = ChatOllama(model="llama3")

# Define a chain and format the output
chain = summary_prompt_template | llm | StrOutputParser()

result = chain.invoke(input={"information": information})
print(result)
