def llm (prompt:str):
    return {
        "content" : "Hello how are you ?",
        "role" : "assistant"
    }

response_dictionary = llm(prompt = "Hi")

print(response_dictionary["content"])
