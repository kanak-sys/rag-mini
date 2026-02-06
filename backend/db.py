import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def insert_doc(content, embedding):
    supabase.table("documents").insert({
        "content": content,
        "embedding": embedding
    }).execute()

def search_docs(query_embedding, k=3):
    res = supabase.rpc("match_documents", {
        "query_embedding": query_embedding,
        "match_count": k
    }).execute()
    return res.data
