from .chunker import ast_parse
from .loader import load_codebase
from tools.indexing.classes.blocks import CodeChunk
from .embeddings import build_metadata, embed_model
import uuid
from langchain_core.documents import Document # type: ignore
from tools.core.config import COLLECTION_NAME, QDRANT_URL
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.models import Distance, VectorParams # type: ignore
from langchain_qdrant import QdrantVectorStore # type: ignore

def chunks_to_metadata(codechunks: list[CodeChunk])-> list[dict]:
    metadatas =[]
    for chunk in codechunks:
        meta = build_metadata(chunk)
        metadatas.append(meta)

    return metadatas

def store_chunk(chunks: list[CodeChunk]):
    documents = []
    ids = []
    
    for chunk in chunks:
        # 1. Build the metadata
        meta = build_metadata(chunk)
        
        # 2. SAFETY FILTER: Loop through and fix any None values
        clean_meta = {}
        for key, value in meta.items():
            if value is None:
                print(f"⚠️ Warning: Found None in field '{key}' for symbol '{chunk.symbol}'. Defaulting to empty string.")
                clean_meta[key] = ""
            else:
                clean_meta[key] = str(value) # Force string conversion
        
        # 3. Create the document with the cleaned metadata
        documents.append(Document(
            page_content=chunk.chunk_text, 
            metadata=clean_meta
        ))
        ids.append(str(uuid.uuid4()))
        
    # 4. Add to Qdrant
    if documents:
        vector_db.add_documents(documents=documents, ids=ids)
        print(f"Successfully added {len(documents)} chunks to Qdrant.")

def store_codebase(path: str ):
    # Deleting old code base stored.


    codefiles = load_codebase(path)
    for file in codefiles: 
        code_chunks = ast_parse(file)
        
        store_chunk(code_chunks)

client = QdrantClient(QDRANT_URL)

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