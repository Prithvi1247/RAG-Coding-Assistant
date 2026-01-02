from tools.indexing.classes.blocks import CodeChunk
from langchain_huggingface import HuggingFaceEmbeddings # type: ignore
from tools.core.config import EMBED_MODEL_NAME

def build_metadata(chunk: CodeChunk) -> dict:
    return {
        # Wrap everything in str() and handle None explicitly
        "symbol": str(chunk.symbol) if chunk.symbol is not None else "",
        'filename': str(chunk.filename) if chunk.filename is not None else "",
        'filepath': str(chunk.filepath) if chunk.filepath is not None else "",
        
        # Ensure line numbers are strings
        'start_line': int(chunk.start_line) if chunk.start_line is not None else "0",
        'end_line': int(chunk.end_line) if chunk.end_line is not None else "0",
        
        'is_split': bool(chunk.is_split) if chunk.is_split is not None else "False",
        'language': str(chunk.language) if chunk.language is not None else "unknown",
        
        # The critical fix: If split_id is None, force it to "-1"
        'split_id': int(chunk.split_id) if chunk.split_id is not None else "-1",
        
        'chunk_type': str(chunk.chunk_type) if chunk.chunk_type is not None else "unknown"
    }
    



# Embedding ;)
def embed_text(text: str):
    return embed_model.embed_query(text)

def chunks_to_metadata(codechunks: list[CodeChunk])-> list[dict]:
    metadatas =[]
    for chunk in codechunks:
        meta = build_metadata(chunk)
        metadatas.append(meta)

    return metadatas

embed_model = HuggingFaceEmbeddings(
    model_name= EMBED_MODEL_NAME,
    model_kwargs= {"trust_remote_code": True}
)

