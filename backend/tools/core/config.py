import os
from dotenv import load_dotenv # type: ignore
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

QDRANT_URL=os.getenv("QDRANT_URL")
COLLECTION_NAME = "codebase_chunks"

LLM_PROVIDER = 'google'

TOKEN_LIMIT = 512
OVERLAP = int(0.25*TOKEN_LIMIT)

EMBED_MODEL_NAME = 'nomic-ai/nomic-embed-text-v1.5'

TOKEN_BUDGET = 6000 #
ALLOWED_EXTENSIONS= ['.py','.yaml','.md','.txt','.yml','.json','.csv']

PRIORITY = {
 "class_method": 100,
 "function": 90,
 "class_header": 80,
 "async_function": 80,
 "module": 50
}