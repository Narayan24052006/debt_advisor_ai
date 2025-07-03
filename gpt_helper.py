import ollama

def call_llm(prompt: str, model: str = "tinyllama") -> str:
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    
    return response['message']['content']
    