import requests
import json
import keys


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


# enter_world(0)
locate_me()
