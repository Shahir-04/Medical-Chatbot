from flask import Flask,render_template,redirect,request
from src.helper import downloading_embedding_model
from src.store_index import load_llm
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
import os
from dotenv import load_dotenv
from db import Database
import re


app=Flask(__name__)
db=Database()
load_dotenv()
PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
HF_TOKEN_TESt=os.environ.get('HF_TOKEN_TEST')
os.environ['PINECONE_API_KEY']=PINECONE_API_KEY
os.environ['HF_TOKEN']=HF_TOKEN_TESt 

embeddings=downloading_embedding_model()

index_name='miniproject'
docsearch=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=docsearch.as_retriever(search_type='similarity',search_kawgs={'k':3})

hugging_face_repo='mistralai/Mistral-7B-Instruct-v0.3'
llm=load_llm(hugging_face_repo)

prompt=ChatPromptTemplate.from_messages(
    [
        ('system',system_prompt),
        ('human','{input}')
    ]
)


question_ans_chain=create_stuff_documents_chain(llm,prompt)
rag_chain=create_retrieval_chain(retriever,question_ans_chain)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/bot')
def bot():
    return render_template('bot.html')

@app.route('/get',methods=['GET','POST'])
def chat():
    msg = request.form['msg']
    print("User:", msg)
    if msg.lower().strip() in ['hi','hello','hey']:
        return "Hello! How can i help u"
    else:
        response = rag_chain.invoke({'input': msg})
        answer = re.sub(r'^.*?(Assistant:|Answer:)\s*', '', response['answer'], flags=re.DOTALL)
        print(answer.strip())

        # print(type(answer))
        # print(response)
    #     if answer.lower().startswith("? answer"):
    #         answer = answer[8:].strip()  # Remove "? Answer" (8 characters) 

    # # Normalize "I don't know" response
    #     if answer.lower().startswith(" Answer: The context provided does not mention a "):
    #         answer = "I don't know."

        print("Response:", answer)
        return str(answer)
        # print("Response:",answer)
        # return answer


@app.route('/perform_login', methods=['post'])
def perform_login():
    email=request.form.get('email')
    password=request.form.get('password')
    search=db.find(email=email,password=password)
    if search:
        return redirect('/bot')
    else:
        return render_template('home.html',message='Invalid email or password')

@app.route('/enter',methods=['post'])
def enter():
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    print(username,email,password)
    response=db.register(name=username,email=email,password=password)
    if response:
        return render_template('home.html',message='Successfully Register,Please login!')
    else:
        return render_template('register.html',message='Email already Exists')


if __name__=='__main__':
    app.run(debug=True)