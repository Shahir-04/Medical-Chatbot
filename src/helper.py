from langchain.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

def load_data(data):
    loader=DirectoryLoader(data,
                           glob='*.pdf',
                           loader_cls=PyPDFLoader)
    documents=loader.load()
    return documents


def chunking(extracted_data):
    textsplitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    text_chunks=textsplitter.split_documents(extracted_data)
    return text_chunks


def downloading_embedding_model():
    embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2') # convert the chunks into 384 dimensional dense vector
    return embeddings

