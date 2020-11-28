from dotenv import load_dotenv
import json
import os
import requests
from requests.exceptions import RequestException

load_dotenv()

def get_summoner_by_name(summoner_name):
    """Requests a summonerDto from the Riot API for a given summoner name

    Args:
        summoner_name ([string]): [The summoner name of the user being searched for. This is the name
        that they will use in games.]

    Returns:
        [dictionary]: Returns the content of the response. Keys: id, accountId, puuid, name, profileIconId, revisionDate
        summonerLevel
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

def get_matches_for_account(account_id, champion=None, queue=None, season=None, endTime=None, beginTime=None, endIndex=None, beginIndex=None):
    """Requests a MatchlistDto from the Riot Match API. This contains a series of MatchReferenceDtos, each containing:
    gameId: long
    role: string
    season: int
    platformId: string
    champion: int
    queue: int
    lane: string
    timestamp: long
    
    Args:
        account_id (string): Encrypted accountId. This is returned in the summonerDto from the get_summoner_by_name function.
        champion (int, optional): Champion key. The value that corresponds to each champion can be found in champions.json. Defaults to None.
        queue (int, optional): Queue key. The value that corresponds to each queue can be found in queues.json.  Defaults to None.
        season (int, optional): Corresponds to the season. Riot's API documentation specifies this as deprecated, so do not rely on it. Defaults to None.
        endTime (long, optional): The end time to use for filtering the matchlist specified as epoch milliseconds. If beginTime is specified but not endTime, endTime defaults to the current timestamp in milliseconds. Defaults to None.
        beginTime (long, optional): The begin time to use for filtering the matchlist specified as epoch milliseconds. If beginTime is specified but not endTime, endTime defaults to the current timestamp in milliseconds. Defaults to None.
        endIndex (int, optional): The end index to use for filtering the matchlist. If beginIndex is specified but not endIndex, endIndex defaults to beginIndex+100. The maximum range allowed is 100. Defaults to None.
        beginIndex (int, optional): The begin index to use for filtering the matchlist. If beginIndex is specified but not endIndex, endIndex defaults to beginIndex+100. The maximum range allowed is 100. Defaults to None.

    Returns:
        [dict]: Returns a dictionary containing a list of match references, each denoting a game played. This is followed by values for the keys: startIndex, endIndex, totalGames.
    """
    api_key = os.getenv("API_KEY")

    # Arrange headers
    headers_dict = {"X-Riot-Token":api_key}

    # Get response from Match API, check for errors
    try:
        # Update parameters dictionary with optional parameters from call
        parameters={
            "champion": champion,
            "queue": queue,
            "season": season,
            "endTime": endTime,
            "beginTime": beginTime,
            "endIndex": endIndex,
            "beginIndex": beginIndex    
        }

        # Make request call
        response = requests.get(f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}", headers=headers_dict, params=parameters)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse result
    try:
        response_content = response.content
        json_response_content = json.loads(response_content.decode('utf-8'))
        return json_response_content
    except (KeyError, TypeError, ValueError):
        return None

def get_match_for_match_id(match_id):
    """Requests a matchDto for a match ID. Each contains:
    NAME	                DATA TYPE	                            DESCRIPTION
    gameId	                long	
    participantIdentities	List[ParticipantIdentityDto]	        Participant identity information. Participant identity information is purposefully excluded for custom games.   
    queueId	                int	                                    Please refer to the Game Constants documentation.
    gameType	            string	                                Please refer to the Game Constants documentation.
    gameDuration	        long	                                Match duration in seconds.
    teams	                List[TeamStatsDto]	                    Team information.
    platformId	            string	                                Platform where the match was played.
    gameCreation	        long	                                Designates the timestamp when champion select ended and the loading screen appeared, NOT when the game timer was at 0:00.
    seasonId	            int	                                    Please refer to the Game Constants documentation.
    gameVersion	            string	                                The major.minor version typically indicates the patch the match was played on.
    mapId	                int	                                    Please refer to the Game Constants documentation.
    gameMode	            string	                                Please refer to the Game Constants documentation.
    participants	        List[ParticipantDto]	                Participant information.

    Args:
        match_id ([int]): [Match Id, obtainable from get_matches_for_account]

    Returns:
        [string]: [match_dto]
    """
    api_key = os.getenv("API_KEY")

    # Arrange headers
    headers_dict = {"X-Riot-Token":api_key}

    try:
        response = requests.get(f"https://euw1.api.riotgames.com//lol/match/v4/matches/{match_id}", headers=headers_dict)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse result
    try:
        response_content = response.content
        json_response_content = json.loads(response_content.decode('utf-8'))
        return json_response_content
    except (KeyError, TypeError, ValueError):
        return None

# Basic Integration Test:

#george = get_summoner_by_name("George")
#george_nunu_matches = get_matches_for_account(george["account_id"], 20)
#first_george_nunu_match_reference = george_nunu_matches.get("matches")[0]
#first_george_nunu_match = get_match_for_match_id(first_george_nunu_match_reference.get("gameId"))


