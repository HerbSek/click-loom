import requests
import json



def function_scrape(url:str ,payload:dict) -> dict:
    request = requests.get(url = url , params = payload)
    my_request = request.json()
    return my_request




if __name__ == "__main__":
    url2 = "https://apexherbert200-playwright-scraper-clean.hf.space/scrape"
    url = "https://selenium-scraper-sayw.onrender.com/scrape"  # Replace with your actual API endpoint
    user_input = "https://www.google.com"
    payload = {"url": user_input, "screenshot": True, "get_links":True, "get_body":True, "lead_generation":False }
    
    my_function = function_scrape(url2, payload)
    print(my_function)