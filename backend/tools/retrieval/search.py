from langchain_core.documents import Document # type: ignore
from qdrant_client import QdrantClient  # type: ignore
from langchain_qdrant import QdrantVectorStore # type: ignore
from langchain_core.documents import Document # type: ignore
from tools.core.config import COLLECTION_NAME, QDRANT_CLUSTER_ENDPOINT, EMBED_MODEL_NAME, QDRANT_API_KEY
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore


def retrieve_chunks(query:str, k:int, repo_id : str) -> list[Document]:
    search_Results= vector_db.similarity_search(query=query, k = k, filter={
            "repo_id": repo_id
        }
    )
    return search_Results


client = QdrantClient(url= QDRANT_CLUSTER_ENDPOINT, api_key= QDRANT_API_KEY)

embed_model = HuggingFaceEmbeddings(
    model_name=EMBED_MODEL_NAME,
    model_kwargs={"trust_remote_code": True}
)

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    url=QDRANT_CLUSTER_ENDPOINT,
    embedding=embed_model
    )
