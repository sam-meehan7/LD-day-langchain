# L&D Day 29/09/23 -

LangChain, VectorDb, embeddings and more!

## Description

This project contains scripts that interact with the Pinecone, OpenAI, and Datasets Python libraries to perform tasks related to natural language processing and information retrieval. The scripts leverage the OpenAI API to initialize chat models, perform embedding on text documents, and interact with Pinecone indices.

## Scripts

### Script 1: [rag.py]

This script performs tasks such as initializing a Pinecone index, embedding text documents from a dataset, and upserting them to the Pinecone index. The script utilizes the OpenAI API for embedding documents.

### Script 2: [vectors.py]

This script initializes a Pinecone index and a chat model using the OpenAI API. It performs a similarity search on the index and augments the prompt based on the retrieved documents.
