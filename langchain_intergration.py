import chainlit as cl
import openai
import os
from langchain import PromptTemplate, OpenAI, LLMChain

#os.environ['OPEN_API_KEY'] = ''
# openai.api_key = ''

# Define the prompt template with placeholders for question and answer
template = """Question: {question}

Answer: Let's think step by step."""

# Define the function to be executed when the chat starts
@cl.on_chat_start
def main():
    # Create a PromptTemplate object using the defined template
    prompt = PromptTemplate(template=template, input_variables = ["question"])

    # Initialize the OpenAI LLM with a specific temperature and streaming enabled
    llm_chain = LLMChain(prompt = prompt,llm=OpenAI(temperature=0,streaming=True),verbose=True)

    # Save the initialized llm_chain object to the user session
    cl.user_session.set("llm_chain",llm_chain)

# Define the function to be executed when a message is received
@cl.on_message
async def main(message : str):
    # Retrieve the saved llm_chain object from the user session
    llm_chain = cl.user_session.get("llm_chain")

    # Use the llm_chain to generate a response to the received message
    # The response generation is asynchronous and uses a callback handler
    res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Send the generated response back to the user
    await cl.Message(content=res["text"]).send()



