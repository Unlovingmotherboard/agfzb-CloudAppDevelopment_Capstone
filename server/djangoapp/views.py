from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, form_get_dealer_details, form_get_car_info
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

def about(request):
    if request.method == "GET":
        return render(request, "djangoapp/about.html")

def contact(request):
    if request.method == "GET":
        return render(request, "djangoapp/contact.html")

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"] = "Invalid username or password."
            return render(request, "djangoapp/index.html", context)
    else:
        return render(request, "djangoapp/index.html", context)

def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["register_message_error"] = "User already exists"
            return render(request, "djangoapp/registration.html", context)

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80ce1635-5b07-4c07-b501-faf8beb04e6c/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        context["dealers"] = dealerships

        return render(request, "djangoapp/index.html", context)


def get_dealer_details(request, dealer_id):
    context = {}
    
    print("")
    print(f"Inside of get dealer details: {dealer_id}")
    #if request.method == "POST":
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/80ce1635-5b07-4c07-b501-faf8beb04e6c/dealership-package/get-dealership-reviews.json"

    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    reviews_length = len(reviews)
    context["our_dealer_id"] = dealer_id
    if reviews_length > 0: 
        context["reviews"] = reviews
        if context["reviews"]:
            context["response_code"] = "Success"
        else:
            context["response_code"] = "Fail"
        print(context["reviews"])
        return render(request, "djangoapp/dealer_details.html", context)

    else: 
        context["message"] = "Be the first to add a review!"
        return render(request, "djangoapp/dealer_details.html", context)

    # add 'success' and 'error' to context. Just use the request response
    
    

def add_review(request, dealer_id):
    context = {}
    
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80ce1635-5b07-4c07-b501-faf8beb04e6c/dealership-package/form-get-dealership.json"
        dealership_details = form_get_dealer_details(url, dealer_id) #make API call for this dealer 
        #get_dealership_cars = False #Get car details 
        console_dealership_details = json.dumps(dealership_details, indent=4)
        context["dealer"] = dealership_details
        context["full_name"] = dealership_details["full_name"]
        context["options_cars"] = dealership_details["options_cars"]

        return render(request, "djangoapp/add_review.html", context)

    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80ce1635-5b07-4c07-b501-faf8beb04e6c/dealership-package/post-dealership-reviews"
        user = request.user
        review_data = request.POST
       
        if user:
            review = {}

            car_details_from_restapi = form_get_car_info(review_data['car'])

            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

            review["time"] = formatted_datetime
            review["dealership"] = dealer_id
            review["review"] = review_data["form_review"]

            form_purchasecheck = review_data.get("purchasecheck")

            if form_purchasecheck is not None:
                review["purchase"] = True
            else:
                review["purchase"] = False

            review["purchase_date"] = review_data["purchasedate"]
            review["car_make"] = car_details_from_restapi["car_make"]
            review["car_model"] = car_details_from_restapi["car_model"]
            review["car_year"] = car_details_from_restapi["car_year"]
            review["name"] = str(user)

            json_payload = {}
            json_payload["review"] = review

            result = post_request(url, json_payload, dealer_id=dealer_id)
            print("")
            print(f"result: {result}")

            context["result"] = result
    return render(request, "djangoapp/index.html", context)

def getDealerReviews():
    # query the database with dealer_id
    # etc.
    # return object with queried data
    return False
