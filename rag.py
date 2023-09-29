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



dataset = load_dataset(
    "jamescalam/llama-2-arxiv-papers-chunked",
    split="train"
)
load_dotenv()

chat = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-3.5-turbo'
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="How does next-seo work?")
]

# get API key from app.pinecone.io and environment from console
pinecone.init(
    api_key=os.environ['PINECONE_API_KEY'] ,
    environment=os.environ['PINECONE_ENV']
)

index = pinecone.Index('rag-test')

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")

data = dataset.to_pandas()  # this makes it easier to iterate over the dataset

batch_size = 100

for i in tqdm(range(0, len(data), batch_size)):
    i_end = min(len(data), i+batch_size)
    # get batch of data
    batch = data.iloc[i:i_end]
    # generate unique ids for each chunk
    ids = [f"{x['doi']}-{x['chunk-id']}" for i, x in batch.iterrows()]
    # get text to embed
    texts = [x['chunk'] for _, x in batch.iterrows()]
    # embed text
    embeds = embed_model.embed_documents(texts)
    # get metadata to store in Pinecone
    metadata = [
        {'text': x['chunk'],
         'source': x['source'],
         'title': x['title']} for i, x in batch.iterrows()
    ]
    # add to Pinecone
    index.upsert(vectors=zip(ids, embeds, metadata))

print(index.describe_index_stats())





