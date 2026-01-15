from tools.core.config import PRIORITY, TOKEN_BUDGET
from .reconstruction import chunks_to_content, attach_class_headers
from langchain_core.documents import Document # type: ignore

def score(chunk:dict):
    return PRIORITY.get(chunk['chunk_type'], 10)

def fit_budget(objs: list[dict], max_tokens:int = TOKEN_BUDGET) -> list[dict]:
    final = [] 
    used = 0
    
    for c in objs:
        t = len(c['code'].split())
        if used + t > max_tokens:
            break
        final.append(c)
        used += t
    
    return final

def format_content(objs:list[dict]) ->str:
    final = []

    for obj in objs : 
        final.append(
            f'''
                filename : {obj['filename']}\n
                filepath : {obj['filepath']}\n
                symbol : {obj['symbol']}\n
                start_line: {obj['start_line']}\t end_line: {obj['end_line']}\n
                language : {obj['language']}\n\n
                {obj['code']}
            '''
        )
    return '\n\n -------- \n'.join(final)

def context_structure(results:list[Document], repo_id:str)->str:

    content = chunks_to_content(results)
    print("Converted payload to string ✅")

    final_content = attach_class_headers(content, repo_id)
    print("Attached headers to class methods ✅")

    final_content = sorted(final_content, key= score, reverse=True)
    print("Sorted the content ✅")

    final_content = fit_budget(final_content)
    print("Content in right size ✅")

    final_string = format_content(final_content)
    print("Content Formated ✅")
    return final_string