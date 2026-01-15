from fastapi import FastAPI, UploadFile, File
import uuid, os, zipfile
from tools.indexing.indexer import store_codebase
from tools.retrieval.search import retrieve_chunks
from tools.retrieval.context_builder import context_structure
from tools.llm.answerer import llm_response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tools.core.config import COLLECTION_NAME, QDRANT_CLUSTER_ENDPOINT,QDRANT_API_KEY



from tools.indexing.embeddings import  embed_model

from qdrant_client import QdrantClient # type: ignore
from qdrant_client.models import Distance, VectorParams # type: ignore
from langchain_qdrant import QdrantVectorStore # type: ignore
UPLOAD_DIR = "uploads"
REPO_DIR = "repos"



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # or ["http://localhost:5174"]
    allow_credentials=True,
    allow_methods=["*"],          # <-- IMPORTANT
    allow_headers=["*"],
)

client = QdrantClient(url = QDRANT_CLUSTER_ENDPOINT, api_key = QDRANT_API_KEY)

client.delete_collection(collection_name=COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE
    ),
)

vector_db = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embed_model,
    content_payload_key="page_content",   # <- THIS IS IMPORTANT
)

@app.post("/upload")
async def upload_codebase(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        return {"error": "Only .zip files allowed"}

    session_id = str(uuid.uuid4())

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(REPO_DIR, exist_ok=True)

    zip_path = f"{UPLOAD_DIR}/{session_id}.zip"
    repo_path = f"{REPO_DIR}/{session_id}"

    with open(zip_path, "wb") as buffer:
        buffer.write(await file.read())

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(repo_path)

    # AST + Qdrant embedding pipeline
    store_codebase(repo_path)

    return {"message": "Indexed successfully", "session_id": session_id}

class Query(BaseModel):
    question: str
@app.post("/ask")
def ask_code_assistant(req: Query):
    results = retrieve_chunks(req.question, k=6)
    context = context_structure(results)
    answer = llm_response(req.question, context)

    return {
        "answer": answer,
        "context": context
    }