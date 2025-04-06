import os
import sys
from dotenv import load_dotenv
import warnings

from langchain_community.vectorstores import Chroma
from flask import Flask, render_template, jsonify, request
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser

from src.logger import logging
from src import constants
from src.helper import repo_ingestion, load_embedding_model, get_prompt, format_docs

load_dotenv()
warnings.filterwarnings("ignore")
logger = logging.getLogger("App")
embeddings = load_embedding_model()
persist_directory = constants.VECTOR_DB_DATA_PATH
app = Flask(__name__)

## Loading the Vector DB
vectorDB = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

## Loading embedding model
llm_model = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"), 
    model=constants.LLM_MODEL_NAME, 
    temperature=constants.LLM_MODEL_TEMPERATURE_VALUE, 
    top_p=0.8,
    convert_system_message_to_human=constants.CONVERT_TO_HUMAN_MESSAGE
)

## Loading memory for Chat chain
memory = ConversationSummaryMemory(llm=llm_model, memory_key = "chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(
    llm_model,
    retriever=vectorDB.as_retriever(search_type="mmr", search_kwargs={"k": constants.TOP_SIMILAR_RECORDS}), 
    memory=memory
)

## Creating Rag Chain using LLM expressions
llm_prompt = get_prompt()
rag_chain = (
    {
        "context": vectorDB.as_retriever(
            search_type="mmr", search_kwargs={"k": constants.TOP_SIMILAR_RECORDS}
        ) | format_docs, 
        "question": RunnablePassthrough()
    }
    | llm_prompt
    | llm_model
    | StrOutputParser()
)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')



@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        repo_ingestion(user_input)
        os.system("python store_index.py")

    return jsonify({"response": str(user_input) })

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)

    if input == "clear":
        os.system("rm -rf repo")

    ## Using Langchain QA Chain
    # result = qa.invoke(input)
    # print(result['answer'])
    # return str(result["answer"])
    ## Using Langchain Expression Language 
    result = rag_chain.invoke(input=input)
    print(result)
    return str(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)