import requests
import json
import keys


#########################################
#####              API              #####
#####   - API is case sensitive.    #####
#####   - e.g. teamid != teamId     #####
#########################################


def get_my_team():
    url = "https://www.notexponential.com/aip2pgaming/api/index.php"
    params = {"type": "myTeams", "teamId": keys.TEAM_ID}
    payload = {}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, params=params
    )
    response_in_dict = json.loads(response.text)

    print("My Team is: ", response_in_dict)


def reset_my_team():
    url = "https://www.notexponential.com/aip2pgaming/api/rl/reset.php"

    payload = {}
    params = {"type": "myTeams", "teamId": keys.TEAM_ID, "otp": "5712768807"}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.request(
        "GET", url, headers=headers, data=payload, params=params
    )
    response_in_dict = json.loads(response.text)
    # print("DEBUG: ", response_in_dict)

    if response_in_dict["code"] == "OK":
        print("Successfully Resetted")
    elif response_in_dict["code"] == "FAIL":
        fail_message = response_in_dict["message"]
        print(fail_message)
    else:
        print("*** ERROR ***")


def get_runs(count):  # Get my team's last x runs
    """
    Request Type: GET

    Parameters: type=runs, teamId=$teamId, count=$count
    Return Values: Your previous $count runs with score.
    """

    payload = {}
    params = {"type": "runs", "teamId": keys.TEAM_ID, "count": count}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.get(
        keys.SCORE_URL, headers=headers, data=payload, params=params
    )
    response_in_dict = json.loads(response.text)
    print("DEBUG: ", response_in_dict)

    # TODO


def locate_me():  # Get Location
    """
    Request Type: GET

    Parameters: type=location, teamId=$teamId
    Return Values: your current world and state in that world.
    Think of this as your GPS, and confirm where you are.
    If you are in world “-1”, that means you are in no world, and you can enter a world.

    ***** This call is entirely optional and is useful only for debugging purposes.
    ***** Your program does not need to make this call.
    """

    payload = {}
    params = {"type": "location", "teamId": keys.TEAM_ID}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.get(
        url=keys.WORLD_URL, headers=headers, data=payload, params=params
    )
    response_in_dict = json.loads(response.text)
    # print("DEBUG: ", response_in_dict)
    return response_in_dict


def enter_world(world_id):
    """
    Request Type: POST

    Parameters: type=location, worldId=$worldId, teamId=$teamId
    Return Values: your current world and state in that world.
    Think of this as your GPS, and confirm where you are.
    If you are in world “-1”, that means you are in no world, and you can enter a world.

    ***** This call is entirely optional and is useful only for debugging purposes.
    ***** Your program does not need to make this call.
    """

    payload = {"type": "enter", "worldId": world_id, "teamId": keys.TEAM_ID}
    params = {}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.post(keys.WORLD_URL, headers=headers, data=payload)
    response_in_dict = json.loads(response.text)

    # "[0,0]"
    # move_t = tuple(...) == ('0', '0')
    # move = f"[{move_t[0]},{move_t[1]}]""

    print(response_in_dict)
    # print("DEBUG:", response.text)
    return response_in_dict
    # TODO


def make_move(move, world_id):
    """
    Request Type: POST

    Body: type="move", teamId=$teamId, move="$move", worldId=$worldId
    Return Values: Reward, New State entered $runId started

    Fails if you are not already in a world (in that case, enter a world first).

    ***** This is the central part of your "learning" agent.
    ***** Your program needs to carefully process the result.
    ***** Introduce a delay and do not make more than one move call every 15 seconds..
    """

    payload = {
        "type": "move",
        "teamId": keys.TEAM_ID,
        "move": move,
        "worldId": world_id,
    }
    params = {}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.post(
        url=keys.WORLD_URL, headers=headers, data=payload, params=params
    )
    # print("DEBUG:", response.text)  # Example Result of Success: {"code":"OK","worldId":0,"runId":"14","reward":10000,"scoreIncrement":51.5399999999999991473487108787977695465087890625,"newState":null}
    # Example Result of Fail: {"code":"FAIL","message":"No run is open for this team and world."}

    if len(response.text) != 0:  # There is some messages in the response
        response_in_dict = json.loads(response.text)
        # print("DEBUG:", response_in_dict)  # Example: {'code': 'OK', 'worldId': 0, 'runId': '14', 'reward': 10000, 'scoreIncrement': 51.5399999999999991473487108787977695465087890625, 'newState': null}
        if response_in_dict["code"] == "OK":  # Success
            print(response_in_dict)
            return (
                response_in_dict["reward"],
                response_in_dict["newState"],
            )
        elif response_in_dict["code"] == "FAIL":  # Fail
            print(response_in_dict["message"])
        else:
            print("*** ERROR ***")
    else:  # Another type of Fail
        print("*** ERROR ***")


def get_score():
    """
    Request Type: GET

    Parameters: type=score, teamId=$teamId
    Return Values: score. Fails if you are not in the team (you can only get scores for your team).

    ***** This call is entirely optional and will be useful only after many runs have been completed.
    ***** Your program never needs to make this call.
    """

    payload = {}
    params = {"type": "score", "teamId": keys.TEAM_ID}
    headers = {
        "x-api-key": keys.API_KEY,
        "userId": keys.USER_ID,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "PostmanRuntime/7.37.0",
    }

    response = requests.get(
        keys.SCORE_URL, headers=headers, data=payload, params=params
    )
    # print("DEBUG:", response.text)  # Example Result of Success: {"score":0,"code":"OK"}
    # Example Result of Fail: {"code":"FAIL","message":"Invalid team ID, or you are not in the team"}
    response_in_dict = json.loads(response.text)
    # print("DEBUG:", response_in_dict)  # Example: {'score': 0, 'code': 'OK'}

    if response_in_dict["code"] == "OK":
        score = response_in_dict["score"]
        # print("DEBUG:", score)
        return score
    elif (
        response_in_dict["code"] == "FAIL"
    ):  # Fails if the team ID is invalid or if you are not in the team
        fail_message = response_in_dict["message"]
        print(fail_message)  # Example: Invalid team ID, or you are not in the team
    else:
        print("*** ERROR ***")


#########################################
#####         Testing Calls         #####
#########################################

# get_my_team()
# reset_my_team()
# get_runs(count=10)
# enter_world(0)
# locate_me()

# print(make_move(move="S", world_id="0"))
# reward, current_pos = make_move(move="N", world_id="0")
# print(f"Reward: {reward}")
# print(f"Current pos: {current_pos}")
# get_score()
