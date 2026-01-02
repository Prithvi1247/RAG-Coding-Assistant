from openai import OpenAI # type: ignore
from tools.core.config import GOOGLE_API_KEY

client_llm = OpenAI(
    api_key=GOOGLE_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def llm_response(user_query:str, context:str)->str:
    
    SYSTEM_PROMPT = f"""
        You are a highly reliable codebase assistant.

        Here are the most relevant code chunks from the repository:

        {context}

        When answering:
        - USE the code above
        - Be precise and grounded in this code
        - If code is missing, say so
        - If you improve code, return COMPLETE updated snippet
        """
        
    response = client_llm.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        temperature = 0.2
    )

    return f"{response.choices[0].message.content}"
