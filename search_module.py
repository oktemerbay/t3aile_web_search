import sys
import common.common as common
from dotenv import load_dotenv



def main():
    question = input("Sorunuzu giriniz:")
    api_id = common.get_search_api_id_from_prompt()
    search_web(question, api_id)
    
    
def search_web(question, api_id):
    search_result = ""
    search_api = common.get_search_api_by_id(api_id)
    search_api_function = search_api["api_function"]
    search_result = search_api_function(question)
    common.save_llm_result(search_result)
    print(f"Arama sonucu :{search_result}")
    return search_result


if __name__ == "__main__":
    load_dotenv()
    folderPath = ""
    if len(sys.argv[1:]) > 0:
        folderPath = sys.argv[1:][0]
    main()
