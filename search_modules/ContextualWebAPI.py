import requests
from typing import List
import datetime


def search_web(query: str) -> List[dict]:
    from common.common import get_random_file_name_for_contextual_web_api_without_extension, search_web_save_result_and_get_snippets, get_contextual_web_api_key
    API_KEY = get_contextual_web_api_key()
    url = "https://real-time-web-search.p.rapidapi.com/search-advanced"
    querystring = {"q": query,
                   "num": "10", "start": "0", "gl": "us", "hl": "en", "nfpr": "0"}
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "real-time-web-search.p.rapidapi.com"
    }
    start = datetime.datetime.now()
    response = requests.get(url, headers=headers, params=querystring)
    end = datetime.datetime.now()
    duration = str((end - start).total_seconds())
    search_result_json = response.json()
    fileName = get_random_file_name_for_contextual_web_api_without_extension()
    snippets, str_val, my_dict = search_web_save_result_and_get_snippets(
        search_result_json, duration, fileName, get_snippets_and_str_value)
    return my_dict


def get_snippets_and_str_value(search_dict):
    from common.common import MAX_RESULT_NUM
    results = search_dict["data"]
    str_val = ""
    snippets = []
    my_dict = []
    count = 0
    for result in results:
        if count == MAX_RESULT_NUM:
            break
        count += 1
        title = result["title"]
        description = result["snippet"]
        url = result["url"]
        my_dict_item = {
            "title": title,
            "description": description,
            "url": url
        }
        str_val += str(count) + ". Başlık : "+result["title"]
        str_val += " Açıklama/snippet : "+result["snippet"]
        str_val += " URL : " + result["url"]
        str_val += "\n"
        snippets.append(result["snippet"])
        my_dict.append(my_dict_item)
    return snippets, str_val, my_dict
