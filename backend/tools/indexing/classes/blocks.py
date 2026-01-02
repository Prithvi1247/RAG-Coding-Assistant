class CodeFile: 
   
    def __init__(self, filename, extension, filepath, filetext, language= "unknown"):
        self.filename = filename
        self.extension = extension
        self.filepath = filepath
        self.filetext = filetext
        self.language = language

    filename: str
    extension: str
    filepath: str
    filetext: str
    language: str 

class CodeChunk:

    def __init__(self, chunk_text, symbol,chunk_type, is_split, filename,filepath,start_line, end_line,split_id= '-1',language= 'unknown'):
        self.chunk_text = chunk_text
        self.symbol = symbol
        self.chunk_type= chunk_type
        self.is_split = is_split
        self.filename = filename
        self.filepath = filepath
        self.start_line = start_line
        self.end_line = end_line
        self.split_id = split_id
        self.language = language

    chunk_type:str
    chunk_text:str
    symbol: str
    is_split: str  |bool          # True if chunk was split
    split_id: str |int      # 1, 2, 3... corresponding to order
    filename:str
    filepath:str
    start_line:str|int
    end_line:str|int
    language:str 