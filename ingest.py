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

#Create the index if it doesn't exist
if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension = dimensions,
        metric = "cosine",
        spec = ServerlessSpec(
            cloud = "aws",
            region = "us-east-1"
        )
    )

#Connect to index
index = pc.Index(index_name)

#Read the document
with open("documents/company.txt","r",encoding = "utf-8") as file:
    document = file.read()

    #Split document into chunks
    chunks = document.split("\n\n")

    #Generate embeddings and store them
    vectors = []

    for index_number, chunk in enumerate(chunks):
        response = client.embeddings.create(
            model = "text-embedding-3-small",
            input = chunk
        )
        print("Response :: ", response)
        embedding = response.data[0].embedding

        #Create Pinecone vector

        vectors.append({
            "id" : f"chunk-{index_number}",
            "values" : embedding,
            "metadata" : {
                "text" : chunk
            }
        })

        #Upload vectors to pinecone

        index.upsert(vectors = vectors)


print("Document successfully stored in pinecone...")