import openai
import os

def generate_response(prompt, model="gpt-3.5-turbo"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def main():
    print("AutoPromptX – GPT Prompt Generator")
    while True:
        prompt = input("Enter your prompt (or type 'exit'): ")
        if prompt.lower() == 'exit':
            break
        response = generate_response(prompt)
        print("\nGenerated Response:\n", response)
        print("-" * 50)

if __name__ == "__main__":
    main()
