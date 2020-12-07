# this file is here to be used to arrange the data for the summoners

# Basically we're going to have to work out a way of getting the information from the api calls into the database and then manipulating that data in order to arrange the information we need (see app notes)

# at a minimum we need to be able to work out for the last 10 games a player played:
# - what was the outcome
# - what champion did they play
# - what was their score
# etc.
def get_participant_id_for_summoner_for_match(summoner_name, match):
    for participant_identity in match["participantIdentities"]:
        if participant_identity["player"]["summonerName"] == summoner_name:
            return participant_identity["participantId"]
            

def get_participant_data_for_participant_identity(match, participant_id):
    for participant in match["participants"]:
        if participant["participantId"] == participant_id:
            return participant