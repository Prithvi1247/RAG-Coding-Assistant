from tools.core.config import ALLOWED_EXTENSIONS
import os
from tools.indexing.classes.blocks import CodeFile


def load_codebase(path:str) -> list[CodeFile]:

    code_files = []
    allowed_extensions = ALLOWED_EXTENSIONS
    IGNORES = ("__MACOSX", ".DS_Store")
    # Start traversing from the current working directory
    for dirpath, dirnames, filenames in os.walk(path):
        
        print("PWD ", dirpath+'/')
        if any(x in path for x in IGNORES):
            continue
        if os.path.basename(path).startswith("._"):
            continue

        for file in filenames:
            # Construct the full path for each file
            full_file_path = os.path.join(dirpath, file)
            file_name, extension = os.path.splitext(file)

            extension = extension.lower()
            if extension in allowed_extensions:
                with open(full_file_path, 'r', encoding="utf-8", errors='ignore') as f:
                    file_text= f.read()
                language = 'unknown'
                if extension == '.py': 
                    language = 'python'
                cFile = CodeFile(
                            filename=file_name,
                            extension=extension,
                            filepath=full_file_path,
                            filetext=file_text,
                            language=language
                        )
                code_files.append(cFile)

    return code_files
    
