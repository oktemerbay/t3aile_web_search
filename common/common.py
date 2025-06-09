import time
import json
from bs4 import BeautifulSoup
import search_modules.BraveSearchAPI as BraveSearchAPI
import search_modules.SerpAPI as SerpAPI
import search_modules.GoogleCustomSearch as GoogleCustomSearch
import search_modules.ContextualWebAPI as ContextualWebAPI
import search_modules.SerperDev as SerperDev
import search_modules.Searxng as Searxng
import common.LLMEvaulator as LLMEvaulator
from urllib.parse import urlparse
import os
import common.constants

MAX_RESULT_NUM = 10

SERP_API = "SerpAPI"
BRAVE_SEARCH_API = "BraveSearchAPI"
# LLM_FOLDER_RESULT_PATH = "D:/Geliştirme Notları/T3AILE/T3AI Topluluk Projeleri/searchAPI/model_search_result/"


def get_miliseconds():
    return str(int(time.time() * 1000.0))


def get_random_file_name():
    return get_miliseconds() + ".txt"


def get_random_file_name_without_extension():
    return get_miliseconds()


def get_random_file_name_for_serp_api():
    return "serp_api_log_"+get_random_file_name()


def get_random_file_name_for_serp_api_without_extension():
    return "serp_api_log_"+get_random_file_name_without_extension()


def get_random_file_name_for_searxng_without_extension():
    return "searxng_log_"+get_random_file_name_without_extension()


def get_random_file_name_for_serper_dev_without_extension():
    return "serper_dev_log_"+get_random_file_name_without_extension()


def get_random_file_name_for_google_custom_search_api_without_extension():
    return "google_custom_search_log_"+get_random_file_name_without_extension()


def get_random_file_name_for_contextual_web_api_without_extension():
    return "contextual_web_api_search_log_"+get_random_file_name_without_extension()


def get_random_file_name_for_brave_search_api():
    return "brave_search_api_log_"+get_random_file_name()


def get_random_file_name_for_brave_search_api_without_extension():
    return "brave_search_api_log_"+get_random_file_name_without_extension()


def log_result(result, response_duration, file_name):
    fileToWrite = open(file=file_name, mode="wb")
    resultJsonFormattedBytes = json.dumps(
        result, ensure_ascii=False, indent=2).encode('utf8')
    fileToWrite.write(resultJsonFormattedBytes)
    response_duration_st = str(
        "\n\nResponse Duration:" + str(response_duration)).encode("utf8")
    fileToWrite.write(response_duration_st)
    fileToWrite.close()


def save_file(content, filePath):
    filePath = filePath
    file = open(file=filePath, mode="w", encoding="utf8")
    file.write(content)
    file.close()


def create_folder_if_not_exists(folder):
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print(f"folder created {folder}")
        return True
    except Exception as e:
        print(f"create_folder_if_not_exists error {e}")
        return False


def search_web_save_result_and_get_snippets(result, duration, fileName, get_snippets_func):
    snippets, str_val, my_dict = get_snippets_func(result)
    operation_path = get_main_operation_path()
    if create_folder_if_not_exists(operation_path):
        jsoFileName = fileName + ".json"
        folderPathRaw = operation_path + \
            common.constants.SEARCH_RAW_RESULT_FOLDER_NAME + "/"
        folderPath = operation_path + common.constants.SEARCH_RESULT_FOLDER_NAME + "/"
        if create_folder_if_not_exists(folderPathRaw) and create_folder_if_not_exists(folderPath):
            filePathRaw = folderPathRaw + jsoFileName
            log_result(result, duration, filePathRaw)
            t3_aile_formatted_file_name = fileName + "web_result.txt"
            filePath = folderPath + t3_aile_formatted_file_name
            save_file(str_val, filePath)
    return snippets, str_val, my_dict


def strip_html(text):
    return BeautifulSoup(text, "html.parser").get_text()


def save_llm_result(result):
    llm_result_folder_path = get_main_operation_path(
    ) + common.constants.LLM_RESULT_FOLDER_NAME + "/"
    if create_folder_if_not_exists(llm_result_folder_path):
        print(f"Result is written to path {llm_result_folder_path}")
        file_name = "llm_result_" + get_random_file_name_without_extension() + ".txt"
        full_file_path = llm_result_folder_path + file_name
        print("model result saved at:", full_file_path)
        file = open(file=full_file_path, mode="w", encoding="utf8")
        file.write(result)


def print_api_choices():
    print("\n\n***********")
    for api in SEARCH_APIS:
        print(f"{api['name']} için {api['id']}")
    print("***********\n\n")


def is_api_choice_valid(api_id):
    if next((id for search_api in SEARCH_APIS if search_api["id"] == api_id), None):
        return True
    return False


def search_web_using_google_custom_search_api(question):
    print("\n\n*********\n")
    print("Google Custom Search API ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = GoogleCustomSearch.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")


def search_web_using_brave_search_api(question):
    print("\n\n*********\n")
    print("Brave Search API ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = BraveSearchAPI.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")


def search_web_using_serp_api(question):
    print("\n\n*********\n")
    print("Serp API ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = SerpAPI.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")


def search_web_using_contextual_web_api(question):
    print("\n\n*********\n")
    print("Contextual Web API ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = ContextualWebAPI.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")


def search_web_using_serper_dev(question):
    print("\n\n*********\n")
    print("Serper Dev ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = SerperDev.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")


def search_web_using_searxng(question):
    print("\n\n*********\n")
    print("Searxng ile arama başlatılıyor")
    print("\n*********\n")
    content_dict = Searxng.search_web(question)
    if is_use_faiss():
        content_dict = LLMEvaulator.evaluate_with_rag_faiss_and_return_only_description(question, content_dict)
    return LLMEvaulator.evaluate_with_rag(question, content_dict, "ozcangundes/mt5-small-turkish-squad")
    # return LLMEvaulator.evaluate_with_rag_v3(question, content_dict, "duxx/DeepSeek-R1-Distill-Qwen-1.5B-Turkish")
    # return LLMEvaulator.evaluate_with_rag(question, content_dict, "vngrs-ai/VBART-Medium-Base")
    # return LLMEvaulator.evaluate_with_rag_v2(question, content_dict, "vngrs-ai/VBART-Medium-Base")
    # return LLMEvaulator.evaluate_with_rag(question, content_dict, "cengines/Orhun-R-7B-v1")
    # return LLMEvaulator.evaluate_with_rag_faiss(question, my_dict, "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def get_search_api_by_id(id):
    return next((search_api for search_api in SEARCH_APIS if search_api["id"] == id), None)


def get_search_api_id_from_prompt():
    print_api_choices()
    api_choice_valid = False
    while not api_choice_valid:
        api_choice = input(
            "Yukarıdaki bilgilere göre uygun api seçiminizi giriniz:")
        api_choice_valid = is_api_choice_valid(api_choice)
        if not api_choice_valid:
            print("Yanlış değer girdiniz")
    return api_choice


SEARCH_APIS = [
    {
        "id": "1",
        "name": "Google Custom Search API",
        "api_function": search_web_using_google_custom_search_api
    },
    {
        "id": "2",
        "name": "Brave Search API",
        "api_function": search_web_using_brave_search_api
    },
    {
        "id": "3",
        "name": "Serp API",
        "api_function": search_web_using_serp_api
    },
    {
        "id": "4",
        "name": "Contextual Web API",
        "api_function": search_web_using_contextual_web_api
    },
    {
        "id": "5",
        "name": "SERPER DEV",
        "api_function": search_web_using_serper_dev
    },
    {
        "id": "6",
        "name": "SEARXNG",
        "api_function": search_web_using_searxng
    }
]


def validate_and_return_url():
    is_valid = False
    while (not is_valid):
        url = input("Enter url:")
        if not url:
            is_valid = True
            url = "http://localhost:8080/search"
        result = urlparse(url)
        if (result.scheme == "http" or result.scheme == "https") \
                and len(result.netloc) > 0:
            is_valid = True
        else:
            print("Invalid url please try again")
            is_valid = False
    print(f"url is {url}")
    return url


def get_env_variable(key):
    value = os.getenv(key)
    if value:
        return value
    else:
        raise ValueError(f"No value for the key : {key} exists")


def get_env_variable_without_raising_error(key):
    value = ""
    try:
        value = os.getenv(key)
    except:
        print("get_env_variable_with_raising_error error occurred")
    return value


def get_main_operation_path():
    return get_env_variable_without_raising_error("MAIN_OPERATION_PATH")


def get_brave_search_api_token():
    return get_env_variable("BRAVE_SEARCH_TOKEN")


def get_searxng_host_url():
    return get_env_variable_without_raising_error("SEARXNG_HOST_URL")


def get_contextual_web_api_key():
    return get_env_variable("CONTEXTUAL_WEB_API_KEY")


def get_google_custom_search_key():
    return get_env_variable("GOOGLE_CUSTOM_SEARCH_KEY")


def get_google_custom_search_cx():
    return get_env_variable("GOOGLE_CUSTOM_SEARCH_CX")


def get_serp_api_api_key():
    return get_env_variable("SERP_API_API_KEY")


def get_serper_dev_api_key():
    return get_env_variable("SERPER_DEV_API_KEY")

def is_use_faiss():
    res = get_env_variable_without_raising_error("IS_USE_FAISS")
    return res == "True"