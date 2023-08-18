import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print("")
    print(":)")
    print(f"kwargs: {kwargs}")
    # print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    # print(f"response: {response}")
    # print("With status {} ".format(status_code))

    json_data = json.loads(response.text)

    return json_data

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=json_payload, params=kwargs)

    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def get_dealers_from_cf(url, **kwargs):
    results = []
    
    json_result = get_request(url)
    if json_result:
        
        dealers = json_result["result"]["rows"]
        
        for dealer in dealers:

            dealer_doc = dealer["doc"]

            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            results.append(dealer_obj)
    return results

def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    print("")
    print(f"Inside of restapi:-  url: {url} dealer_id:{dealer_id}")
    
    json_result = get_request(url, dealer_id=dealer_id)
    print("")
    print(f"url: {url}")
    print(f"After calling IBM Function:-  json_results: {json_result}")

    if json_result["error"]: 
        print("")
        print("error")
        return results

    if json_result:
        dealers_reviews = json_result["docs"]
        dealers_reviews_print = json.dumps(dealers_reviews, indent=4)
        print("")
        print(f"{dealers_reviews_print}")
        for reviews in dealers_reviews:
            dealer_obj = DealerReview(
                dealership=reviews["dealership"],
                sentiment=analyze_review_sentiments(reviews["review"]),
                name=reviews["name"],
                purchase=reviews["purchase"],
                review=reviews["review"],
                purchase_date=reviews["purchase_date"],
                car_make=reviews["car_make"],
                car_model=reviews["car_model"],
                car_year=reviews["car_year"],
                id=reviews["id"],
            )
            results.append(dealer_obj)
    return results

def analyze_review_sentiments(text):
    api_key = os.environ.get("NLU_API")
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/efaf0a34-acf7-4c2c-8ba4-2daa962f0571"
    params = json.dumps({"text": text, "features": {"sentiment": {}}})
    response = requests.post(
        url,
        data=params,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth("apikey", api_key),
    )
    try:
        return response.json()["sentiment"]["document"]["label"]
    except KeyError:
        return "neutral"
