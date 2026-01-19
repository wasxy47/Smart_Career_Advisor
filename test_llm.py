from src.models import get_llm

print("Testing Gemini 2.0 Flash...")
try:
    llm = get_llm()
    response = llm.invoke("Hello, are you working?")
    print("\nSuccess! Response:")
    print(response.content)
except Exception as e:
    print("\nError:")
    print(e)