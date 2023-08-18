from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
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
    url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/80ce1635-5b07-4c07-b501-faf8beb04e6c/actions/dealership-package/get-dealership-reviews"

    reviews = get_dealer_reviews_from_cf(url, dealer_id)
    reviews_length = len(reviews)

    if reviews_length > 0: 
        context["reviews"] = reviews
        if context["reviews"]:
            context["response_code"] = "Success"
        else:
            context["response_code"] = "Fail"

        return render(request, "djangoapp/dealer_details.html", context)

    else: 
        context["message"] = "Be the first to add a review!"
        return render(request, "djangoapp/dealer_details.html", context)

    # add 'success' and 'error' to context. Just use the request response
    
    

def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80ce1635-5b07-4c07-b501-faf8beb04e6c/dealership-package/post-dealership-reviews"
        user = request.user
        if user:
            review = {}
            review["time"] = datetime.utcnow.isoformat()
            review["dealership"] = dealer_id
            review["review"] = False

            json_payload = {}
            json_payload["review"] = review

            result = post_request(url, json_payload, dealer_id=dealer_id)
            context["review_succes"] = True
            context["result"] = result
    return render(request, "djangoapp/index.html", context)

def getDealerReviews():
    # query the database with dealer_id
    # etc.
    # return object with queried data
    return False
