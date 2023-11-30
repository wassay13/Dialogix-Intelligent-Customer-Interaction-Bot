
from langchain.embeddings import OpenAIEmbeddings
from api_keys import gpt_api_key 
import openai
from langchain.llms import OpenAI
import warnings
warnings.filterwarnings('ignore')
import re
import os
os.environ['OPENAI_API_KEY'] = gpt_api_key
openai.api_key = "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"


import pinecone   #connecting vector database
pinecone.init( api_key='68885954-209b-49e3-bb73-1c9d930aa87b', environment='gcp-starter')      
index = pinecone.Index('dellbot')



def chatpine(query):
    pinecone.init( api_key='68885954-209b-49e3-bb73-1c9d930aa87b', environment='gcp-starter')      
    index = pinecone.Index('dellbot')
   
    # most similar from vector database
    embeddings_model = OpenAIEmbeddings(api_key=gpt_api_key)
    query_em = embeddings_model.embed_query(query)
    result = index.query(query_em,top_k=1,include_metadata=True)
    k = 2
    temp_context = [result['matches'][i]['metadata']['text'] for i in range(k)],[result['matches'][i]['metadata']['text'] for i in range(k)]
    context = str(temp_context[0][0])
    header = """Answer the question as truthfully as possible using the provided context below,
                and if the answer is not contained within the text and requires some latest information to be updated,
                print 'Sorry Not Sufficient context to answer query' \n"""

    prompt = header + context + "\n\n" + query + "\n"
    response = openai.Completion.create(model="text-davinci-003",prompt=prompt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END'])
    a = (response.choices[0].text).strip()
    response = {"LLM_Response_With_Org_Data":a}
    
    return response

def pinellm(query):
    llm = OpenAI(temperature=0.7, model_name='text-davinci-003')
    result = llm(query)
    cleaned_string = re.sub(r'\n\n\d+\.', '', result)

    response = {"LLM_Response_with_GPT":cleaned_string}
    return response


    
# obj1 = chatpine("How should I care for my Dell laptop regarding cables and storage devices?")
# obj2 = pinellm("How should I care for my Dell laptop regarding cables and storage devices?")


# print("'''''''''''''''''With Pvt Data'''''''''''''''''''''''''''''''''''''")
# print(obj1)
# print("'''''''''''''''''With Pub Data'''''''''''''''''''''''''''''''''''''")
# print(obj2)

