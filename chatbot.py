

import langchain

import os
from api_keys import palm_api_key
from api_keys import gpt_api_key
from langchain.document_loaders import TextLoader
from langchain.llms import GooglePalm
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

os.environ['OPEN_API_KEY']  = palm_api_key
obj = TextLoader(file_path=r"C:\Users\user\Desktop\Chatbot\conversation_text.txt")
data = obj.load()

llmg = GooglePalm(google_api_key = palm_api_key, temprature = 0.7)
llmo = OpenAI(api_key=gpt_api_key,temperature=0.7)


embeddings_model = OpenAIEmbeddings(api_key = gpt_api_key)
vector_database = FAISS.from_documents(documents = data, embedding = embeddings_model)
# text = "This is a text document"
# result = embeddings_model.embed_query(text)
retrive_obj = vector_database.as_retriever()



from langchain.prompts import PromptTemplate
prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs = {"prompt": PROMPT}


from langchain.chains import RetrievalQA
chain = RetrievalQA.from_chain_type(llm = llmg , 
                                    chain_type = "stuff", 
                                    retriever = retrive_obj , 
                                    input_key = "query" ,
                                    return_source_documents=True,
                                    chain_type_kwargs = {"prompt":PROMPT})


print(chain(" How can I cancel the subscription plan?"))





# How can I cancel the subscription plan?
# Can you explain the pricing details for the standard plan?
# I received an email regarding the payment. Can you confirm if it's legitimate?

# I'm having trouble sharing my screen for the payment confirmation. Can you guide me?
# What steps should I follow to share a screenshot of the payment confirmation?
#Is there an automatic payment option available?

#How do I make a payment on Razor Pay?










