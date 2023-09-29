import os
import pinecone
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from datasets import load_dataset
from langchain.embeddings.openai import OpenAIEmbeddings
from tqdm.auto import tqdm  # for progress bar
from langchain.vectorstores import Pinecone


load_dotenv()

chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
)

# get API key from app.pinecone.io and environment from console
pinecone.init(
    api_key=os.environ['PINECONE_API_KEY'] ,
    environment=os.environ['PINECONE_ENV']
)

index = pinecone.Index('rag-test')

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")

text_field = "text"  # the metadata field that contains our text

# initialize the vector store object
vectorstore = Pinecone(
    index, embed_model.embed_query, text_field
)

query = "What is so special about Llama 2?"

def augment_prompt(query: str):
    # get top 3 results from knowledge base
    results = vectorstore.similarity_search(query, k=3)
    # get the text from the results
    source_knowledge = "\n".join([x.page_content for x in results])
    # feed into an augmented prompt
    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augmented_prompt

print(augment_prompt(query))








