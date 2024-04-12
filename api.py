import requests
import json
import keys

#########################################
#####              API              #####
#####   - API is case sensitive.    #####
#####   - e.g. teamid != teamId     #####
#########################################

def enter_world(world_id):

    payload = {"type": "enter", "worldId": world_id, "teamId": keys.TEAM_ID}
    params = {}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.post(
        keys.WORLD_URL,
        headers=headers,
        data=payload,
    )
    print(response.text)


def locate_me():

    payload = {}
    params = {"type": "location", "teamId": keys.TEAM_ID}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.get(
        keys.WORLD_URL, headers=headers, data=payload, params=params
    )
    print(response.text)
    

def get_score(team_id):
    """
    Request Type: GET

    Parameters: type=score, teamId=$teamId
    Return Values: score. Fails if you are not in the team (you can only get scores for your team).
    
    ***** This call is entirely optional and will be useful only after many runs have been completed.
    ***** Your program never needs to make this call.
    """

    payload = {}
    params = {"type": "score", "teamId": team_id}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.get(keys.SCORE_URL, headers=headers, data=payload, params=params)
    # print("DEBUG:", response.text)  # Example Result of Success: {"score":0,"code":"OK"}
                                      # Example Result of Fail: {"code":"FAIL","message":"Invalid team ID, or you are not in the team"}
    response_in_dict = json.loads(response.text)
    # print("DEBUG:", response_in_dict)  # Example: {'score': 0, 'code': 'OK'}

    if response_in_dict["code"] == "OK":
        score = response_in_dict["score"]
        # print("DEBUG:", score)
        return score
    elif response_in_dict["code"] == "FAIL":  # Fails if the team ID is invalid or if you are not in the team
        fail_message = response_in_dict["message"]
        print(fail_message)  # Example: Invalid team ID, or you are not in the team
    else:
        print("*** ERROR ***")



#########################################
#####         Testing Calls         #####
#########################################

# enter_world(0)
# locate_me()

get_score(team_id=1397)