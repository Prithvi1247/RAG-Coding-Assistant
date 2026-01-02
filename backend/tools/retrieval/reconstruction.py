from langchain_core.documents import Document # type: ignore
from .search import retrieve_chunks

# returns a combined version of a split function
def symbol_chunks(chunks:list[Document], symbol:str)-> list[Document]:

    func = []
    for chunk in chunks:
        if chunk.metadata['symbol'] == symbol:
            func.append(chunk)
    # sort func by split id
    if func[0].metadata['is_split']:
        func = sorted(func, key=lambda part: part.metadata['split_id'])

    return func
# returns a document list to a final string
def documentlist_to_codestr(chunks:list[Document])->str:
    content = []
    for chunk in chunks:
        content.append(chunk.page_content+"\n")
    
    return "".join(content)

def build_object(chunk: Document, parts: list[Document] | None = None) -> dict:
    if parts:
        return{
            'filename' : chunk.metadata['filename'],
            'chunk_type' : chunk.metadata['chunk_type'],
            'filepath' : chunk.metadata['filepath'],
            "symbol" : chunk.metadata['symbol'],
            'start_line' : chunk.metadata['start_line'],
            'end_line' : chunk.metadata['end_line'],
            'language' : chunk.metadata['language'],
            'code' : documentlist_to_codestr(parts)
        }
    else:
        return{
            'chunk_type' : chunk.metadata['chunk_type'],
            'filename' : chunk.metadata['filename'],
            'filepath' : chunk.metadata['filepath'],
            "symbol" : chunk.metadata['symbol'],
            'start_line' : chunk.metadata['start_line'],
            'end_line' : chunk.metadata['end_line'],
            'language' : chunk.metadata['language'],
            'code' : chunk.page_content
        }

def chunks_to_content(code_chunks: list[Document]) -> list[dict]:
    net_content=[]
    processed = set()
    
    for chunk in code_chunks:
        if chunk.metadata.get("is_split", False) and (chunk.metadata['symbol'] not in processed):
            parts = symbol_chunks(code_chunks, chunk.metadata["symbol"])
            object_ = build_object(chunk, parts)
            net_content.append(object_) 
            processed.add(chunk.metadata['symbol'])

        elif not chunk.metadata.get("is_split", False):
            object_= build_object(chunk)
            net_content.append(object_)
            processed.add(chunk.metadata['symbol'])

    return net_content

def attach_class_headers(code_objs: list[dict])-> list[dict]:
        
    class_headers = []
    
    for obj in code_objs:
        if obj['chunk_type'] == 'class_header':
            class_headers.append(obj)
    
    
    for method in code_objs:
        if method['chunk_type'] == 'class_method':
            class_name = method['symbol'].split('.')[0]
            # check in class headers for symbol
            got_header = False
            for class_obj in class_headers:
                if class_obj['symbol'] == class_name : 
                    method_content= method['code']
                    method['code'] = class_obj['code']+ '\n\n' +method_content
                    got_header = True
                    break
                        
                # force retrieve headers from db
            if not got_header:
                
                results = retrieve_chunks(class_name, k=3)
                results = chunks_to_content(results)
                for class_obj in results : 
                    if class_obj['symbol']== class_name:
                        method_content= method['code']
                        method['code'] = class_obj['code']+ '\n\n' +method_content
                        break
    
    return code_objs