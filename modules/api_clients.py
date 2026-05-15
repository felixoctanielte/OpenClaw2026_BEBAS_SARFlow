import os

import requests


def fetch_petabencana_reports(disaster: str | None = None, admin: str | None = None) -> dict:
    params = {}
    if disaster:
        params["disaster"] = disaster
    if admin:
        params["admin"] = admin
    response = requests.get(
        "https://data.petabencana.id/reports",
        params=params,
        headers={"User-Agent": "SARFlow-Agent/0.1"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def fetch_bmkg_weather(adm4: str) -> dict:
    api_key = os.getenv("BMKG_API_KEY", "")
    headers = {"User-Agent": "SARFlow-Agent/0.1"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    response = requests.get(
        "https://api.bmkg.go.id/publik/prakiraan-cuaca",
        params={"adm4": adm4},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()

