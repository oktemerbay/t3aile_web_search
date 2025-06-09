import requests
from typing import List
import datetime


def search_web(query: str) -> List[dict]:
    from common.common import get_random_file_name_for_searxng_without_extension, search_web_save_result_and_get_snippets, validate_and_return_url, get_searxng_host_url
    url = get_searxng_host_url()
    if not url:
        url = validate_and_return_url()
    start = datetime.datetime.now()
    params = {
        "q": query,
        "format": "json"
    }
    res = requests.get(url,
                       headers={
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                       }, params=params)
    end = datetime.datetime.now()
    duration = str((end - start).total_seconds())
    if res.status_code == 200:
        # (json.dumps(res.json(), indent=4, ensure_ascii=False)
        search_result_json = res.json()
        fileName = get_random_file_name_for_searxng_without_extension()
        snippets, str_val, my_dict = search_web_save_result_and_get_snippets(
            search_result_json, duration, fileName, get_snippets_and_str_value)
        return my_dict
    return None


def get_snippets_and_str_value(search_dict):
    from common.common import MAX_RESULT_NUM
    results = search_dict["results"]
    str_val = ""
    snippets = []
    my_dict = []
    count = 0
    for result in results:
        if count == MAX_RESULT_NUM:
            break
        count += 1
        title = result["title"]
        description = result["content"]
        url = result["url"]
        my_dict_item = {
            "title": title,
            "description": description,
            "url": url
        }
        str_val += str(count) + ". Başlık : "+result["title"]
        str_val += " Açıklama/snippet : "+result["content"]
        str_val += " URL : " + result["url"]
        str_val += "\n"
        snippets.append(result["content"])
        my_dict.append(my_dict_item)
    return snippets, str_val, my_dict
