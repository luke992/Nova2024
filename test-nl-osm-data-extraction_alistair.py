from openai import OpenAI
import openai
import json
import requests

TEAM_API_KEY = "sk-t294DQLct5JulSvcXBgTAA"
PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com"

openai.api_key = 'sk-t294DQLct5JulSvcXBgTAA'

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"


def get_overpass_api_query(user_query):
    """
    Examples of chat completions from the proxy
    """
    client = OpenAI(
        api_key=TEAM_API_KEY, # set this!!!
        base_url=PROXY_ENDPOINT # and this!!!
    )

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages = [
            {
                "role": "system",
                "content": "You are an expert OpenStreetMap API assistant. Convert the user's natural language query into a valid Overpass API query that can be used to answer the question. You should only respond with the Overpass query itself, not any additional text. You should not output any Python code, just the Overpass query. You should never output any newlines or line breaks in the response.",
            },
            {
                "role": "user",
                "content": f"{user_query}",
            }
        ],
        stream=False
    )

    print("Response")
    print(response.choices[0].message.content)

    return response.choices[0].message.content

def query_overpass(query):
    payload = {"data": query}
    response = requests.post(OVERPASS_API_URL, data=payload)
    return response.json()


def main():
    user_input = input("Describe the location or detail you want to find: ")

    overpass_query = get_overpass_api_query(user_input)
    print(f"Generated Overpass Query: {overpass_query}")

    if "```" in overpass_query:
        overpass_query = overpass_query.replace("```", "")

    response = query_overpass(overpass_query)

    print("Response")
    print(response)

if __name__ == "__main__":
    main()