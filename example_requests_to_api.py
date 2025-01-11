import requests


BASE_URL = "http://localhost:5000/"


def register(username, password):
    url = BASE_URL + "auth/register"
    data = {"username": username, "password": password}
    res = requests.post(url=url, json=data)
    print(res.status_code)
    print(res.text)


def login(username, password):
    url = BASE_URL + "auth/login"
    data = {"username": username, "password": password}
    res = requests.post(url=url, json=data)
    print(res.status_code)
    print(res.text)
    return res.json()["access_token"]


def create_strategy(name, description, asset_type, buy_conditions, sell_conditions, status):
    url = BASE_URL + "strategies"

    data = dict()
    data["name"] = name
    data["description"] = description
    data["asset_type"] = asset_type
    data["buy_conditions"] = buy_conditions
    data["sell_conditions"] = sell_conditions
    data["status"] = status

    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.post(url=url, json=data, headers=headers)
    print(res.status_code)
    print(res.text)


def read_strategies():
    url = BASE_URL + "strategies"

    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url=url, headers=headers)
    print(res.status_code)
    print(res.text)


def update_strategy(
    st_id,
    name: str | None = None,
    description: str | None = None,
    asset_type: str | None = None,
    buy_conditions: dict | None = None,
    sell_conditions: dict | None = None,
    status: str | None = None,
):
    url = BASE_URL + f"strategies/{st_id}"

    data = dict()
    data["name"] = name
    data["description"] = description
    data["asset_type"] = asset_type
    data["buy_conditions"] = buy_conditions
    data["sell_conditions"] = sell_conditions
    data["status"] = status

    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.patch(url=url, json=data, headers=headers)
    print(res.status_code)
    print(res.text)


def delete_strategy(st_id):
    url = BASE_URL + f"strategies/{st_id}"

    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.delete(url=url, headers=headers)
    print(res.status_code)
    print(res.text)


def simulate_strategy(st_id, history: list[dict]):
    url = BASE_URL + f"strategies/{st_id}/simulate"

    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"historical_data": history}
    res = requests.post(url=url, json=data, headers=headers)
    print(res.status_code)
    print(res.text)


register("example", "1234")
access_token = login("example", "1234")

if __name__ == "__main__":
    create_strategy(
        name="Momentum Strategy",
        description="Buy assets when momentum exceeds thresholds",
        asset_type="stock",
        buy_conditions={"indicator": "momentum", "threshold": 1.5},
        sell_conditions={"indicator": "momentum", "threshold": -1.5},
        status="active",
    )
    read_strategies()
    update_strategy(1, name="New strategy name")
    read_strategies()
    simulate_strategy(
        1,
        [
            {"date": "2024-06-01", "open": 100.5, "close": 102.3, "high": 103.0, "low": 99.8, "volume": 150000},
            {"date": "2024-06-02", "open": 102.3, "close": 104.7, "high": 105.5, "low": 101.2, "volume": 180000},
        ],
    )
    delete_strategy(1)
    read_strategies()
