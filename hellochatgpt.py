import sys
from openai import OpenAI

def chat_gpt(apiKey, prompt):
    client=OpenAI(api_key=apiKey)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
key=sys.argv[1]
print (chat_gpt(key, "Hello world!"))