from src.helper import load_data,chunking,downloading_embedding_model
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint


load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
HF_TOKEN=os.environ.get('HF_TOKEN')
os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
os.environ['HF_TOKEN']=HF_TOKEN 

# extracted_data=load_data(data='C:/setup/Medical-Bot/Data')
# chunks=chunking(extracted_data=extracted_data)
embeddings=downloading_embedding_model()

index_name='miniproject'
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

def load_llm(repo):
    llm=HuggingFaceEndpoint(
        repo_id=repo,
        temperature=0.5,
        model_kwargs={'token':HF_TOKEN,
                      'max_length':'500'
        }
    )
    return llm