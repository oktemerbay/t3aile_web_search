import requests
import datetime
from typing import List

def search_web(query: str) -> List[dict]:
    from common.common import get_random_file_name_for_brave_search_api_without_extension, search_web_save_result_and_get_snippets , get_brave_search_api_token
    API_TOKEN = get_brave_search_api_token()
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": API_TOKEN
    }
    params = {
        "q": query,
        #"count": 10
    }
    start = datetime.datetime.now()
    res = requests.get("https://api.search.brave.com/res/v1/web/search",
                       headers=headers, params=params)
    end = datetime.datetime.now()
    duration = str((end - start).total_seconds())
    search_result_json = res.json()
    fileName = get_random_file_name_for_brave_search_api_without_extension()
    snippets, str_val, my_dict = search_web_save_result_and_get_snippets(
        search_result_json, duration, fileName, get_snippets_and_str_value)
    return my_dict


def get_snippets_and_str_value(search_dict):
    from common.common import MAX_RESULT_NUM, strip_html
    str_val = ""
    snippets = []
    my_dict = []
    count = 0
    if "web" in search_dict and "type" in search_dict["web"]:
        if search_dict["web"]["type"] == "search" and search_dict["web"]["results"] and len(search_dict["web"]["results"]) > 0:
            results = search_dict["web"]["results"]
            for result in results:
                if count == MAX_RESULT_NUM:
                    break
                count += 1
                title = strip_html(result["title"])
                description = strip_html(result["description"])
                url = result["url"]
                my_dict_item = {
                    "title": title,
                    "description": description,
                    "url": url
                }
                str_val += str(count) + ". Başlık : " + title
                str_val += " Açıklama/snippet : " + description
                str_val += " URL : " + url
                str_val += "\n"
                snippets.append(result["description"])
                my_dict.append(my_dict_item)
    return snippets, str_val, my_dict
