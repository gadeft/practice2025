import requests
import json

URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/json"

headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "google-translate113.p.rapidapi.com",
    "x-rapidapi-key": "78814a8045mshe98cdd3102137b3p1d10c1jsn72f109803478",
}

def translator(message, lang_code_to, lang_code_from = "auto") -> str:
    payload = {
        "from": lang_code_from,
        "to": lang_code_to,
        "json": {
            "title": message,
        }
    }
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return response.json()["trans"]["title"]


def translate(message, languages_to: list, lang_code_from = "auto") -> dict:
    translated = dict()
    for lang in languages_to:
        translated[lang] = translator(message, lang, lang_code_from)

    return translated