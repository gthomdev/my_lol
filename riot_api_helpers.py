from dotenv import load_dotenv
import json
import os
import requests
from requests.exceptions import RequestException

load_dotenv()

def get_summoner_by_name(summoner_name):
    """[Requests a summoner DTO from the Riot API for a given summoner name]

    Args:
        summoner_name ([string]): [The summoner name of the user being searched for. This is the name
        that they will use in games.]

    Returns:
        [dictionary]: [Returns the content of the response. Keys: id, accountId, puuid, name, profileIconId, revisionDate
        summonerLevel]
    """
    api_key = os.getenv("API_KEY")

    # Arrange headers
    headers_dict = {"X-Riot-Token":api_key}

    # Get response from Summoner API, check for errors
    try:
        response = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}", headers=headers_dict)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        response_content = response.content
        json_response_content = json.loads(response_content.decode('utf-8'))
        return {
            "id": json_response_content["id"],
            "account_id": json_response_content["accountId"],
            "puuid": json_response_content["puuid"],
            "name": json_response_content["name"],
            "revision_date": json_response_content["revisionDate"],
            "summoner_level": json_response_content["summonerLevel"]
        }
    except (KeyError, TypeError, ValueError):
        return None