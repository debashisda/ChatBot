from openai import OpenAI

endpoint = ""
deployment_name = "gpt-4o-default"
api_key = "<API_KEY>"

client = OpenAI(base_url=endpoint, api_key=api_key)

conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant.",
    }
]

def get_response(message):
    conversation_history.append({"role": "user", "content": message})
    try:
        completion = client.chat.completions.create(model=deployment_name,messages=conversation_history,)
        reply = completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        conversation_history.pop()
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break
        print(f"\nAI: {get_response(user_input)}\n")
