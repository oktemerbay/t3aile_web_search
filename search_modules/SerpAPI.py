from serpapi import GoogleSearch
import datetime
from typing import List


def search_web(query: str) -> List[dict]:
    from common.common import get_random_file_name_for_serp_api_without_extension, search_web_save_result_and_get_snippets, get_serp_api_api_key
    API_KEY = get_serp_api_api_key()
    start = datetime.datetime.now()
    search = GoogleSearch({
        "q": query,
        "location": "Turkey",
        "api_key": API_KEY
    })
    end = datetime.datetime.now()
    duration = str((end - start).total_seconds())
    search_result_json = search.get_dict()
    fileName = get_random_file_name_for_serp_api_without_extension()
    snippets, str_val, my_dict = search_web_save_result_and_get_snippets(
        search_result_json, duration, fileName, get_snippets_and_str_value)
    return my_dict


def get_snippets_and_str_value(search_dict):
    from common.common import MAX_RESULT_NUM
    results = search_dict["organic_results"]
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
        url = result["link"]
        my_dict_item = {
            "title": title,
            "description": description,
            "url": url
        }
        str_val += str(count) + ". Başlık : "+result["title"]
        str_val += " Açıklama/snippet : "+result["snippet"]
        str_val += " URL : " + result["link"]
        str_val += "\n"
        snippets.append(result["snippet"])
        my_dict.append(my_dict_item)
    return snippets, str_val, my_dict
