import requests
import json
import os
from .models import CarDealer, DealerReview, CarModel, CarMake
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    my_params = {}
    my_params["dealer_id"] = str(kwargs.get("dealer_id"))

    try:
        response = requests.get(url, headers={"Content-Type": "application/json"}, params=my_params)
    except:
        print("Network exception occurred")

    json_data = json.loads(response.text)

    return json_data

def post_request(url, json_payload, **kwargs):

    response = None

    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=json_payload, params=kwargs)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Network exception occurred", e)

    if response is not None:
        json_data = response.json()
        return json_data
    else: 
        return None
    
def form_get_dealer_details(url, dealer_id):
    
    json_results =  get_request(url, dealer_id=dealer_id)

    result_doc = {}

    dealership_cars_Django = CarModel.objects.filter(dealer_id=dealer_id)

    form_car_options = list(dealership_cars_Django.values())

    result_doc["options_cars"] = form_car_options

    if json_results:
        website_json_results = json_results["docs"]
        print(f"json_results = {website_json_results}")

        for form_info in website_json_results:

            result_doc["full_name"] = form_info["full_name"]
            result_doc["city"] = form_info["city"]
            result_doc["lat"] = form_info["lat"]
            result_doc["long"] = form_info["long"]
            result_doc["state"] = form_info["state"]
            result_doc["lat"] = form_info["lat"]

        return result_doc
  
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
                id=reviews["_id"],
            )
            results.append(dealer_obj)
    return results

def analyze_review_sentiments(text):
    api_key_NLU = os.environ.get("NLU_API")
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/efaf0a34-acf7-4c2c-8ba4-2daa962f0571"
    params = json.dumps({"text": text, "features": {"sentiment": {}}})
    response = requests.post(
        url,
        data=params,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth("apikey", api_key_NLU),
    )
    try:
        return response.json()["sentiment"]["document"]["label"]
    except KeyError:
        return "neutral"

def form_get_car_info(car_id):

    result = {}

    car_details_from_models = CarModel.objects.get(pk=car_id)

    result["car_make"] = car_details_from_models.make.name
    result["car_model"] = car_details_from_models.name
    result["car_year"] = car_details_from_models.name

    return result