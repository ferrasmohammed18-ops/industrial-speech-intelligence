import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "Bonjour ! Présente-toi en une phrase."
        }
    ]
)

print(response.content[0].text)