from multiprocessing import context
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import UsersDetails
from .models import Ser

from .forms import UserDetailForm

import requests, json
from django.conf import settings

# Create your views here.

#List
def create_view(request):
    # User Detail fields
    if request.method == "POST":
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        credit_card = request.POST.get("credit_card")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Generate new AES 256 key using Randtronics DPM easyKey API
        url = settings.RANDTRONICS_EASYKEY_API + "/dpmkm_kmip/easyKeyRest/doCreate"
        payload = {
            "policy": "Default Key Policy",
            "keyTemplate": "Default Key Template AES-128",
            "dataList": {"dataItem": [{"identifier": "1"}]}
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + settings.RANDTRONICS_EASYEKEY_AUTH_KEY
        }
        response = requests.request("POST", url, headers=headers, json=payload, verify=False)
        uuidkey = response.json()["responseDetails"][0]["uuidKey"] # Get uuidkey from response

        ivnonce = "12345678123456781234567812345678" # You can generate this as well.


        # Encrypt credit card number and password using AES 256 key
        url = settings.RANDTRONICS_EASYKEY_API + "/dpmkm_kmip/easyKeyRest/doEncrypt"
        payload = {
            "uuidKey": uuidkey,
            "cryptographicParameters": {"blockCipherMode": "CBC"},
            "dataList": {"dataItem": [
                    {
                        "identifier": "1",
                        "data": credit_card,
                        "ivCounterNonce": ivnonce
                    },
                    {
                        "identifier": "2",
                        "data": email,
                        "ivCounterNonce": ivnonce
                    }
                ]}
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic " + settings.RANDTRONICS_EASYEKEY_AUTH_KEY
        }

        response = requests.request("POST", url, json=payload, headers=headers, verify=False)
        encrypted_credit_card = response.json()["responseDetails"][0]["data"]
        encrypted_email = response.json()["responseDetails"][1]["data"]

        # Create User Detail
        user = UsersDetails(
            name=name,
            gender=gender,
            phone=phone,
            credit_card=encrypted_credit_card,
            username=username,
            email=encrypted_email,
            password=password,
            uuidkey=uuidkey,
            ivnonce=ivnonce
        )
        user.save()
        return HttpResponseRedirect("/") # Redirect to list_view
    else:
        genders = ["Male", "Female", "Other"]
        context = {
            "genders": genders
        }
        return render(request, "create_view.html", context)

#List
def list_view(request):

    get_data = UsersDetails.objects.all()

    ids = []
    names = []
    genders = []
    phones = []  
    credit_cards = []
    usernames = []
    emails = []
    passwords = []
    for data in get_data:
        ids.append(data.id) 
        names.append(data.name)
        genders.append(data.gender)
        phones.append(data.phone)

        if data.uuidkey != "":
            # Decrypt credit card number and email and password using AES 256 key
            url = settings.RANDTRONICS_EASYKEY_API + "/dpmkm_kmip/easyKeyRest/doDecrypt"
            payload = {
                "uuidKey": data.uuidkey,
                "cryptographicParameters": {"blockCipherMode": "CBC"},
                "dataList": {"dataItem": [
                        {
                            "identifier": "1",
                            "data": data.credit_card,
                            "ivCounterNonce": data.ivnonce
                        },
                        {
                            "identifier": "2",
                            "data": data.email,
                            "ivCounterNonce": data.ivnonce
                        }
                    ]}
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Basic " + settings.RANDTRONICS_EASYEKEY_AUTH_KEY
            }
            response = requests.request("POST", url, json=payload, headers=headers, verify=False)
            decrypted_credit_card = response.json()["responseDetails"][0]["data"]
            decrypted_email = response.json()["responseDetails"][1]["data"]

            credit_cards.append(decrypted_credit_card)
            emails.append(decrypted_email)
        else:
            credit_cards.append(data.credit_card)
            emails.append(data.email)
        usernames.append(data.username)
        passwords.append(data.password)

    all_data = []
    for i in range(len(ids)):
        all_data.append({"id": ids[i],
                            "name": names[i],
                            "gender": genders[i],
                            "email": emails[i],
                            "phone": phones[i],
                            "credit_card": credit_cards[i],
                            "username": usernames[i],
                            "password": passwords[i]})
    context = {
        "all_data": all_data
    }
    return render(request, "list_view.html", context)
    

#Update
def detail_view(request, id):

    context = {}

    context["data"] = UsersDetails.objects.get(id = id)

    return render(request, "detail_view.html", context)

#update
def update_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id=id)

    form = UserDetailForm(request.POST or None, instance = obj)

    if form.is_valid():

        form.save()

        return HttpResponseRedirect("/"+id)

    context["form"] = form

    return render(request, "update_view.html", context)

#Delte
def delete_view(request, id):

    context = {}

    obj = get_object_or_404(UsersDetails, id = id)

    if request.method == "POST":

        obj.delete()

        return HttpResponseRedirect("/")

    return render(request, "delete_view.html", context)



