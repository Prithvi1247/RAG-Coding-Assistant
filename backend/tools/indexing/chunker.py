from tools.core.config import TOKEN_LIMIT, OVERLAP
from tools.indexing.classes.blocks import CodeFile,CodeChunk
import ast


def split_chunk_text(chunk_text:str, max_size:int = TOKEN_LIMIT, overlap:int = OVERLAP) -> list[str]:

    tokens = chunk_text.split()
    token_length = len(tokens)

    if token_length <= max_size:
        return [chunk_text]
    else:
        chunk_text_list = []
        i= 0 
        while i < token_length:
            window= tokens[i: i+max_size]
            if not window:
                break
            i += max_size - overlap
            window_text =" ".join(window)
            chunk_text_list.append(window_text)
        
    return chunk_text_list

def ast_parse(block: CodeFile) -> list[CodeChunk]:

    code_chunks=[]
    functions=[]
    async_functions=[]
    classes=[]
    class_methods=[]

    occupied_lines = set()
    # parse ast safely
    try:
        tree = ast.parse(block.filetext)
    except SyntaxError:
        print(f"skipped parsing {block.filename}")
        return []
    

    # walk ast , collect functions , async functions and class nodes
    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            print("Found a function:", node.name)
            functions.append(node)
            
        if isinstance(node, ast.AsyncFunctionDef):
            print("Found an async function:", node.name)
            async_functions.append(node)

        if isinstance(node, ast.ClassDef):
            print("Found a class:", node.name)
            classes.append(node)
    
    for class_node in classes:
        for node in class_node.body : 

            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                class_methods.append((class_node, node))
                print(f"found class method {class_node.name}.{node.name}")

    # extract function chunks

    file_lines = block.filetext.splitlines()

    # extract classes header chunks
    for class_node in classes:
        # include class header and decorators
        class_start_lineno = class_node.lineno
        if class_node.decorator_list:
            decorator_count = len(class_node.decorator_list)
            class_start_lineno = max(class_node.lineno - decorator_count, 1)

        class_end_lineno = class_start_lineno
       
        # include docstrings if exists
            # python stores docstrings as Expr(Constant("text"))
        if class_node.body:
            first = class_node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                docstring_node = first.value
                class_end_lineno = docstring_node.end_lineno
        
        full_text = "\n".join(file_lines[class_start_lineno-1 : class_end_lineno])
        occupied_lines.update(range(class_start_lineno , class_end_lineno+1) )

        split_parts = split_chunk_text(full_text)
        if len(split_parts) == 1 :

            class_code_chunk = CodeChunk(
                                            chunk_text= split_parts[0],
                                            symbol=class_node.name,
                                            chunk_type="class_header",
                                            is_split='False',
                                            filename=block.filename,
                                            filepath=block.filepath,
                                            start_line=class_start_lineno,
                                            end_line=class_end_lineno,
                                            
                                            language=block.language,
                                           

            )

            code_chunks.append(class_code_chunk)
        else :
            i=1
            for part_text in split_parts:
                class_code_chunk = CodeChunk(
                    chunk_text=part_text,
                    symbol=class_node.name,
                    chunk_type="class_header",
                    is_split='True',
                    filename = block.filename,
                    filepath = block.filepath,
                    start_line=class_start_lineno,
                    end_line=class_end_lineno,
                    split_id=str(i),
                    language=block.language
                    
                )
                i+=1
                code_chunks.append(class_code_chunk)

    # Extract method chunks inside each class
    

    for class_method in class_methods:
        # (class_node, node)
        class_node = class_method[0]
        function_node = class_method[1]

        classname = class_node.name

        start_line = function_node.lineno
        end_line = function_node.end_lineno
        
        full_text = "\n".join(file_lines[start_line-1: end_line])
        occupied_lines.update(range(start_line, end_line + 1))
        split_parts = split_chunk_text(full_text)
        i=1
        if len(split_parts) == 1 : 
            method_code_chunk = CodeChunk(
                                    chunk_text=split_parts[0],
                                    symbol= f"{classname}.{function_node.name}",
                                    chunk_type="class_method",
                                    is_split= 'False',
                                    filename=block.filename,
                                    filepath= block.filepath,
                                    start_line= start_line,
                                    end_line= end_line,
                                    
                                    language=block.language
                                    
            )

            code_chunks.append(method_code_chunk)
        
        else:
            for part_text in split_parts:
                method_code_chunk = CodeChunk(
                                    chunk_text=part_text,
                                    symbol= f"{classname}.{function_node.name}",
                                    chunk_type="class_method",
                                    is_split= 'True',
                                    filename=block.filename,
                                    filepath= block.filepath,
                                    start_line= start_line,
                                    end_line= end_line,
                                    split_id=str(i),
                                    language=block.language
                                    
                )
                code_chunks.append(method_code_chunk)
                i+= 1
    class_method_lines = set()

    for class_node, function_node in class_methods:
        class_method_lines.update(range(function_node.lineno, function_node.end_lineno + 1))

    for function_node in functions:

        if function_node.lineno not in class_method_lines:
            function_start_line = function_node.lineno # storing into codechunk shd have 1-indexed numbering
            function_end_line = function_node.end_lineno

            # lists are 0-indexed
            full_text = '\n'.join( file_lines[function_start_line-1 : function_end_line] )
            occupied_lines.update(range(function_start_line , function_end_line+1) )
            split_chunks = split_chunk_text(chunk_text= full_text)
            
            if len(split_chunks) == 1:
                function_chunk= CodeChunk(
                    chunk_text= full_text, 
                    symbol= function_node.name, 
                    chunk_type="function",
                    is_split= 'False', 
                    filename= block.filename, 
                    filepath= block.filepath, 
                    start_line= str(function_start_line), 
                    end_line= str(function_end_line),
                    language=str(block.language)
                    
                    )
                code_chunks.append(function_chunk)
            else:
        
                i=1
                for part_text in split_chunks:

                    function_chunk = CodeChunk(chunk_text = part_text,
                                    symbol= function_node.name,
                                    chunk_type="function",
                                    is_split= 'True',
                                    filename= block.filename,
                                    filepath= block.filepath, 
                                    start_line= str(function_start_line), 
                                    end_line= str(function_end_line),
                                    split_id=str(i),
                                    language=block.language
                                    
                                    )

                    code_chunks.append(function_chunk)
                    i+=1



    # extract async-function chunks
    for asyncfunction_node in async_functions:
        if asyncfunction_node.lineno not in class_method_lines:
            asyncfunction_start_line = asyncfunction_node.lineno # storing into codechunk shd have 1-indexed numbering

            asyncfunction_end_line = asyncfunction_node.end_lineno
            # lists are 0-indexed

            full_text = '\n'.join( file_lines[asyncfunction_start_line-1 : asyncfunction_end_line] )
            occupied_lines.update(range(asyncfunction_start_line , asyncfunction_end_line+1) )
            split_chunks = split_chunk_text(chunk_text= full_text)
            
            if len(split_chunks) == 1:
                asyncfunction_chunk= CodeChunk(
                    chunk_text= full_text, 
                    symbol= asyncfunction_node.name, 
                    chunk_type="async_function",
                    is_split= 'False', 
                    filename= block.filename, 
                    filepath= block.filepath, 
                    start_line= str(asyncfunction_start_line), 
                    end_line= str(asyncfunction_end_line),
                    language=block.language
                    
                    )
                code_chunks.append(asyncfunction_chunk)
            else:
                i=1
                for part_text in split_chunks:

                    asyncfunction_chunk = CodeChunk(chunk_text = part_text,
                                    symbol= asyncfunction_node.name,
                                    chunk_type="async_function",
                                    is_split= 'True',
                                    filename= block.filename,
                                    filepath= block.filepath, 
                                    start_line= str(asyncfunction_start_line), 
                                    end_line= str(asyncfunction_end_line),
                                    split_id=str(i),
                                    language=block.language
                                )

                    code_chunks.append(asyncfunction_chunk)
                    i+=1
            
    
    # module level code chunks

    module_lines=[]

    start_line = 0 
    for lineno,line in enumerate(file_lines,1):
        if lineno not in occupied_lines:
            module_lines.append(line)
    for i in range(1, len(file_lines)+1):
        if i not in occupied_lines:
            start_line = i
            break
    for i in range(len(file_lines),0, -1 ):
        if i not in occupied_lines:
            end_line = i
            break
    
    
    full_text = '\n'.join( module_lines ).strip()
    if full_text:
        
        split_parts = split_chunk_text(full_text)

        i= 1 
        if len(split_parts) == 1 :
            global_code_chunk = CodeChunk(
                                        chunk_text=split_parts[0],
                                        symbol= f"{block.filename}.__module__",
                                        chunk_type="module",
                                        is_split= "False",
                                        filename=block.filename,
                                        filepath= block.filepath,
                                        start_line= start_line,
                                        end_line= end_line,
                                        split_id='-1',
                                        language=block.language
                                        
                )

            code_chunks.append(global_code_chunk)
        else:
            for part_text in split_parts:
                    global_code_chunk = CodeChunk(
                                        chunk_text=part_text,
                                        symbol= f"{block.filename}.__module__",
                                        chunk_type="module",
                                        is_split= 'True',
                                        filename=block.filename,
                                        filepath= block.filepath,
                                        start_line= start_line,
                                        end_line= end_line,
                                        split_id=str(i),
                                        language=block.language
                                        
                    )
                    code_chunks.append(global_code_chunk)
                    i+= 1
    # return chunks
    print(f"returning chunks for block {block.filename}")
    return code_chunks
