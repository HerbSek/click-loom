import requests
import json



def function_scrape(url:str ,payload:dict) -> dict:
    request = requests.get(url = url , params = payload)
    my_request = request.json()
    return my_request




if __name__ == "__main__":

    url = "https://selenium-scraper-sayw.onrender.com/scrape"  # Replace with your actual API endpoint
    user_input = "https://www.google.com"
    payload = {"link": user_input }
    
    my_function = function_scrape(url, payload)
    print(my_function)