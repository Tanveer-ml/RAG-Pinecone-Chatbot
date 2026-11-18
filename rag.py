import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone,ServerlessSpec

#Load the environment variable
load_dotenv()

#Get the api key
openai_api_key = os.getenv("OPENAI_API_KEY")
#Get the pinecone api key
pinecone_api_key = os.getenv("PINECONE_API_KEY")

#Create OpenAI Client
client = OpenAI(api_key=openai_api_key)

#Create Pinecone Client
pc = Pinecone(api_key=pinecone_api_key)

#Pinecone Index Configuration
index_name = "company-policy-docs"
dimensions = 1536
index = pc.Index(index_name)


def ask_question(question):
    #Create embedding for the question
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = question
    )

    question_embedding = response.data[0].embedding

    #Search the data in pinecone
    results = index.query(
        vector = question_embedding,
        top_k = 3,
        include_metadata = True
    )
    print("Results :", results)

    documents = []

    for match in results["matches"]:
        document = match["metadata"]["text"]
        documents.append(document)

    print("Documents :", documents)

    #Combine documents into context
    context = "\n\n".join(documents)

    print("Context:" , context)

    #Create RAG prompt

    prompt = f"""
    Answer the question using only the context provided below
    
    Context : {context}
    
    Question : {question}
"""

    response = client.responses.create(
        model = "gpt-6-astra",
        input = prompt
    )

    return response.output_text


#Simple test to run
if __name__=="__main__":
    question = input("Ask a question:")
    answer = ask_question(question)

    print(answer)