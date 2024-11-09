from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from openai import OpenAI
import openai
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import json

TEAM_API_KEY = "sk-t294DQLct5JulSvcXBgTAA"
PROXY_ENDPOINT = "https://nova-litellm-proxy.onrender.com"

# Initialize OSM and OpenAI API
osm_api = Api()
openai.api_key = 'sk-t294DQLct5JulSvcXBgTAA'


# def interpret_input(user_input):
#     """Use OpenAI to interpret the natural language and suggest an OSM query."""
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=f"Convert the following natural language description into an OpenStreetMap-compatible query:\n\n'{user_input}'\n\nFormat it as 'key=value' and suggest appropriate tags if relevant.",
#         max_tokens=100
#     )
#     return response.choices[0].text.strip()

def interpret_input(user_input):
    """
    Examples of chat completions from the proxy
    """
    client = OpenAI(
        api_key=TEAM_API_KEY, # set this!!!
        base_url=PROXY_ENDPOINT # and this!!!
    )

    response_string = ""

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages = [
            {
                "role": "user",
                "content": f"Convert the following natural language description into an OpenStreetMap-compatible query. The query should be written as a Python call to overpassQueryBuilder:\n\n'{user_input}'\n\nType out a json object containing the necessary arguments, such as areas, elementType, and selector. Do not type any extra text.",
            }
        ],
        stream=False
    )

    # for chunk in response:
    #     if not chunk.choices[0].delta.content is None:
    #         print(chunk.choices[0].delta.content)
    #         response_string += chunk.choices[0].delta.content

    print("Response")
    print(response.choices[0].message.content)

    return response.choices[0].message.content

def query_osm(query):
    """Run a query against the OSM database based on interpreted input."""
    try:
        # For example, query: 'amenity=school' or 'tourism=hotel' (based on user input)
        osm_data = osm_api.query(f'[out:json];node[{query}](around:10000,48.8588443,2.2943506);out;')
        return osm_data.toJSON()
    except Exception as e:
        return {"error": str(e)}


def main():
    user_input = input("Describe the location or detail you want to find: ")

    osm_query = interpret_input(user_input)

    if osm_query.endswith('```'):
        osm_query = osm_query[:-3]

    if osm_query.startswith('```json'):
        osm_query = osm_query[7:]

    print(f"Generated OSM Query: {osm_query}")

    osm_json = json.loads(osm_query)
    print("Area: " + osm_json["area"])

    overpass = Overpass()
    osm_query = overpassQueryBuilder(area=Nominatim().query(osm_json["area"]).areaId(), elementType=osm_json["elementType"], selector=osm_json["selector"])
    osm_results = overpass.query(osm_query)

    print("Number of results found: " + str(osm_results.countElements()))

if __name__ == "__main__":
    main()