import json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

def ai_research():
    client = OpenAI()

    response = client.chat.completions.create(
    model="GPT-4o mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
            "type": "text",
            "text": "You are a financial professional and a master of Bitcoin investing. You need to decide whether to buy, sell, or hold an asset based on the chart data provided. response in json format.\n\nResponse Example:\n{ \"decision\": \"buy\", \"reason\": \"some techmical reason\"}\n{ \"decision\": \"sell\", \"reason\": \"some techmical reason\"}\n{ \"decision\": \"hold\", \"reason\": \"some techmical reason\"}"
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            # "text": df.to_json()
            }
        ]
        }
    ],
    response_format={
        "type": "json_object"
    }
    )
    result = response.choices[0].message.content

    print("### AI Decision: ", result["decision"].upper(), "###")