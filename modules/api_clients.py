import requests


def fetch_petabencana_reports(disaster: str | None = None, admin: str | None = None) -> dict:
    params = {}
    if disaster:
        params["disaster"] = disaster
    if admin:
        params["admin"] = admin
    response = requests.get(
        "https://api.petabencana.id/reports",
        params=params,
        headers={"User-Agent": "SARFlow-Agent/0.1"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def fetch_bmkg_weather(adm4: str) -> dict:
    headers = {"User-Agent": "SARFlow-Agent/0.1"}
    response = requests.get(
        "https://api.bmkg.go.id/publik/prakiraan-cuaca",
        params={"adm4": adm4},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
