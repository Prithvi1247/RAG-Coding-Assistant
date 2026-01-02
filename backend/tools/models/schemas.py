from pydantic import BaseModel # type: ignore

class Query(BaseModel):
    question: str
