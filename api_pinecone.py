from flask import Flask, jsonify,request
from codepine import chatpine
from codepine import pinellm
import sys,os
from flask_cors import CORS

import warnings
warnings.filterwarnings('ignore')
from api_keys import gpt_api_key # as we are using Open_Ai embeddings
from langchain.embeddings import OpenAIEmbeddings
import openai



import pinecone   #connecting vector database
pinecone.init( api_key='68885954-209b-49e3-bb73-1c9d930aa87b', environment='gcp-starter')      
index = pinecone.Index('dellbot')



app = Flask(__name__)
CORS(app) 
@app.route('/')
def test():
    return "Hello"

CORS(app) 
@app.route("/pvt",methods=['POST'])
def text():
    try:
        print("**************************************")
        print(request.data)
        print(type(request.data))
        userinput = request.data.decode('utf-8')
        print(userinput)
        print(type(userinput))
        response = chatpine(userinput)
        return jsonify(response)

        
    except Exception as e:
        print("Exception ",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify("Failed1")
    
CORS(app) 
@app.route("/pub",methods=['POST'])
def function():
    try:

        print("**************************************")
        print(request.data)
        print(type(request.data))
        usertext = request.data.decode('utf-8')
        
        print(usertext)
        print(type(usertext))
        result = pinellm(usertext)
        return jsonify(result)

        
    except Exception as e:
        print("Exception ",e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify("Failed2")

if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug=True,port=8220)








