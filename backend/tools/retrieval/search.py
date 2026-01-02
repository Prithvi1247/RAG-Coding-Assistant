from langchain_core.documents import Document # type: ignore
from qdrant_client import QdrantClient  # type: ignore
from langchain_qdrant import QdrantVectorStore # type: ignore
from langchain_core.documents import Document # type: ignore
from tools.core.config import COLLECTION_NAME, QDRANT_URL, EMBED_MODEL_NAME
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore


def retrieve_chunks(query:str, k:int) -> list[Document]:
    search_Results= vector_db.similarity_search(query=query, k = k)
    return search_Results


client = QdrantClient("http://localhost:6333")

embed_model = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL_NAME,
    model_kwargs={"trust_remote_code": True}
)

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=QDRANT_URL,
    embedding=embed_model
    )
