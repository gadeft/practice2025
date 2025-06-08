import requests
import json

#URL to google translate API
URL = "https://google-translate113.p.rapidapi.com/api/v1/translator/json"

headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "google-translate113.p.rapidapi.com",
    "x-rapidapi-key": "78814a8045mshe98cdd3102137b3p1d10c1jsn72f109803478",
}

'''
Body of the request
language_to and language_from must be language codes 
'''
def get_payload(message, language_to, language_from):
    return {
        "from": language_from,
        "to": language_to,
        "json": {
            "title": message,
        }
    }

'''
Gets translation of the message within one language
language_to and language_from must be language codes
Returns translated message
'''
def translator(message, language_to, language_from) -> str:
    payload = get_payload(message, language_to, language_from)
    response = requests.post(URL, headers=headers, data=json.dumps(payload))
    return response.json()["trans"]["title"]

'''
Translates message into multiple languages
languages_to and language_from must be language codes
Returns translated message on selected languages
'''
def translate(message, languages_to: list, language_from = "auto") -> dict:
    translated = dict()
    for lang in languages_to:
        translated[lang] = translator(message, lang, language_from)
    return translated