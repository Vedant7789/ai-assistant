import os 
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

EMBED_MODEL=os.getenv("EMBED_MODEL")

def get_embedding(text):
    response=client.embeddings.create(
        model=EMBED_MODEL,
        input=text

    )
    return response.data[0].embedding

chunks={
    "c0":"Hiring Process - Joining New joiners receive a laptop within one day of joining. HR sends the onboarding checklist two days before the joining date.",
    "c1":"Maternity leave is 26 weeks of paid leave. Paternity leave is 10 working days and must be taken within 3 months of the child's birth.",


}

ids=list(chunks.keys())
documents=list(chunks.values())

embeddings=[]
for s in documents:
    embedding=get_embedding(s)
    embeddings.append(embedding)

chroma=chromadb.PersistentClient(path="./chromadbStorage")

tech=chroma.get_or_create_collection(
    name="techno",
    configuration={
        "hnsw":{
            "space":"cosine",
        }
        
    }

)
tech.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
)

query="new joiners receives what?"
query_embeddings=get_embedding(query)

results=tech.query(
    query_embeddings=[query_embeddings],
    n_results=1
)

print(results["documents"][0])






